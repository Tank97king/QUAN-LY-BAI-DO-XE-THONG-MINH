#include <Servo.h> // Thư viện điều khiển Servo
#include <Wire.h>  // Thư viện giao tiếp I2C
#include <LiquidCrystal_I2C.h> // Thư viện điều khiển LCD I2C
LiquidCrystal_I2C lcd(0x27, 20, 4); // Nếu dùng LCD 20x4
Servo myservo; // Khởi tạo đối tượng Servo
#define IR_ENTER 2  // Cảm biến lối vào
#define IR_BACK  4  // Cảm biến lối ra
#define IR_CAR1  5  // Cảm biến chỗ đỗ 1
#define IR_CAR2  6  // Cảm biến chỗ đỗ 2
#define IR_CAR3  7  // Cảm biến chỗ đỗ 3
#define IR_CAR4  8  // Cảm biến chỗ đỗ 4
#define IR_CAR5  9  // Cảm biến chỗ đỗ 5
#define IR_CAR6 10  // Cảm biến chỗ đỗ 6
// Biến lưu trạng thái các chỗ đỗ (1: có xe, 0: trống)
int S1 = 0, S2 = 0, S3 = 0, S4 = 0, S5 = 0, S6 = 0;
// Số chỗ đỗ trống (ban đầu là 6)
int slot = 6;
void setup() {
  // Khởi tạo Serial để debug
  Serial.begin(9600);
  // Cấu hình các chân cảm biến là INPUT
  pinMode(IR_CAR1, INPUT);
  pinMode(IR_CAR2, INPUT);
  pinMode(IR_CAR3, INPUT);
  pinMode(IR_CAR4, INPUT);
  pinMode(IR_CAR5, INPUT);
  pinMode(IR_CAR6, INPUT);
  pinMode(IR_ENTER, INPUT);
  pinMode(IR_BACK, INPUT);

  // Gắn servo vào chân 3 và đặt góc ban đầu là 90 độ (cổng đóng)
  myservo.attach(3);
  myservo.write(90);

  // Khởi tạo LCD
  lcd.init(); // Khởi tạo giao tiếp I2C
  lcd.begin(20, 4); // Khởi tạo LCD 20x4 (hoặc 16x2 nếu đã sửa)
  lcd.backlight(); // Bật đèn nền

  // Hiển thị thông điệp khởi động
  lcd.setCursor(0, 1);
  lcd.print("    Car Parking  ");
  lcd.setCursor(0, 2);
  lcd.print("      System     ");
  delay(2000);
  lcd.clear();

  // Đọc trạng thái ban đầu của các cảm biến
  Read_Sensor();

  // Tính số chỗ đỗ trống ban đầu
  int total = S1 + S2 + S3 + S4 + S5 + S6;
  slot = slot - total;

  // In thông tin debug ra Serial Monitor
  Serial.print("Initial slots available: ");
  Serial.println(slot);
}

void loop() {
  // Đọc trạng thái cảm biến
  Read_Sensor();

  // Hiển thị số chỗ đỗ trống
  lcd.setCursor(0, 0);
  lcd.print("   Have Slot: ");
  lcd.print(slot);
  if (slot < 10) lcd.print(" "); // Thêm khoảng trống nếu slot là số 1 chữ số

  // Hiển thị trạng thái từng chỗ đỗ
  lcd.setCursor(0, 1);
  lcd.print(S1 == 1 ? "S1:Fill " : "S1:Empty");

  lcd.setCursor(10, 1);
  lcd.print(S2 == 1 ? "S2:Fill " : "S2:Empty");

  lcd.setCursor(0, 2);
  lcd.print(S3 == 1 ? "S3:Fill " : "S3:Empty");

  lcd.setCursor(10, 2);
  lcd.print(S4 == 1 ? "S4:Fill " : "S4:Empty");

  lcd.setCursor(0, 3);
  lcd.print(S5 == 1 ? "S5:Fill " : "S5:Empty");

  lcd.setCursor(10, 3);
  lcd.print(S6 == 1 ? "S6:Fill " : "S6:Empty");

  // Debug: In trạng thái cảm biến ra Serial Monitor
  Serial.print("Slots: ");
  Serial.print(slot);
  Serial.print(" | S1: ");
  Serial.print(S1);
  Serial.print(" S2: ");
  Serial.print(S2);
  Serial.print(" S3: ");
  Serial.print(S3);
  Serial.print(" S4: ");
  Serial.print(S4);
  Serial.print(" S5: ");
  Serial.print(S5);
  Serial.print(" S6: ");
  Serial.println(S6);

  // Điều khiển cổng khi xe vào (dựa trên cảm biến IR_ENTER)
  if (digitalRead(IR_ENTER) == 0 && slot > 0) {
    myservo.write(180); // Mở cổng
    delay(2000); // Giữ cổng mở 2 giây
    myservo.write(90); // Đóng cổng
    slot--; // Giảm số chỗ trống
    Serial.println("Car entered. Slots left: " + String(slot));
  } else if (digitalRead(IR_ENTER) == 0 && slot <= 0) {
    lcd.setCursor(0, 0);
    lcd.print(" Sorry Parking Full ");
    delay(1500);
    lcd.clear();
    Serial.println("Parking full!");
  }

  // Điều khiển cổng khi xe ra (dựa trên cảm biến IR_BACK)
  if (digitalRead(IR_BACK) == 0) {
    myservo.write(180); // Mở cổng
    delay(2000); // Giữ cổng mở 2 giây
    myservo.write(90); // Đóng cổng
    slot++; // Tăng số chỗ trống
    Serial.println("Car exited. Slots left: " + String(slot));
  }

  delay(100); // Delay nhỏ để tránh đọc cảm biến quá nhanh
}

// Hàm đọc trạng thái cảm biến
void Read_Sensor() {
  // Đặt lại trạng thái các chỗ đỗ
  S1 = S2 = S3 = S4 = S5 = S6 = 0;

  // Đọc cảm biến (0: có xe, 1: không có xe)
  // Lưu ý: Một số cảm biến IR có logic đảo ngược (LOW khi phát hiện vật thể)
  if (digitalRead(IR_CAR1) == LOW) S1 = 1; // Sửa logic đọc cảm biến
  if (digitalRead(IR_CAR2) == LOW) S2 = 1; // Sửa logic đọc cảm biến
  if (digitalRead(IR_CAR3) == LOW) S3 = 1; // Sửa logic đọc cảm biến
  if (digitalRead(IR_CAR4) == LOW) S4 = 1; // Sửa logic đọc cảm biến
  if (digitalRead(IR_CAR5) == LOW) S5 = 1; // Sửa logic đọc cảm biến
  if (digitalRead(IR_CAR6) == LOW) S6 = 1; // Sửa logic đọc cảm biến
}