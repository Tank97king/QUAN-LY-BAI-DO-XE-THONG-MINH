<h1 align="center">🚗 HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE VỚI NHẬN DIỆN BIỂN SỐ </h1>

<div align="center">

<p align="center">
</p>
<p align="center">
<img src="QUẢN LÝ BÃI ĐỖ XE THÔNG MINH/logoDaiNam.png" alt="DaiNam University Logo" width="200"/>
<img src="QUẢN LÝ BÃI ĐỖ XE THÔNG MINH/LogoAIoTLab.png" alt="AIoTLab Logo" width="170"/>
</p>

</div>


<p align="left">
  Hệ thống quản lý bãi đỗ xe tích hợp nhận diện biển số xe tự động, với giao diện web hiện đại để quản lý bãi đỗ một cách dễ dàng và hiệu quả. Dữ liệu điểm danh được lưu trữ trong liteSQL 
</p>

---
## 🌟 Sơ Đồ Kết Nối Mạch
</p>
<p align="center">
<img src="QUẢN LÝ BÃI ĐỖ XE THÔNG MINH/Sơ đồ mạch của dự án.png" alt="DaiNam University Logo" width="700"/>
</p>


---
## 🌟 Tính Năng
✅ Nhận diện biển số xe tự động với EasyOCR  
✅ Quản lý **6 vị trí đỗ xe**  
✅ Giao diện web **hiện đại & dễ sử dụng**  
✅ **Lưu trữ lịch sử** đỗ xe  
✅ Thống kê số lượng xe đang đỗ và chỗ trống  
✅ Hiển thị **thời gian vào/ra** của xe  

---

## 📌 Yêu Cầu Hệ Thống
### 🖥️ Phần Mềm
- **Python 3.7+**
- Các thư viện Python cần thiết:
  ```bash
  pip install Flask EasyOCR OpenCV-Python NumPy Pillow
  Flask==2.3.3
  Pillow==10.2.0
  numpy==1.26.4
  opencv-python==4.9.0.80
  torch==2.2.0
  torchvision==0.17.0
  easyocr==1.7.1 
  ```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Hệ Thống

### 1️⃣ Cài Đặt Môi Trường
1. Đảm bảo bạn đã cài đặt **Python 3.7+**. Nếu chưa, hãy tải về từ [Python.org](https://www.python.org/).
2. Cài đặt các thư viện cần thiết bằng lệnh:
   ```bash
   pip install Flask EasyOCR OpenCV-Python NumPy Pillow
   ```

---

### 2️⃣ Khởi Tạo Cơ Sở Dữ Liệu
Tạo một file mới `init_db.py` và thêm đoạn mã sau:
```python
from database import init_db
init_db()
```
Chạy file để tạo cơ sở dữ liệu:
```bash
python init_db.py
```

---

### 3️⃣ Thêm Bản Ghi Đỗ Xe
Tạo file `add_record.py` và thêm mã sau:
```python
from database import add_parking_record
entry_time = add_parking_record('A1', 'ABC-123', '/path/to/image.jpg')
print(f"Entry time: {entry_time}")
```
Chạy file để thêm bản ghi:
```bash
python add_record.py
```

---

### 4️⃣ Cập Nhật Thời Gian Ra
Tạo file `update_exit.py` và thêm mã sau:
```python
from database import update_exit_time
exit_time = update_exit_time('A1')
print(f"Exit time: {exit_time}")
```
Chạy file để cập nhật thời gian ra:
```bash
python update_exit.py
```

---

### 5️⃣ Lấy Lịch Sử Đỗ Xe
Tạo file `get_history.py` và thêm mã sau:
```python
from database import get_parking_history
records = get_parking_history()
for record in records:
    print(record)
```
Chạy file để xem lịch sử đỗ xe:
```bash
python get_history.py
```

---

### 6️⃣ Xóa Lịch Sử Đỗ Xe
Tạo file `clear_history.py` và thêm mã sau:
```python
from database import clear_parking_history
clear_parking_history()
print("Parking history cleared.")
```
Chạy file để xóa lịch sử đỗ xe:
```bash
python clear_history.py
```

---

## ⚠️ Lưu Ý
- **ESP32-CAM không cắm như sơ đồ mạch**, mà **cắm thẳng vào laptop**.
- **Code Arduino đã được cập nhật và sửa lỗi**, không chạy theo video sẽ gặp lỗi.

---

## 🎯 Mục Tiêu
- **Tự động hóa quy trình quản lý bãi đỗ xe** bằng công nghệ nhận diện biển số xe.
- **Nâng cao hiệu suất và giảm thiểu lỗi thủ công** trong quản lý xe ra vào.
- **Dễ dàng tích hợp với hệ thống IoT** để giám sát từ xa.

🚀 **Hãy triển khai ngay và trải nghiệm sự tiện lợi!** 🚀

---
## 📝 Bản quyền

© 2025 Đinh Thế Thành-Nhóm 3-CNTT_16-01, Khoa Công nghệ Thông tin, Đại học Đại Nam. Mọi quyền được bảo lưu.
<div align="center">
Được thực hiện bởi 💻 Nhóm 3-CNTT_16-01 tại Đại học Đại Nam

Email cá nhân : dinhthethanh73@gmail.com
