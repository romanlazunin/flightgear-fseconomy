import telnetlib
import re
import sys
import urllib.parse

HOST = "localhost"
PORT = 5401
CRLF = '\r\n'

class FlightGearTelnetClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.tn = None
        self.prompt = [re.compile(rb'/[^>]*> ')]
        self.timeout = 5

    def connect(self):
        try:
            self.tn = telnetlib.Telnet(self.host, self.port, timeout=self.timeout)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port} - {e}")

    def _putcmd(self, cmd):
        if not self.tn:
            raise ConnectionError("Not connected to the server")
        cmd = cmd + CRLF
        self.tn.write(cmd.encode('utf-8'))

    def _getresp(self):
        if not self.tn:
            raise ConnectionError("Not connected to the server")
        response = b""
        while True:
            index, match, data = self.tn.expect(self.prompt, self.timeout)
            response += data
            if index == 0:  # End of response detected
                break
            if index == -1:
                raise TimeoutError("Response timeout exceeded")
        # Decode and return response without the prompt
        return response.decode("utf-8").split("\n")[:-1]

    def read_property(self, property_name):
        try:
            self._putcmd(f"get {property_name}")
            response = self.tn.read_until(b"\n", timeout=self.timeout).decode("utf-8").strip()
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to read property '{property_name}' - {e}")

    def write_property(self, property_name, value):
        try:
            self._putcmd(f"set {property_name} {value}")
        except Exception as e:
            raise RuntimeError(f"Failed to write property '{property_name}' - {e}")

    def list_properties(self):
        try:
            self._putcmd("ls")
            return self._getresp()
        except Exception as e:
            raise RuntimeError(f"Failed to list properties - {e}")

    def disconnect(self):
        if self.tn:
            self._putcmd("quit")
            self.tn.close()
            self.tn = None

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: python update_flight.py '<callsign>' <from> <to>")
        sys.exit(1)

    callsign, icao_from, icao_to = sys.argv[1:4]
    print(callsign, icao_from, icao_to)
    callsign = urllib.parse.quote(callsign)

    client = FlightGearTelnetClient(HOST, PORT)
    try:
        client.connect()

        def read_property(client, property_path):
            raw_value = client.read_property(property_path)
            cleaned_value = raw_value.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            print(f"{property_path}: {cleaned_value}")
            return cleaned_value

        fuel_gal_us = read_property(client, "/consumables/fuel/total-fuel-gal_us")
        old_callsign = read_property(client, "/sim/multiplay/callsign")
        tank = read_property(client, "/consumables/fuel/tank/level-gal_us")

        client.write_property("/sim/multiplay/callsign", callsign)

        callsign = read_property(client, "/sim/multiplay/callsign")

        # client.write_property("/autopilot/route-manager/departure/airport", icao_from)
        # read_property(client, "/autopilot/route-manager/departure/airport")

        # client.write_property("/autopilot/route-manager/destination/airport", icao_to)
        # read_property(client, "/autopilot/route-manager/destination/airport")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
