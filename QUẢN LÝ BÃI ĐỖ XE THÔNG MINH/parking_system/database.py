# Import các thư viện cần thiết
import sqlite3  # Thư viện để làm việc với SQLite database
from datetime import datetime  # Thư viện để làm việc với thời gian

def init_db():
    # Hàm khởi tạo cơ sở dữ liệu
    # Tạo kết nối đến file parking.db, nếu chưa có sẽ tự động tạo mới
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    
    # Tạo bảng parking_records nếu chưa tồn tại
    # Cấu trúc bảng gồm:
    # - id: khóa chính, tự động tăng
    # - slot_number: số vị trí đỗ xe (bắt buộc)
    # - license_plate: biển số xe
    # - entry_time: thời gian vào bãi (bắt buộc)
    # - exit_time: thời gian ra khỏi bãi
    # - image_path: đường dẫn đến ảnh xe
    c.execute('''
        CREATE TABLE IF NOT EXISTS parking_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number TEXT NOT NULL,
            license_plate TEXT,
            entry_time DATETIME NOT NULL,
            exit_time DATETIME,
            image_path TEXT
        )
    ''')
    
    conn.commit()  # Lưu các thay đổi
    conn.close()   # Đóng kết nối

def add_parking_record(slot_number, license_plate, image_path):
    # Hàm thêm bản ghi mới khi có xe vào bãi
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    
    # Lấy thời gian hiện tại làm thời gian vào bãi
    entry_time = datetime.now()
    
    # Thêm bản ghi mới vào bảng với các thông tin:
    # số vị trí, biển số xe, thời gian vào, đường dẫn ảnh
    c.execute('''
        INSERT INTO parking_records (slot_number, license_plate, entry_time, image_path)
        VALUES (?, ?, ?, ?)
    ''', (slot_number, license_plate, entry_time, image_path))
    
    conn.commit()  # Lưu các thay đổi
    conn.close()   # Đóng kết nối
    return entry_time  # Trả về thời gian vào bãi

def update_exit_time(slot_number):
    # Hàm cập nhật thời gian ra khỏi bãi cho xe
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    
    # Lấy thời gian hiện tại làm thời gian ra khỏi bãi
    exit_time = datetime.now()
    
    # Cập nhật thời gian ra cho bản ghi của xe tại vị trí đã cho
    # và chưa có thời gian ra (đang đỗ trong bãi)
    c.execute('''
        UPDATE parking_records 
        SET exit_time = ? 
        WHERE slot_number = ? AND exit_time IS NULL
    ''', (exit_time, slot_number))
    
    conn.commit()  # Lưu các thay đổi
    conn.close()   # Đóng kết nối
    return exit_time  # Trả về thời gian ra khỏi bãi

def get_parking_history():
    # Hàm lấy toàn bộ lịch sử đỗ xe
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    
    # Lấy tất cả bản ghi, sắp xếp theo thời gian vào mới nhất đến cũ nhất
    c.execute('''
        SELECT * FROM parking_records 
        ORDER BY entry_time DESC
    ''')
    records = c.fetchall()  # Lấy tất cả kết quả
    
    conn.close()  # Đóng kết nối
    return records  # Trả về danh sách các bản ghi

def clear_parking_history():
    # Hàm xóa toàn bộ lịch sử đỗ xe
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    c.execute('DELETE FROM parking_records')  # Xóa tất cả bản ghi trong bảng
    conn.commit()  # Lưu các thay đổi
    conn.close()   # Đóng kết nối