import sqlite3
from datetime import datetime

class SensorVector:
    def __init__(self, db_path="sensor_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with sensor table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_name TEXT NOT NULL,
                value REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def insert_sensor_value(self, sensor_name, value):
        """Insert a sensor reading into the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sensors (sensor_name, value) VALUES (?, ?)",
            (sensor_name, value)
        )
        conn.commit()
        conn.close()
    
    def get_sensor_values(self, sensor_name=None):
        """Retrieve sensor values from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if sensor_name:
            cursor.execute("SELECT * FROM sensors WHERE sensor_name = ?", (sensor_name,))
        else:
            cursor.execute("SELECT * FROM sensors")
        results = cursor.fetchall()
        conn.close()
        return results


if __name__ == "__main__":
    sensor = SensorVector()
    sensor.insert_sensor_value("temperature", 23.5)
    sensor.insert_sensor_value("humidity", 65.2)
    print(sensor.get_sensor_values())