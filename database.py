# database.py

import mysql.connector
from config import MYSQL_CONFIG

db = mysql.connector.connect(**MYSQL_CONFIG)
cursor = db.cursor(dictionary=True)

def update_vehicle(vehicle_id, x, y, battery, status):
    sql = """
    REPLACE INTO vehicles (id, x, y, battery, status)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (vehicle_id, x, y, battery, status))
    db.commit()

def get_other_vehicles(vehicle_id):
    cursor.execute("SELECT id, x, y FROM vehicles WHERE id != %s", (vehicle_id,))
    return cursor.fetchall()

def get_vehicle_task(vehicle_id):
    cursor.execute(
        "SELECT * FROM tasks WHERE vehicle_id = %s AND done = 0 LIMIT 1",
        (vehicle_id,)
    )
    return cursor.fetchone()
