from dotenv import load_dotenv  
load_dotenv()

import os
import pandas as pd
import numpy as np
from supabase import create_client 

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

risk_level = 0

supabase = create_client(url, key)

# Fetch all columns in one query (more efficient)
data = supabase.table("sensors_table").select(
    "created_at, ultrasonic_sensor, turbidity_sensor, flowrate_sensor"
).order("created_at").limit(100).execute()

# Load into DataFrame
df = pd.DataFrame(data.data)
df['created_at'] = pd.to_datetime(df['created_at'])
df = df.sort_values('created_at').reset_index(drop=True)

# ── 1. RATE OF CHANGE ──────────────────────────────────────────────
df['ultrasonic_roc']  = df['ultrasonic_sensor'].diff()
df['turbidity_roc']   = df['turbidity_sensor'].diff()
df['flowrate_roc']    = df['flowrate_sensor'].diff()

# ── 2. ROLLING AVERAGE (last 5 readings) ───────────────────────────
df['ultrasonic_avg']  = df['ultrasonic_sensor'].rolling(window=5).mean()
df['turbidity_avg']   = df['turbidity_sensor'].rolling(window=5).mean()
df['flowrate_avg']    = df['flowrate_sensor'].rolling(window=5).mean()

# ── 3. THRESHOLDS — adjust these to your sensor specs ──────────────
ULTRASONIC_HIGH   = 80    # e.g. level too high = blockage
TURBIDITY_HIGH    = 300   # e.g. murky water = debris
FLOWRATE_LOW      = 5     # e.g. low flow = clog forming
ROC_SPIKE         = 20    # sudden change threshold

# ── 4. RISK SCORING ────────────────────────────────────────────────
def calculate_risk(row):
    risk_score = 0
    reasons = []

    # Threshold checks
    if row['ultrasonic_sensor'] > ULTRASONIC_HIGH:
        risk_score += 30
        reasons.append("High ultrasonic level")
    if row['turbidity_sensor'] > TURBIDITY_HIGH:
        risk_score += 25
        reasons.append("High turbidity")
    if row['flowrate_sensor'] < FLOWRATE_LOW:
        risk_score += 25
        reasons.append("Low flow rate")

    # Rate of change spike checks
    if abs(row['ultrasonic_roc']) > ROC_SPIKE:
        risk_score += 20
        reasons.append("Ultrasonic spike")
    if abs(row['flowrate_roc']) > ROC_SPIKE:
        risk_score += 20
        reasons.append("Flowrate spike")

    # Rolling average deviation
    if pd.notna(row['ultrasonic_avg']) and row['ultrasonic_sensor'] > row['ultrasonic_avg'] * 1.3:
        risk_score += 15
        reasons.append("30% above average ultrasonic")
    if pd.notna(row['flowrate_avg']) and row['flowrate_sensor'] < row['flowrate_avg'] * 0.7:
        risk_score += 15
        reasons.append("30% below average flowrate")

    # Risk level label
    if risk_score < 30:
        risk_level = 0
        level = "🟢 LOW RISK"
    elif risk_score < 60:
        risk_level = 0
        level = "🟡 MEDIUM RISK"
    else:
        risk_level = 0
        level = "🔴 HIGH RISK"

    return pd.Series({'risk_score': risk_score, 'risk_level': level, 'reasons': ', '.join(reasons)})

# Apply risk scoring
df[['risk_score', 'risk_level', 'reasons']] = df.apply(calculate_risk, axis=1)

# Get the LATEST row's risk score (last reading)
latest_score = df['risk_score'].iloc[-1]

if latest_score >= 60:
    risk_level = 2
elif latest_score >= 30:
    risk_level = 1
else:
    risk_level = 0

print(f"Sending risk_level: {risk_level}")  # confirm it's not always 0
supabase.table("risk_table").upsert({"id": 1, "risk_level": risk_level}).execute()

# ── 5. OUTPUT ──────────────────────────────────────────────────────
print("\n===== SENSOR READINGS + CLOG RISK ANALYSIS =====\n")
for _, row in df.iterrows():
    print(f"Time:        {row['created_at']}")
    print(f"Ultrasonic:  {row['ultrasonic_sensor']} (ROC: {row['ultrasonic_roc']})")
    print(f"Turbidity:   {row['turbidity_sensor']}")
    print(f"Flow Rate:   {row['flowrate_sensor']} (ROC: {row['flowrate_roc']})")
    print(f"Risk:        {row['risk_level']} (Score: {row['risk_score']})")
    if row['reasons']:
        print(f"Reasons:     {row['reasons']}")
    print("-" * 50)

# Show any HIGH RISK alerts
high_risk = df[df['risk_level'].str.contains("HIGH")]
if not high_risk.empty:
    print("\n⚠️  HIGH RISK ALERTS DETECTED:")
    print(high_risk[['created_at', 'ultrasonic_sensor', 'turbidity_sensor', 'flowrate_sensor', 'risk_score', 'reasons']])

