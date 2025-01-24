import os
import requests
import urllib.parse

host = "https://server.fseconomy.net/fsagentFSX?"

user = os.getenv("FSE_USER")
password = os.getenv("FSE_PASSWORD")
password = urllib.parse.quote(password)

action = "accountCheck"

url = host + "user=" + user + "&pass=" + password + "&action=" + action

try:
    response = requests.get(url)
    print("Response Status:", response.status_code)
    print("Response text:", response.text)

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)