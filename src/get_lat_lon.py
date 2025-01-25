import telnetlib
import re

HOST = "localhost"
PORT = 5401  # Default Telnet port for FlightGear

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
        print(f"Latitude: {latitude}")
        longitude = client.read_property("/position/longitude-deg")
        print(f"Longitude: {longitude}")

        # print("Listing properties:")
        # properties = client.list_properties()
        # for prop in properties:
        #     print(prop)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
