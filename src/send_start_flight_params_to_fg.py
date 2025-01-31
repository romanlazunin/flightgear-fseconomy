import telnetlib

FG_TELNET_HOST = "127.0.0.1"
FG_TELNET_PORT = 5401

def write_property(property_name, value):
    try:
        with telnetlib.Telnet(FG_TELNET_HOST, FG_TELNET_PORT) as telnet:
            command = f"set {property_name} {value}\r\n"
            telnet.write(command.encode('utf-8'))

            response = telnet.read_very_eager().decode('utf-8')
            print(f"Response: {response}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    property_name = "sim/multiplay/callsign"
    value = "DQ-QSO"
    write_property(property_name, value)
