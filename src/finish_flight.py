"""
This module performs FSEconomy API finish flight procedure
"""

import os
import urllib.parse
import sys
import requests

HOST = "https://server.fseconomy.net/fsagentFSX?"

USER = os.getenv("FSE_USER")
PASSWORD = os.getenv("FSE_PASSWORD")

if PASSWORD:
    PASSWORD = urllib.parse.quote(PASSWORD)

ACTION = "arrive"

flight_time, lat, lon, central, left_main, left_aux, left_tip, right_main, right_aux, right_tip, c2, c3, x1, x2 = sys.argv[1:15]
# python finish_flight.py 900 -77.85042876808599 166.4606189903415 0.0 100.5 0.0 0.0 100.5 0.0 0.0 0.0 0.0 0.0 0.0

lat_lon = "&lat=" + lat + "&lon=" + lon
# fuel
tanks_left_url = "&lm=" + left_main + "&la=" + left_aux + "&let=" + left_tip

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
