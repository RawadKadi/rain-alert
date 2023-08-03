import os

import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
API_KEY="726e1255dc128d586bd8ad1492ab320d"
latitude=33.694569
longitude=35.502651

account_sid = "AC1b7e23b72114253fab53f69556f64ca8"
auth_token = "f4045403ea65505fae293d0bcfc826bb"



parameters={
    "lon": longitude,
    "lat": latitude,
    "appid": API_KEY,
    "exclude":"current,minutely,daily"
}

response=requests.get(url="https://api.openweathermap.org/data/2.5/onecall",params=parameters)
response.raise_for_status()
weather_id=[]
will_rain=False
for i in range (1,13):
    weather_data=response.json()["hourly"][i]["weather"][0]["id"]
    if weather_data<700:
        will_rain=True
    weather_id.append(weather_data)
if will_rain:
        proxy_client=TwilioHttpClient()
        proxy_client.session.proxies={'https':os.environ['https_proxy']}
        client = Client(account_sid, auth_token,http_client=proxy_client)
        message = client.messages.create(
            body="It is going to rain today. Remember to bring an umbrella",
            from_="+19108385851",
            to='+96178864568'
        )
        print(message.status)
else:
    proxy_client=TwilioHttpClient()
    proxy_client.session.proxies={'https':os.environ['https_proxy']}
    client = Client(account_sid, auth_token,http_client=proxy_client)
    message = client.messages.create(
            body="It is not going to rain today. Remember not to bring an umbrella",
            from_="+19108385851",
            to='+96178864568'
        )
    print(message.status)
