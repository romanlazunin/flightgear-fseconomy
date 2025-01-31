import telnetlib
import re

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


# Example usage
if __name__ == "__main__":
    client = FlightGearTelnetClient(HOST, PORT)
    try:
        client.connect()
        latitude = client.read_property("/position/latitude-deg")
        longitude = client.read_property("/position/longitude-deg")
        time = client.read_property("/sim/time/elapsed-sec")
        description = client.read_property("sim/description")

        client.tn.write(b"ls /consumables/fuel/\n")
        response = client.tn.read_until(b"\n", timeout=2).decode()

        # Count tanks based on response
        tanks = [line for line in response.splitlines() if "tank" in line]
        num_tanks = len(tanks)

        print(f"Tanks count: {num_tanks}")

        # tanks = {}
        # for i in range(8):
        #     raw_value = client.read_property(f"/consumables/fuel/tank[{i}]/level-gal_us")
        #     tanks[i] = raw_value.split('=')[1].strip().replace("'", "").split()[0]

        # for i, level in tanks.items():
        #     print(f"Tank {i}: {level}")

        # print(" ".join(str(level) for level in tanks.values()))

        time = time.split('=')[1].strip().replace("'", "").split()[0]
        latitude = latitude.split('=')[1].strip().replace("'", "").split()[0]
        longitude = longitude.split('=')[1].strip().replace("'", "").split()[0]
        description = description.split('=')[1].strip().split("(")[0].strip()
        print(f"Time: {time}")

        print(f'py .\\start_flight.py {latitude} {longitude} {description}')

        callsign = client.read_property("/sim/multiplay/callsign").split('=')[1].strip()
        print(f"Callsign: {callsign}")

        client.write_property("/sim/multiplay/callsign", "")

        callsign = client.read_property("/sim/multiplay/callsign").split('=')[1].strip()
        print(f"Callsign: {callsign}")


        # print("Listing properties:")
        # properties = client.list_properties()
        # for prop in properties:
        #     print(prop)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
