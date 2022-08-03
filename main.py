import os
from twilio.rest import Client
import requests

twilio_verification = "enter you verification"
API_key = "enter your API"
website_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = "enter your account sid"
auth_token = "enter your auth token"
twilio_phone = "enter your twilio generated #"
MY_LAT = -37.840935
MY_LON = 144.946457

# Parameters for your API
parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": API_key,
    "exclude": "current,daily,minutely",
}

# Sending a call to the API, asking for specific forecast variables
response = requests.get(website_endpoint, params=parameters)
response.raise_for_status()
data = response.json()
raining_half_day_data = data["hourly"][:12]
sunset_data = data["hourly"][4:7]
raining = False
fire_sunset = False

# Looping through the received data to find a wanted attribute
for hour_weather in raining_half_day_data:
    weather_data = hour_weather['weather'][0]['id']
    if weather_data < 700:
        raining = True

# Once satisfied the specification that points out rain occurrence, send an SMS
if raining:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='Bring an ☔',
        from_=twilio_phone,
        to='enter the recipient #'
    )

    print(message.status)

