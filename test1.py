from supabase import create_client, Client

class Config:
    SUPABASE_URL = "https://your-project-id.supabase.co"
    SUPABASE_KEY = "your-anon-or-service-role-key"
    TABLE_NAME = "sensor_readings"

    
    MAX_TURBIDITY = 60
    MAX_WATER_LEVEL = 15      
    MAX_FLOWRATE = 10
    MAX_PRESSURE = 5



class SensorReading:
    def __init__(self, data: dict):
        self.id: int = data["id"]
        self.created_at: str = data["created_at"]
        self.ultrasonic: float = data["ultrasonic_sensor"]
        self.turbidity: float = data["turbidity_sensor"]
        self.flowrate: float = data["flowrate_sensor"]
        self.pressure: float = data["pressure_sensor"]
        self.time_value = data["time"]