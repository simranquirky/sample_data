import json
import random
from datetime import datetime, timedelta, timezone

# Output file name
output_file = "slo_metrics_data.json"

# Define IST timezone offset (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

# Convert IST datetime to milliseconds since epoch (UTC-based)
def to_millis_utc(dt_ist):
    dt_utc = dt_ist.astimezone(timezone.utc)
    return int(dt_utc.timestamp() * 1000)

# Current time in IST
now_ist = datetime.now(IST)
start_time_ist = now_ist - timedelta(minutes=5)

data_points = []
hosts = ["db1", "db2"]
mounts = ["/", "/data"]
interval = 10  # every 10 seconds
n_points = int((5 * 60) / interval)

for i in range(n_points):
    ts_ist = start_time_ist + timedelta(seconds=i * interval)
    for host in hosts:
        for mount in mounts:
            value = random.uniform(85.0, 95.0) if i % 7 == 0 else random.uniform(40.0, 60.0)
            point = {
                "__name__": "disk_utilization",
                "__type__": "gauge",
                "host": host,
                "mount": mount,
                "service": "database-server",
                "_timestamp": to_millis_utc(ts_ist),
                "value": round(value, 2)
            }
            data_points.append(point)

# Save to sample.json
with open(output_file, "w") as f:
    json.dump(data_points, f, indent=2)

print(f"✅ Generated '{output_file}' with {len(data_points)} points in IST time window.")
