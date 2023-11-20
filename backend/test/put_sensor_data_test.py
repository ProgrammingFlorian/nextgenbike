from datetime import datetime, timedelta

import requests

dev = True

if dev:
    host = "localhost:5000"
else:
    host = "104.248.148.208"

now = datetime.now()
now1 = now.strftime("%Y-%m-%dT%H:%M:%S.000000+00:00")
now2 = (now - timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S.000000+00:00")
now3 = (now - timedelta(seconds=2)).strftime("%Y-%m-%dT%H:%M:%S.000000+00:00")
now4 = (now - timedelta(seconds=3)).strftime("%Y-%m-%dT%H:%M:%S.000000+00:00")

print(now)

result = requests.put(f"http://{host}/sensor", json=({"time":[now1, now2, now3, now4], "trip_id": 11, "vibration":[1.0, 0.5, 2.0, 5.0], "latitude":[-5, -4.9, -4.8, -4.7], "longitude":[1, 1.9, 2.8, 3.7], "acceleration_x":[1, 0, 5, 3], "acceleration_y":[3, 8, 4, 1], "acceleration_z":[6, 3, 6, 2], "gyroscope_x":[3, 2, 5, 3], "gyroscope_y":[7, 0, 2, 5], "gyroscope_z":[9, 1, 0, 8]}))

print(result.content)
