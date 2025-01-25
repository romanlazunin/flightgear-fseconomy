import telnetlib

# FlightGear Telnet settings
TELNET_HOST = "127.0.0.1"
TELNET_PORT = 5401

def write_property(property_name, value):
    try:
        # Connect to FlightGear Telnet interface
        with telnetlib.Telnet(TELNET_HOST, TELNET_PORT) as telnet:
            # Send the command to set the property
            command = f"set {property_name} {value}\n"
            telnet.write(command.encode('ascii'))

            # Optional: Read and print the response from FlightGear
            response = telnet.read_very_eager().decode('ascii')
            print(f"Response: {response}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    property_name = "/controls/engines/engine[0]/throttle"
    value = 0.5  # Set throttle to 50%
    write_property(property_name, value)
