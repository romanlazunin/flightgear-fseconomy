import os
import urllib.parse
import requests

HOST = "https://server.fseconomy.net/fsagentFSX?"

USER = os.getenv("FSE_USER")
PASSWORD = os.getenv("FSE_PASSWORD")

if PASSWORD:
    PASSWORD = urllib.parse.quote(PASSWORD)

ACTION = "arrive"

flight_time = "1620"  # seconds
lat = "-3.89958546582"
lon = "141.186346745107"
lat_lon = "&lat=" + lat + "&lon=" + lon
# fuel
central = "0.0"
left_main = "99.0"
left_aux = "0.0"
left_et = "0.0"
tanks_left_url = "&lm=" + left_main + "&la=" + left_aux + "&let=" + left_et

right_main = "99.0"
right_aux = "0.0"
right_tip = "0.0"

c2 = "0.0"
c3 = "0.0"
x1 = "0.0"
x2 = "0.0"

fuel_url = (f"&c={central}{tanks_left_url}&rm={right_main}&ra={right_aux}"
            f"&rt={right_tip}&c2={c2}&c3={c3}&x1={x1}&x2={x2}")

engineStr = "&mixture1=0&heat1=0&time1=" + flight_time

action_url = (f"&action={ACTION}&rentalTime={flight_time}"
              f"{lat_lon}{fuel_url}{engineStr}")

url = f"{HOST}user={USER}&pass={PASSWORD}{action_url}"

try:
    response = requests.get(url, timeout=10)  # 10 seconds timeout
    response.raise_for_status()  # Check for any HTTP errors
except requests.exceptions.Timeout:
    print("The request timed out")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
else:
    print("Response Status:", response.status_code)
    print(response.text)
