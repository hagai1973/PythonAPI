import time

import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MY_LAT = 32.085300  # Your latitude
MY_LONG = 34.781769  # Your longitude

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
    "tzid": "Asia/Jerusalem"
}

MY_EMAIL = "hagai1973@gmail.com"
PASSWORD = "cpfuivrepmarvlac"


def send_mail(message_text):
    """
    Sends an email with the provided message text

    :param message_text: The content of the email
    """
    # Email account details
    my_email = MY_EMAIL
    password = PASSWORD
    recipient = "hagai.tregerman@gmail.com"  # Replace with recipient email

    # Create message
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = recipient
    msg['Subject'] = "🛰️ Look up! 👆 The ISS is above you in the night sky! ✨🌃"

    # Attach message text
    msg.attach(MIMEText(message_text, 'plain'))

    try:
        # Connect to SMTP server (Gmail example)
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # Secure the connection
            connection.login(user=my_email, password=password)
            connection.send_message(msg)
        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")


def get_iss_position():
    """
    Gets the current ISS position from the API
    Returns a tuple of (latitude, longitude)
    """
    response = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
    response.raise_for_status()
    iss_latitude = response.json()["latitude"]
    iss_longitude = response.json()["longitude"]
    iss_position = (iss_latitude, iss_longitude)
    return iss_position


def is_iss_overhead(iss_position):
    """
    Checks if the ISS is close to the user's position.
    Returns True if ISS is within ±5 degrees of user's position.

    :param iss_position: Tuple containing (latitude, longitude) of the ISS
    :return: Boolean indicating if ISS is overhead
    """
    iss_lat, iss_lng = iss_position
    my_lat1, my_long1 = MY_LAT, MY_LONG
    # Check if ISS is within ±5 degrees of user's position
    lat_close = my_lat1 - 5 <= iss_lat <= MY_LAT + 5
    lng_close = my_long1 - 5 <= iss_lng <= MY_LONG + 5

    return lat_close and lng_close


response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


def check_iss_position():
    # Get actual current time (not hardcoded)
    time_now = datetime.now()
    current_hour = time_now.hour
    # current_hour = 22

    # Get current ISS position
    current_iss_position = get_iss_position()
    print(f"ISS current position: {current_iss_position}")

    # Check conditions
    is_overhead = is_iss_overhead(current_iss_position)
    is_dark = current_hour >= sunset or current_hour < sunrise

    if is_overhead and is_dark:
        message = "🛰️ Look up! 👆 The ISS is above you in the night sky! ✨🌃"
        print(message)
        send_mail(message)
    else:
        if not is_overhead:
            print("ISS is not overhead right now.")
        if not is_dark:
            print("It's daytime, ISS might not be visible.")


# Main loop to check every minute
while True:
    print(f"\nChecking ISS position at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"the sunset and sunrise are: {sunset} and {sunrise}")
    print("your position is:" f"{MY_LAT}, {MY_LONG}")
    check_iss_position()
    print("Waiting 60 seconds until next check...")
    time.sleep(60)  # Sleep for 60 seconds before next check
