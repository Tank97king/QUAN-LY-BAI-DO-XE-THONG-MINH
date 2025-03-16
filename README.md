![logoDaiNam](https://github.com/user-attachments/assets/8ab299c0-ca53-42bb-8909-c821bcd71db7)<h1 align="center">🚗 HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE VỚI NHẬN DIỆN BIỂN SỐ </h1>

<div align="center">

<p align="center">
  <img src="images/logoDaiNam.png" alt="DaiNam University Logo" width="200"/>
  <img src="images/LogoAIoTLab.png" alt="AIoTLab Logo" width="170"/>
</p>

[![Made by AIoTLab](https://img.shields.io/badge/Made%20by%20AIoTLab-blue?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Fit DNU](https://img.shields.io/badge/Fit%20DNU-green?style=for-the-badge)](https://fitdnu.net/)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-red?style=for-the-badge)](https://dainam.edu.vn)

</div>

<h2 align="center">🚗 HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE </h2>

<p align="left">
  Hệ thống quản lý bãi đỗ xe tích hợp nhận diện biển số xe tự động, với giao diện web hiện đại để quản lý bãi đỗ một cách dễ dàng và hiệu quả. Dữ liệu điểm danh được lưu trữ trong liteSQL 
</p>

---
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

# 🚗 Smart Parking Management System with License Plate Recognition

An automated parking management system integrating license plate recognition, with a modern web interface for easy and efficient management.

---

## 🌟 Features
✅ Automatic license plate recognition with EasyOCR  
✅ Manage **6 parking spots**  
✅ **Modern & user-friendly** web interface  
✅ **Store parking history**  
✅ Track occupied & available spots  
✅ Display **entry/exit times**  

---

## 📌 System Requirements
### 🖥️ Software
- **Python 3.7+**
- Required Python libraries:
  ```bash
  pip install Flask EasyOCR OpenCV-Python NumPy Pillow
  ```

---

## 🚀 Installation & Setup Guide

### 1️⃣ Setup Environment
1. Ensure **Python 3.7+** is installed. If not, download it from [Python.org](https://www.python.org/).
2. Install required libraries:
   ```bash
   pip install Flask EasyOCR OpenCV-Python NumPy Pillow
   ```

---

### 2️⃣ Initialize Database
Create a new file `init_db.py` and add:
```python
from database import init_db
init_db()
```
Run the file to initialize the database:
```bash
python init_db.py
```

---

### 3️⃣ Add Parking Record
Create `add_record.py` and add:
```python
from database import add_parking_record
entry_time = add_parking_record('A1', 'ABC-123', '/path/to/image.jpg')
print(f"Entry time: {entry_time}")
```
Run the file to add a record:
```bash
python add_record.py
```

---

### ⚠️ Notes
- **ESP32-CAM should be directly connected to the laptop**, not as per the circuit diagram.
- **Updated Arduino code provided**, do not use the video’s code.

🚀 **Develop and improve this model for a smarter future!** 🚀

