from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import requests, os, json

DB = "data.db"
MODEL_SVC = os.getenv("MODEL_SVC", "http://ml:8001/predict")
TWILIO_FROM = os.getenv("TWILIO_FROM", "+123456")
TWILIO_API_KEY = os.getenv("TWILIO_API_KEY", "changeme")

app = FastAPI(title="Smart Health EWS API")

class HealthReport(BaseModel):
    reporter_id: str
    village: str
    symptoms: list
    cases: int
    timestamp: str  # ISO

class WaterReport(BaseModel):
    sensor_id: str
    village: str
    pH: float
    turbidity: float
    bacterial_index: float
    timestamp: str

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS health_reports (id INTEGER PRIMARY KEY, reporter_id TEXT, village TEXT, symptoms TEXT, cases INTEGER, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS water_reports (id INTEGER PRIMARY KEY, sensor_id TEXT, village TEXT, pH REAL, turbidity REAL, bacterial_index REAL, timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/report/health")
def post_health(r: HealthReport):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO health_reports (reporter_id, village, symptoms, cases, timestamp) VALUES (?,?,?,?,?)",
              (r.reporter_id, r.village, json.dumps(r.symptoms), r.cases, r.timestamp))
    conn.commit()
    conn.close()

    # Call ML prediction service
    payload = {"village": r.village, "symptoms": r.symptoms, "cases": r.cases}
    try:
        resp = requests.post(MODEL_SVC, json=payload, timeout=5)
        pred = resp.json()
        if pred.get("risk") == "high":
            send_alert(f"High outbreak risk in {r.village}: {pred.get('score')}")
    except Exception as e:
        print("ML svc unreachable:", e)
    return {"status":"ok"}

@app.post("/report/water")
def post_water(w: WaterReport):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO water_reports (sensor_id,village,pH,turbidity,bacterial_index,timestamp) VALUES (?,?,?,?,?,?)",
              (w.sensor_id, w.village, w.pH, w.turbidity, w.bacterial_index, w.timestamp))
    conn.commit()
    conn.close()
    if w.turbidity > 5.0 or w.bacterial_index > 0.5 or w.pH < 6.5 or w.pH > 8.5:
        send_alert(f"Contaminated water detected at {w.village} (sensor {w.sensor_id})")
    return {"status":"ok"}

def send_alert(message):
    print("ALERT:", message)

@app.get("/reports/summary")
def summary():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT village, COUNT(*) FROM health_reports GROUP BY village")
    rows = c.fetchall()
    return {"summary": rows}
