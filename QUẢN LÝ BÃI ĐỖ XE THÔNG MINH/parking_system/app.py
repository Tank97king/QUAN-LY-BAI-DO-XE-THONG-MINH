# Import các thư viện cần thiết
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, redirect
import os  # Thư viện để làm việc với hệ thống tệp
import csv  # Thư viện để đọc/ghi file CSV
from datetime import datetime  # Thư viện để làm việc với thời gian
from PIL import Image  # Thư viện xử lý ảnh
import io  # Thư viện input/output
import base64  # Thư viện mã hóa/giải mã base64
import easyocr  # Thư viện OCR để nhận dạng biển số xe
import numpy as np  # Thư viện tính toán số học
import cv2  # Thư viện xử lý ảnh OpenCV
from database import init_db, add_parking_record, update_exit_time, get_parking_history, clear_parking_history  # Import các hàm từ module database

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Khởi tạo cơ sở dữ liệu
init_db()

# Cấu hình thư mục upload với đường dẫn tuyệt đối
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(f"Upload folder path: {UPLOAD_FOLDER}")  # Log để debug

# Khởi tạo OCR reader để đọc tiếng Anh và tiếng Việt
reader = easyocr.Reader(['en', 'vi'])

# Đảm bảo thư mục upload tồn tại
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    print(f"Successfully created/verified upload directory: {app.config['UPLOAD_FOLDER']}")
except Exception as e:
    print(f"Error creating upload directory: {str(e)}")

# Lưu trữ trạng thái các vị trí đỗ xe
parking_slots = {
    f'slot_{i}': {
        'status': 'empty',  # Trạng thái: trống
        'image': None,      # Đường dẫn ảnh
        'license_plate': None,  # Biển số xe
        'entry_time': None     # Thời gian vào
    } for i in range(1, 7)  # Tạo 6 vị trí đỗ xe
}

@app.route('/')
def index():
    # Hiển thị trang chủ với thông tin các vị trí đỗ xe
    return render_template('index.html', parking_slots=parking_slots)

@app.route('/static/uploads/<path:filename>')
def serve_image(filename):
    # Phục vụ file ảnh từ thư mục upload
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        print(f"Error serving image {filename}: {str(e)}")
        return jsonify({'error': 'Image not found'}), 404

def detect_license_plate(image_array):
    # Hàm nhận dạng biển số xe từ ảnh
    try:
        results = reader.readtext(image_array)
        if results:
            # Lấy kết quả có độ tin cậy cao nhất
            best_result = max(results, key=lambda x: x[2])
            return best_result[1]
    except Exception as e:
        print(f"Error in license plate detection: {str(e)}")
    return None

