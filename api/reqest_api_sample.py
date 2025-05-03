import requests


response = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
response.raise_for_status()
print(response.status_code)  # 200
print(response.json())  # {'id': 25544, 'name': 'ISS (ZARYA)', ...}
print(response.json()["units"])  # {'velocity': '28,000 km/h', 'altitude': '400 km', ...}
iss_latitude = response.json()["latitude"]
iss_longitude = response.json()["longitude"]
iss_position = (iss_latitude, iss_longitude)
print(iss_position)  # (28.5, 77.5)