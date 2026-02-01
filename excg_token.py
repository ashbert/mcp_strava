
import requests
import os
import json
from dotenv import load_dotenv
import os

#https://www.strava.com/oauth/authorize?client_id=122228&response_type=code&redirect_uri=http://localhost/exchange_token&scope=read,activity:read_all&approval_prompt=force
# copy code and enter below. then run this script again. token.json should update.


load_dotenv()
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
code = "d183c7c3cab16763fb10ddebd69753e825bff4b3"
print(client_id, client_secret, code)
response = requests.post("https://www.strava.com/api/v3/oauth/token", data={
    "client_id": client_id,
    "client_secret": client_secret,
    "code": code,
    "grant_type": "authorization_code"
})

data = response.json()

with open("token.json", "w") as f:
    json.dump(data, f, indent=2)

print(data)
print("Token saved.")