@app.route('/upload', methods=['POST'])
def upload_image():
    # API xử lý upload ảnh
    try:
        print("Received upload request")
        data = request.get_json()
        print(f"Received data keys: {data.keys() if data else 'No data'}")
        
        # Kiểm tra dữ liệu đầu vào
        if not data:
            print("No JSON data received")
            return jsonify({'error': 'No JSON data received'}), 400

        slot = data.get('slot')
        print(f"Slot from request: {slot}")
        
        if not slot:
            print("No slot specified in request")
            return jsonify({'error': 'No slot specified'}), 400
            
        if slot not in parking_slots:
            print(f"Invalid slot: {slot}")
            return jsonify({'error': 'Invalid slot'}), 400

        image_data = data.get('image')
        if not image_data:
            print("No image data received")
            return jsonify({'error': 'No image data'}), 400

        # Xử lý dữ liệu ảnh base64
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]

        # Giải mã ảnh base64
        try:
            image_bytes = base64.b64decode(image_data)
            print("Successfully decoded base64 image")
        except Exception as e:
            print(f"Error decoding base64 image: {str(e)}")
            return jsonify({'error': 'Invalid image data format'}), 400
        
        # Chuyển đổi ảnh sang numpy array
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            print("Successfully converted image to numpy array")
        except Exception as e:
            print(f"Error converting image: {str(e)}")
            return jsonify({'error': 'Error processing image'}), 400
        
        if img is None:
            print("Failed to decode image")
            return jsonify({'error': 'Invalid image data'}), 400

        # Nhận dạng biển số xe
        license_plate = detect_license_plate(img)
        print(f"Detected license plate: {license_plate}")
        
        # Tạo tên file với timestamp
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y%m%d_%H%M%S')
        filename = f'slot_{slot}_{timestamp}.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print(f"Saving image to: {filepath}")
        
        # Lưu ảnh
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            cv2.imwrite(filepath, img)
            print(f"Successfully saved image to {filepath}")
            
            if not os.path.exists(filepath):
                raise Exception("File was not saved successfully")
                
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            return jsonify({'error': 'Error saving image'}), 500
        
        # Thêm bản ghi vào database
        entry_time = add_parking_record(
            slot_number=slot,
            license_plate=license_plate,
            image_path=filename
        )
        
        # Cập nhật thông tin vị trí đỗ xe
        parking_slots[slot]['status'] = 'occupied'
        parking_slots[slot]['image'] = filename
        parking_slots[slot]['license_plate'] = license_plate
        parking_slots[slot]['entry_time'] = entry_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Tạo response
        response_data = {
            'success': True,
            'message': 'Image uploaded successfully',
            'filename': filename,
            'image_url': url_for('static', filename=f'uploads/{filename}', _external=True),
            'license_plate': license_plate,
            'entry_time': parking_slots[slot]['entry_time']
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error in upload_image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/clear_slot/<slot>')
def clear_slot(slot):
    # API xóa thông tin vị trí đỗ xe
    if slot in parking_slots:
        # Xóa file ảnh nếu tồn tại
        if parking_slots[slot]['image']:
            try:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], parking_slots[slot]['image'])
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"Successfully removed file: {filepath}")
            except Exception as e:
                print(f"Error removing file: {str(e)}")
        
        # Cập nhật thời gian ra trong database
        update_exit_time(slot)
        
        # Xóa thông tin vị trí đỗ xe
        parking_slots[slot]['status'] = 'empty'
        parking_slots[slot]['image'] = None
        parking_slots[slot]['license_plate'] = None
        parking_slots[slot]['entry_time'] = None
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid slot'}), 400

@app.route('/parking_history')
def parking_history():
    # Hiển thị lịch sử đỗ xe
    records = get_parking_history()
    return render_template('parking_history.html', records=records)

@app.route('/export_csv')
def export_csv():
    # API xuất dữ liệu ra file CSV
    try:
        records = get_parking_history()
        csv_file = os.path.join(app.config['UPLOAD_FOLDER'], 'parking_history.csv')
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Slot Number', 'License Plate', 'Entry Time', 'Exit Time', 'Image Path'])
            writer.writerows(records)
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'parking_history.csv', as_attachment=True)
    except Exception as e:
        print(f"Error exporting CSV: {str(e)}")
        return jsonify({'error': 'Error exporting CSV'}), 500

@app.route('/clear_history')
def clear_history():
    # API xóa toàn bộ lịch sử
    try:
        clear_parking_history()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error clearing history: {str(e)}")
        return jsonify({'error': 'Error clearing history'}), 500

@app.route('/get_statistics')
def get_statistics():
    # API lấy thống kê số vị trí trống/đã đỗ
    try:
        records = get_parking_history()
        occupied = len([r for r in records if r[4] is None])  # Đếm số xe đang đỗ (chưa có thời gian ra)
        available = len(parking_slots) - occupied  # Tính số vị trí còn trống
        return jsonify({'occupied': occupied, 'available': available})
    except Exception as e:
        print(f"Error getting statistics: {str(e)}")
        return jsonify({'error': 'Error getting statistics'}), 500

if __name__ == '__main__':
    # Chạy ứng dụng Flask
    app.run(host='0.0.0.0', port=5000, debug=True)