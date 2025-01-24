import os
import urllib.parse
import requests

HOST = "https://server.fseconomy.net/fsagentFSX?"

USER = os.getenv("FSE_USER")
PASSWORD = os.getenv("FSE_PASSWORD")

if PASSWORD:
    PASSWORD = urllib.parse.quote(PASSWORD)

ACTION = "cancel"

url = f"{HOST}user={USER}&pass={PASSWORD}&action={ACTION}"

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
