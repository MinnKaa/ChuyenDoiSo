import streamlit as st
import pandas as pd
import altair as alt
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

# =======================
# ⚙️ CẤU HÌNH
# =======================
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

st.set_page_config(page_title="Gemini Phân tích Tài chính", layout="wide")
st.title("💬 Chat Phân tích Báo cáo Tài chính")

# =======================
# 📂 UPLOAD FILE EXCEL
# =======================
st.sidebar.header("📂 Tải dữ liệu Excel")
uploaded_files = st.sidebar.file_uploader("", type=["xlsx"], accept_multiple_files=True)

dfs = {}
if uploaded_files:
    for f in uploaded_files:
        try:
            all_sheets = pd.read_excel(f, sheet_name=None)
            sheet_data = {}
            for sheet_name, df in all_sheets.items():
                if df.empty:
                    continue
                df = df.dropna(how="all").reset_index(drop=True)
                df.columns = [str(c).strip() for c in df.columns]
                sheet_data[sheet_name] = df
            dfs[f.name.split(".")[0]] = sheet_data
        except Exception as e:
            st.sidebar.error(f"❌ Lỗi đọc file {f.name}: {e}")
    st.sidebar.success(f"✅ Đã tải {len(dfs)} file thành công")

# =======================
# 💬 LỊCH SỬ CHAT
# =======================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_plot" not in st.session_state:
    st.session_state.last_plot = False  # Có biểu đồ gần nhất hay chưa

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =======================
# 💬 NHẬN YÊU CẦU
# =======================
prompt = st.chat_input("Nhập yêu cầu: ")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not dfs:
        with st.chat_message("assistant"):
            st.error("⚠️ Vui lòng tải ít nhất 1 file Excel trước khi hỏi.")
        st.stop()

    # =======================
    # 🧠 PHÂN TÍCH DỮ LIỆU
    # =======================
    combined_info = ""
    for company, sheets in dfs.items():
        combined_info += f"\n📘 {company}\n"
        for sheet_name, df in sheets.items():
            combined_info += f"\n--- {sheet_name} ---\n{df.head(5).to_string(index=False)}\n"

    base_prompt = f"""
    Bạn là chuyên gia tài chính Việt Nam.
    Dưới đây là dữ liệu từ báo cáo tài chính của nhiều công ty.
    {combined_info}

    Câu hỏi người dùng: {prompt}

    - Nếu câu hỏi là phân tích, hãy trả lời tự nhiên, chi tiết.
    - Nếu câu hỏi là 'vẽ' hay 'so sánh', chỉ mô tả loại biểu đồ phù hợp (phần code sẽ xử lý hiển thị).
    """

    with st.chat_message("assistant"):
        with st.spinner("🧠 Gemini đang phân tích..."):
            try:
                response = model.generate_content(base_prompt)
                answer = response.text.strip()
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"🚫 Lỗi khi gọi Gemini: {e}")
                st.stop()

    # =======================
    # 🎨 VẼ BIỂU ĐỒ (chỉ khi có yêu cầu)
    # =======================
    if any(k in prompt.lower() for k in ["vẽ", "so sánh", "biểu đồ"]):
        with st.chat_message("assistant"):
            st.markdown("### 📊 Biểu đồ tài chính")

            # Nhận diện chỉ tiêu cần vẽ
            keywords = ["doanh thu", "lợi nhuận", "tài sản", "vốn", "nợ", "tiền"]
            keyword = next((kw for kw in keywords if kw in prompt.lower()), None)
            if not keyword:
                st.warning("⚠️ Không nhận diện được chỉ tiêu. Hãy thử với các từ như 'doanh thu', 'lợi nhuận'...")
                st.stop()

            # Nhận diện năm (nếu có)
            year_match = re.search(r"20\d{2}", prompt)
            target_year = year_match.group(0) if year_match else None

            # Nhận diện quý (nếu có)
            quarter_match = re.search(r"quý\s*[1-4]", prompt.lower())
            target_quarter = quarter_match.group(0).replace(" ", "") if quarter_match else None

            plot_data = []

            for company, sheets in dfs.items():
                for sheet_name, df in sheets.items():
                    df = df.dropna(how="all").reset_index(drop=True)
                    df.columns = [str(c).strip() for c in df.columns]
                    if df.empty or len(df.columns) < 2:
                        continue

                    col0_clean = (
                        df.iloc[:, 0]
                        .astype(str)
                        .str.replace(r"[\d\.\-\–]", "", regex=True)
                        .str.strip()
                        .str.lower()
                    )

                    matched_rows = df[col0_clean.str.contains(keyword, regex=False, na=False)]
                    if matched_rows.empty:
                        continue

                    for _, row in matched_rows.iterrows():
                        row_name = str(row.iloc[0])
                        for col in df.columns[1:]:
                            col_name = str(col)

                            # Lọc theo năm
                            if target_year and target_year not in col_name:
                                continue

                            # Lọc theo quý
                            if target_quarter and target_quarter not in col_name.lower().replace(" ", ""):
                                continue

                            value = pd.to_numeric(str(row[col]).replace(",", "").strip(), errors="coerce")
                            if pd.notna(value):
                                plot_data.append({
                                    "Công ty": company,
                                    "Sheet": sheet_name,
                                    "Chỉ tiêu": row_name,
                                    "Thời gian": col_name,
                                    "Giá trị": value
                                })

            plot_df = pd.DataFrame(plot_data)

            if plot_df.empty:
                st.warning("⚠️ Không tìm thấy dữ liệu phù hợp.")
            else:
                plot_df = plot_df.groupby(["Công ty", "Thời gian"], as_index=False)["Giá trị"].mean()

                chart = (
    alt.Chart(plot_df)
    .mark_bar(size=35)  # 👈 chỉnh độ rộng cột (giá trị càng nhỏ cột càng mảnh, 15–30 là hợp lý)
    .encode(
    x=alt.X("Thời gian:N", title="Thời gian", axis=alt.Axis(labelAngle=0)),
    xOffset="Công ty:N",  # 👈 dịch cột sang ngang theo tên công ty
    y=alt.Y("Giá trị:Q", title="Giá trị (VNĐ)"),
    color=alt.Color("Công ty:N", title="Công ty"),
    tooltip=[
        alt.Tooltip("Công ty:N", title="Công ty"),
        alt.Tooltip("Thời gian:N", title="Thời gian"),
        alt.Tooltip("Giá trị:Q", title="Giá trị (VNĐ)")
    ]
)
    .configure_view(stroke=None)
    .properties(
        width=120,  # 👈 giảm chiều rộng mỗi nhóm để biểu đồ gọn hơn
        height=400,
        title=f"So sánh {keyword.title()} giữa các công ty"
    )
                )

                st.altair_chart(chart, use_container_width=True)
                st.session_state.last_plot = True  # ✅ đánh dấu đã vẽ biểu đồ

    else:
        # Nếu chỉ là phân tích (không có từ “vẽ/biểu đồ”) thì KHÔNG vẽ lại
        if st.session_state.last_plot:
            pass  # ✅ Giữ nguyên biểu đồ cũ
