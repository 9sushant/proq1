import pandas as pd
import io
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

# Initialize the FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# --- MODIFICATION ---
# Embed the JSON data as a multi-line string to work in Vercel's environment.
json_data_string = """
[
  { "region": "apac", "service": "catalog", "latency_ms": 119.71, "uptime_pct": 98.726, "timestamp": 20250301 },
  { "region": "apac", "service": "catalog", "latency_ms": 171.85, "uptime_pct": 97.186, "timestamp": 20250302 },
  { "region": "apac", "service": "support", "latency_ms": 160.67, "uptime_pct": 97.313, "timestamp": 20250303 },
  { "region": "apac", "service": "analytics", "latency_ms": 213.11, "uptime_pct": 98.637, "timestamp": 20250304 },
  { "region": "apac", "service": "checkout", "latency_ms": 131.24, "uptime_pct": 97.344, "timestamp": 20250305 },
  { "region": "apac", "service": "catalog", "latency_ms": 152.25, "uptime_pct": 98.627, "timestamp": 20250306 },
  { "region": "apac", "service": "analytics", "latency_ms": 218.79, "uptime_pct": 98.089, "timestamp": 20250307 },
  { "region": "apac", "service": "support", "latency_ms": 239.48, "uptime_pct": 97.986, "timestamp": 20250308 },
  { "region": "apac", "service": "recommendations", "latency_ms": 229.47, "uptime_pct": 97.706, "timestamp": 20250309 },
  { "region": "apac", "service": "recommendations", "latency_ms": 136.26, "uptime_pct": 98.512, "timestamp": 20250310 },
  { "region": "apac", "service": "catalog", "latency_ms": 203.9, "uptime_pct": 98.688, "timestamp": 20250311 },
  { "region": "apac", "service": "recommendations", "latency_ms": 133.34, "uptime_pct": 99.367, "timestamp": 20250312 },
  { "region": "emea", "service": "payments", "latency_ms": 177.83, "uptime_pct": 98.226, "timestamp": 20250301 },
  { "region": "emea", "service": "recommendations", "latency_ms": 154.14, "uptime_pct": 99.063, "timestamp": 20250302 },
  { "region": "emea", "service": "catalog", "latency_ms": 161.37, "uptime_pct": 97.473, "timestamp": 20250303 },
  { "region": "emea", "service": "checkout", "latency_ms": 173.63, "uptime_pct": 97.364, "timestamp": 20250304 },
  { "region": "emea", "service": "catalog", "latency_ms": 140.53, "uptime_pct": 97.618, "timestamp": 20250305 },
  { "region": "emea", "service": "recommendations", "latency_ms": 190.13, "uptime_pct": 97.686, "timestamp": 20250306 },
  { "region": "emea", "service": "checkout", "latency_ms": 202.14, "uptime_pct": 98.718, "timestamp": 20250307 },
  { "region": "emea", "service": "payments", "latency_ms": 172.79, "uptime_pct": 99.477, "timestamp": 20250308 },
  { "region": "emea", "service": "support", "latency_ms": 118.38, "uptime_pct": 98.461, "timestamp": 20250309 },
  { "region": "emea", "service": "checkout", "latency_ms": 223.64, "uptime_pct": 98.324, "timestamp": 20250310 },
  { "region": "emea", "service": "recommendations", "latency_ms": 213.84, "uptime_pct": 97.767, "timestamp": 20250311 },
  { "region": "emea", "service": "analytics", "latency_ms": 174.69, "uptime_pct": 97.344, "timestamp": 20250312 },
  { "region": "amer", "service": "analytics", "latency_ms": 160.93, "uptime_pct": 97.477, "timestamp": 20250301 },
  { "region": "amer", "service": "payments", "latency_ms": 184.58, "uptime_pct": 99.075, "timestamp": 20250302 },
  { "region": "amer", "service": "analytics", "latency_ms": 154.57, "uptime_pct": 97.638, "timestamp": 20250303 },
  { "region": "amer", "service": "recommendations", "latency_ms": 116.86, "uptime_pct": 98.826, "timestamp": 20250304 },
  { "region": "amer", "service": "recommendations", "latency_ms": 174.1, "uptime_pct": 98.404, "timestamp": 20250305 },
  { "region": "amer", "service": "catalog", "latency_ms": 128.72, "uptime_pct": 97.492, "timestamp": 20250306 },
  { "region": "amer", "service": "analytics", "latency_ms": 148.4, "uptime_pct": 98.434, "timestamp": 20250307 },
  { "region": "amer", "service": "checkout", "latency_ms": 220.05, "uptime_pct": 97.918, "timestamp": 20250308 },
  { "region": "amer", "service": "analytics", "latency_ms": 120.5, "uptime_pct": 97.282, "timestamp": 20250309 },
  { "region": "amer", "service": "checkout", "latency_ms": 233, "uptime_pct": 99.271, "timestamp": 20250310 },
  { "region": "amer", "service": "analytics", "latency_ms": 166.58, "uptime_pct": 98.71, "timestamp": 20250311 },
  { "region": "amer", "service": "catalog", "latency_ms": 211.24, "uptime_pct": 97.827, "timestamp": 20250312 }
]
"""

# Load the string data into a pandas DataFrame
try:
    df = pd.read_json(io.StringIO(json_data_string))
except Exception as e:
    df = pd.DataFrame()

# Define the request body structure
class LatencyQuery(BaseModel):
    regions: List[str]
    threshold_ms: int = Field(..., gt=0)
# Add this to your api/index.py file

@app.get("/")
def read_root():
    return {"message": "API is running. POST to /api/metrics to get data."}
# Define the main POST endpoint
@app.post("/api/metrics")
async def get_latency_metrics(query: LatencyQuery):
    results = {}
    if df.empty:
        return {"error": "Telemetry data not available."}

    for region in query.regions:
        region_df = df[df['region'] == region]

        if region_df.empty:
            continue

        # Calculate metrics using pandas
        avg_latency = region_df['latency_ms'].mean()
        p95_latency = region_df['latency_ms'].quantile(0.95)
        avg_uptime = region_df['uptime_pct'].mean()
        breaches = int((region_df['latency_ms'] > query.threshold_ms).sum())

        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 3), # Kept higher precision for percentage
            "breaches": breaches
        }

    return results
