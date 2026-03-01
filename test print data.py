from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from .env file

import os
from supabase import create_client 

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

ultrasonic_data = supabase.table("sensors_table").select("ultrasonic_sensor").limit(5).execute()
turbidity_data = supabase.table("sensors_table").select("turbidity_sensor").limit(5).execute()
flowrate_data = supabase.table("sensors_table").select("flowrate_sensor").limit(5).execute()


for i in range(5):
    ultrasonic_value = ultrasonic_data.data[i]["ultrasonic_sensor"]
    print(ultrasonic_value)
for i in range(5):
    turbidity_value = turbidity_data.data[i]["turbidity_sensor"]
    print(turbidity_value)  
for i in range(5):
    flowrate_value = flowrate_data.data[i]["flowrate_sensor"]
    print(flowrate_value)