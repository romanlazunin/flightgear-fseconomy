import os
import requests
import urllib.parse

HOST = "https://server.fseconomy.net/fsagentFSX?"

USER = os.getenv("FSE_USER")
PASSWORD = os.getenv("FSE_PASSWORD")

if PASSWORD:
    PASSWORD = urllib.parse.quote(PASSWORD)

ACTION = "accountCheck"

url = (f"{HOST}user={USER}&pass={PASSWORD}&action={ACTION}")

try:
    response = requests.get(url)
    print("Response Status:", response.status_code)
    print("Response text:", response.text)

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)