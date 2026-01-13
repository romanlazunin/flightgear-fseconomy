import asyncio
import telnetlib3
import re

HOST = "localhost"
# PORT = 5401
PORT = 5501

CRLF = '\r\n'


class FlightGearTelnetClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.prompt = [re.compile(rb'/[^>]*> ')]
        self.timeout = 10

    def connect(self):
        raise RuntimeError("connect() is async; use 'await client.connect()' or run via asyncio")

    async def aconnect(self):
        try:
            self.reader, self.writer = await telnetlib3.open_connection(self.host, self.port)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port} - {e}")

    async def _putcmd(self, cmd):
        if not self.writer:
            raise ConnectionError("Not connected to the server")
        cmd = cmd + CRLF
        # Try writing text first; if writer expects bytes, fall back to encoded bytes
        try:
            self.writer.write(cmd)
        except TypeError:
            self.writer.write(cmd.encode("utf-8"))
        try:
            await self.writer.drain()
        except Exception:
            # Some writer implementations may not support drain
            await asyncio.sleep(0)

    async def _getresp(self):
        if not self.reader:
            raise ConnectionError("Not connected to the server")
        # Read up to the next newline; callers may call repeatedly if needed
        # Try bytes delimiter first, fall back to text delimiter if needed
        try:
            data = await self.reader.readuntil(b"\n")
        except TypeError:
            data = await self.reader.readuntil("\n")

        if isinstance(data, bytes):
            text = data.decode("utf-8", errors="replace")
        else:
            text = data
        return text.split("\n")[:-1]

    async def read_property(self, property_name):
        try:
            await self._putcmd(f"get {property_name}")
            try:
                response = await self.reader.readuntil(b"\n")
            except TypeError:
                response = await self.reader.readuntil("\n")

            if isinstance(response, bytes):
                return response.decode("utf-8", errors="replace").strip()
            return response.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to read property '{property_name}' - {e}")

    async def write_property(self, property_name, value):
        try:
            await self._putcmd(f"set {property_name} {value}")
        except Exception as e:
            raise RuntimeError(f"Failed to write property '{property_name}' - {e}")

    async def list_properties(self):
        try:
            await self._putcmd("ls")
            return await self._getresp()
        except Exception as e:
            raise RuntimeError(f"Failed to list properties - {e}")

    async def disconnect(self):
        if self.writer:
            try:
                await self._putcmd("quit")
            except Exception:
                pass
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except Exception:
                pass
            self.reader = None
            self.writer = None


# Example usage
if __name__ == "__main__":
    async def main():
        client = FlightGearTelnetClient(HOST, PORT)
        try:
            await client.aconnect()

            # print("Listing properties:")
            # properties = await client.list_properties()
            # for prop in properties:
            #     print(prop)

            latitude = await client.read_property("/position/latitude-deg")
            longitude = await client.read_property("/position/longitude-deg")
            time = await client.read_property("/sim/time/elapsed-sec")
            description = await client.read_property("sim/description")
            callsign = await client.read_property("/sim/multiplay/callsign")

            fuel_gal_us = await client.read_property("/consumables/fuel/total-fuel-gal_us")
            tank = await client.read_property("/consumables/fuel/tank/level-gal_us")
            tank_name = await client.read_property("/consumables/fuel/tank/name")
            tank1 = await client.read_property("/consumables/fuel/tank[1]/level-gal_us")
            tank1_name = await client.read_property("/consumables/fuel/tank[1]/name")
            tank2 = await client.read_property("/consumables/fuel/tank[2]/level-gal_us")
            tank2_name = await client.read_property("/consumables/fuel/tank[2]/name")
            tank3 = await client.read_property("/consumables/fuel/tank[3]/level-gal_us")
            tank3_name = await client.read_property("/consumables/fuel/tank[3]/name")

            clean_latitude = latitude.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_longitude = longitude.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_description = description.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_callsign = callsign.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_time = time.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_fuel = fuel_gal_us.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_tank = tank.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_tank_name = tank_name.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_tank1 = tank1.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_tank1_name = tank1_name.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_tank2 = tank2.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_tank2_name = tank2_name.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_tank3 = tank3.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            clean_tank3_name = tank3_name.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            
            print(f"Latitude: {clean_latitude}")
            print(f"Longitude: {clean_longitude}")
            print(f"Time elapsed: {clean_time}")
            print(f"Description: {clean_description}")
            print(f"Callsign: {clean_callsign}")
            print(f"Total Fuel (gal US): {clean_fuel}")
            print(f"Tank 0 Level (gal US), {clean_tank_name}: {clean_tank}")
            print(f"Tank 1 Level (gal US), {clean_tank1_name}: {clean_tank1}")
            print(f"Tank 2 Level (gal US), {clean_tank2_name}: {clean_tank2}")
            print(f"Tank 3 Level (gal US), {clean_tank3_name}: {clean_tank3}")
            print("")

            print(f"py .\\start_flight.py {clean_latitude} {clean_longitude} '{clean_description}'")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await client.disconnect()

        async def read_property(client, property_path):
            raw_value = client.read_property(property_path)
            cleaned_value = raw_value.replace("/> ", "").split('=')[1].split("(")[0].replace("'", "").strip()
            print(f"{property_path}: {cleaned_value}")
        
            return cleaned_value

        # 

        

        # client._putcmd("ls /consumables")
        # tanks = client._getresp()
        # for tank in tanks:
        #     print(tank)

        # client.tn.write(b"ls /consumables/fuel\n")
        # response = client.tn.read_until(b"\n", timeout=4).decode()
        # print(response)

        # print("Listing properties:")
        # properties = client.list_properties()
        # for prop in properties:
        #     print(prop)

        # Count tanks based on response
        # tanks = [line for line in response.splitlines() if "tank" in line]
        # num_tanks = len(tanks)

        # print(f"Tanks count: {num_tanks}")

        # tanks = {}
        # for i in range(8):
        #     raw_value = client.read_property(f"/consumables/fuel/tank[{i}]/level-gal_us")
        #     tanks[i] = raw_value.split('=')[1].strip().replace("'", "").split()[0]
        #     print(f"Tank {i}: {level}")

        # for i, level in tanks.items():
        #     print(f"Tank {i}: {tanks[i]}")

        # print(" ".join(str(level) for level in tanks.values()))

        # time = time.split('=')[1].strip().replace("'", "").split()[0]
        # latitude = latitude.split('=')[1].strip().replace("'", "").split()[0]
        # longitude = longitude.split('=')[1].strip().replace("'", "").split()[0]
        # description = description.split('=')[1].strip().split("(")[0].replace("'", "").strip()
        # print(f"Time: {time}")

        # print(f"py .\\start_flight.py {latitude} {longitude} '{description}'")
      
    asyncio.run(main())
