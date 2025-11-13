from flask import Flask, request, jsonify
from database import get_db
from path_planner import get_next_step
import os

app = Flask(__name__)

# 接收 ESP32 上傳位置
@app.route('/update', methods=['POST'])
def update_vehicle():
    data = request.get_json()
    vehicle_id = data['id']
    x, y = data['x'], data['y']
    battery, status = data['battery'], data['status']

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # 更新車輛資訊
    cursor.execute("""
        REPLACE INTO vehicles (id, x, y, battery, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (vehicle_id, x, y, battery, status))
    db.commit()

    # 查找任務
    cursor.execute("SELECT * FROM tasks WHERE vehicle_id=%s AND done=FALSE LIMIT 1", (vehicle_id,))
    task = cursor.fetchone()

    # 讀取其他車輛位置（避障）
    cursor.execute("SELECT x, y FROM vehicles WHERE id != %s", (vehicle_id,))
    obstacles = [(row['x'], row['y']) for row in cursor.fetchall()]
    cursor.close()
    db.close()

    if not task:
        return jsonify({"task": "none"})

    # 取得下一步路徑
    target = (task['from_x'], task['from_y']) if status == "idle" else (task['to_x'], task['to_y'])
    next_pos = get_next_step((x, y), target, obstacles)
    print(f"🚗 {vehicle_id} 從 ({x},{y}) → 下一步 {next_pos} 目標 {target}")

    return jsonify({"next_x": next_pos[0], "next_y": next_pos[1]})

# 檔案上傳
@app.route('/upload/<vehicle_id>', methods=['POST'])
def upload_file(vehicle_id):
    file = request.files['file']
    os.makedirs("files", exist_ok=True)
    path = f"files/{vehicle_id}_{file.filename}"
    file.save(path)
    return jsonify({"saved": path})

if __name__ == '__main__':
    app.run(debug=True)
