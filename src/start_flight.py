import sys
import os
import requests
import urllib.parse

from datetime import datetime

HOST = "https://server.fseconomy.net/fsagentFSX?"

USER = os.getenv("FSE_USER")
PASSWORD = os.getenv("FSE_PASSWORD")

if PASSWORD:
    PASSWORD = urllib.parse.quote(PASSWORD)

ACTION = "startFlight"

# Usage example:
# python start_flight.py "-5.12928" "141.637" "Aero Vodochody L-39"


def main():
    if len(sys.argv) < 4:
        print("Usage: python start_flight.py <latitude> <longitude> <aircraft>")
        sys.exit(1)

    lat, lon, aircraft = sys.argv[1:4]

    aircraft = urllib.parse.quote(aircraft)

    url = f"{HOST}user={USER}&pass={PASSWORD}&action={ACTION}&lat={lat}&lon={lon}&aircraft={aircraft}"

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

        # Generate filename with current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        directory = "responses"
        os.makedirs(directory, exist_ok=True)
        filename = os.path.join(directory, f"response_{timestamp}.txt")

        # Save response to file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"Response saved to {filename}")

if __name__ == "__main__":
    main()
