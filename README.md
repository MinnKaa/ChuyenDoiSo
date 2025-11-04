<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>

<h2 align="center">
  ỨNG DỤNG CHUYỂN ĐỔI SỐ — PHÂN TÍCH BÁO CÁO TÀI CHÍNH BẰNG AI GEMINI
</h2>

<div align="center">
    <p align="center">
      <img src="https://github.com/Tank97king/LapTrinhMang/blob/main/CHAT%20TCP/%E1%BA%A2nh/aiotlab_logo.png?raw=true" alt="AIoTLab Logo" width="170"/>
      <img src="https://github.com/Tank97king/LapTrinhMang/blob/main/CHAT%20TCP/%E1%BA%A2nh/fitdnu_logo.png?raw=true" alt="FITDNU Logo" width="180"/>
      <img src="https://github.com/Tank97king/LapTrinhMang/blob/main/CHAT%20TCP/%E1%BA%A2nh/dnu_logo.png?raw=true" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)
</div>

---

## 📖 1. Giới thiệu hệ thống

`Ứng Dụng Chuyển Đổi Số` là một ứng dụng web sử dụng **AI Gemini của Google** để **phân tích và trực quan hóa dữ liệu tài chính** từ các báo cáo Excel.  
Hệ thống được xây dựng bằng **Streamlit**, hỗ trợ người dùng:
- Tải nhiều file báo cáo tài chính (*.xlsx*)
- Trò chuyện, đặt câu hỏi bằng tiếng Việt về dữ liệu tài chính
- Tự động sinh phân tích và biểu đồ bằng AI

---

## 🔧 2. Công nghệ sử dụng

| Thành phần | Công nghệ |
|-------------|------------|
| Giao diện web | Streamlit |
| Trí tuệ nhân tạo | Google Gemini API |
| Phân tích dữ liệu | Pandas, Altair |
| Quản lý môi trường | python-dotenv |
| Xử lý tệp Excel | pandas.read_excel() |

---

## 🚀 3. Hình ảnh giao diện và chức năng

<p align="center">
  <img src="https://github.com/MinnKaa/ChuyenDoiSo/blob/main/Ảnh/1.jpg?raw=true" alt="Trang chủ ứng dụng" width="700"/>
</p>
<p align="center"><em>Hình 1: Giao diện trang chủ của ứng dụng Chuyển Đổi Số</em></p>

<p align="center">
  <img src="https://github.com/MinnKaa/ChuyenDoiSo/blob/main/Ảnh/2.jpg?raw=true" alt="Mẫu biểu nhập dữ liệu" width="700"/>
</p>
<p align="center"><em>Hình 2: Biểu mẫu nhập liệu và xử lý dữ liệu số hóa</em></p>

<p align="center">
  <img src="https://github.com/MinnKaa/ChuyenDoiSo/blob/main/Ảnh/3.jpg?raw=true" alt="Kết quả hiển thị" width="700"/>
</p>
<p align="center"><em>Hình 3: Kết quả hiển thị sau khi xử lý dữ liệu</em></p>

---

## 📝 4. Cách chạy ứng dụng

1️⃣ Cài Python và các thư viện cần thiết**

```bash
pip install streamlit pandas altair python-dotenv google-generativeai openpyxl
2️⃣ Cấu hình API key Gemini

Tạo file .env trong cùng thư mục với code chính (ví dụ: app.py):

GOOGLE_API_KEY=your_google_api_key_here
3️⃣ Chạy ứng dụng Streamlit

Trong terminal, gõ lệnh:

streamlit run app.py
4️⃣ Cách sử dụng

Trong thanh bên trái, tải lên 1 hoặc nhiều file Excel (báo cáo tài chính).

Nhập câu hỏi vào ô chat, ví dụ:

“Phân tích doanh thu của các công ty trong năm 2024”

“So sánh lợi nhuận giữa các công ty quý 2/2023”

“Vẽ biểu đồ vốn chủ sở hữu theo thời gian”

Ứng dụng sẽ:

Hiển thị phân tích chi tiết bằng tiếng Việt từ AI Gemini

Tự động vẽ biểu đồ cột bằng Altair khi có yêu cầu “vẽ”, “so sánh”, “biểu đồ”
## 👤 6. Thông tin sinh viên

**Họ tên:** Vũ Đức Minh
**Lớp:** CNTT 16–02
**Email:** mvu2k4@gmail.com

© 2025 AIoTLab, Faculty of Information Technology, DaiNam University.  
