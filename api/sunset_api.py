import requests
from datetime import datetime


parameters = {
    "lat": 32.085300,
    "lng": 34.781769,
    "tzid": "Asia/Jerusalem",
    "formatted": 0  # Get ISO format

}
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()  # Raise an error for bad responses
print(response
      .json())  # Print the entire

data = response.json()

# Parse the ISO format time strings to datetime objects
sunrise_time = datetime.fromisoformat(data["results"]["sunrise"])
sunset_time = datetime.fromisoformat(data["results"]["sunset"])

# Calculate the difference
daylight_duration = sunset_time - sunrise_time

# Format the result
hours = daylight_duration.seconds // 3600
minutes = (daylight_duration.seconds % 3600) // 60

print(f"Sunrise: {sunrise_time}")
print(f"Sunset: {sunset_time}")
print(f"Daylight duration: {hours} hours and {minutes} minutes")