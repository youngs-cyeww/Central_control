# Central_control
中控




建立 conda 環境
mkdir C:\Central_control_topic
cd C:\Central_control_topic
conda create -n logistics_server python=3.11
conda activate logistics_server
pip install flask mysql-connector-python









登入 MySQL：

mysql -u root -p


建立資料庫：

CREATE DATABASE logistics;
USE logistics;

CREATE TABLE vehicles (
    id VARCHAR(20) PRIMARY KEY,
    x INT,
    y INT,
    battery INT,
    status VARCHAR(20)
);

CREATE TABLE tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id VARCHAR(20),
    from_x INT,
    from_y INT,
    to_x INT,
    to_y INT,
    done BOOLEAN DEFAULT FALSE
);








ESP32 端程式（Arduino）
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "你的WiFi";
const char* password = "你的密碼";
const char* server = "http://你的電腦IP:5000";

float x = 0, y = 0;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(String(server) + "/update");
    http.addHeader("Content-Type", "application/json");

    String body = "{\"id\":\"car1\",\"x\":" + String(x) + ",\"y\":" + String(y) + ",\"battery\":90,\"status\":\"moving\"}";
    int code = http.POST(body);

    if (code == 200) {
      String payload = http.getString();
      Serial.println("Server 回傳: " + payload);
      int nx = payload.substring(payload.indexOf("next_x")+8, payload.indexOf(",")-1).toInt();
      int ny = payload.substring(payload.indexOf("next_y")+8, payload.lastIndexOf("}")).toInt();
      x = nx;
      y = ny;
    } else {
      Serial.println("HTTP Error: " + String(code));
    }
    http.end();
  }
  delay(2000);
}








1️⃣ 啟動 MySQL
2️⃣ 啟動伺服器

conda activate logistics_server
cd C:\Central_control_topic
python app.py


3️⃣ 在 MySQL 新增任務：

INSERT INTO tasks (vehicle_id, from_x, from_y, to_x, to_y) VALUES ('car1', 1, 1, 2, 3);


4️⃣ 啟動 ESP32 → 觀察串口回傳的指令（中控會指派座標）
