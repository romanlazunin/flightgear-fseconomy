# FlightGear FSEconomy Integration

Experimental integration between the open-source FlightGear flight simulator and FSEconomy.

This project provides small Python scripts for manually interacting with the FSEconomy API and reading or updating selected FlightGear properties. It is primarily intended as a lightweight toolkit for use while flying in FlightGear, but the scripts may also be useful for experimentation with other simulators.

## Features

- Start an FSEconomy flight at the aircraft's current latitude and longitude.
- Finish an FSEconomy flight with fuel and flight-time data.
- Cancel an active FSEconomy flight.
- Check the FSEconomy account status.
- Read FlightGear position, fuel, time, and aircraft properties.
- Send selected property changes to FlightGear through its telnet interface.

## Requirements

- Python 3
- A valid FSEconomy account
- Access to the FSEconomy API
- FlightGear with its telnet server enabled
- The following Python packages:

```bash
python3 -m pip install -r requirements.txt
```

## Configuration

Set your FSEconomy credentials before running the API scripts:

```bash
export FSE_USER="your-fseconomy-username"
export FSE_PASSWORD="your-fseconomy-password"
```

On Windows PowerShell, use:

```powershell
$env:FSE_USER = "your-fseconomy-username"
$env:FSE_PASSWORD = "your-fseconomy-password"
```

The scripts read these variables from the environment. Keep the password out of source control.

## Usage

The scripts are located in the `src` directory. Run them from the project root or include the correct relative path.

### Check the account

```bash
python3 src/account_check.py
```

### Start a flight

```bash
python3 src/start_flight.py "<latitude>" "<longitude>" "<aircraft name>"
```

Example:

```bash
python3 src/start_flight.py "-5.12928" "141.637" "Aero Vodochody L-39"
```

The response is printed to the terminal and saved in the `src/responses` directory with a timestamped filename.

### Finish a flight

```bash
python3 src/finish_flight.py <flight_time> <latitude> <longitude> <central> <left_main> <left_aux> <left_tip> <right_main> <right_aux> <right_tip> <c2> <c3> <x1> <x2>
```

The arguments are passed directly to the FSEconomy API. Values should be supplied in the units expected by the service and should correspond to your aircraft's actual fuel and flight data.

### Cancel a flight

```bash
python3 src/cancel_flight.py
```

### Read FlightGear data

```bash
python3 src/get_lat_lon.py
```

This script connects to FlightGear on `localhost:5501` and prints the aircraft's latitude, longitude, elapsed time, call sign, description, and fuel information.

### Write a FlightGear property

```bash
python3 src/send_start_flight_params_to_fg.py
```

The script currently demonstrates how to set the multiplayer call sign. Update the `property_name` and `value` variables in the script before using it for another property.

### Update the FlightGear call sign and route data

```bash
python3 src/update_sim.py "<callsign>" "<departure-airport-icao>" "<destination-airport-icao>"
```

The script attempts to connect to FlightGear on `localhost:5401`. The departure and destination airport arguments are currently commented out, so the script only updates the call sign by default.

## FlightGear setup

For the telnet scripts to work, enable the FlightGear telnet server and use the appropriate port:

- `get_lat_lon.py` connects to `localhost:5501`.
- `update_sim.py` connects to `localhost:5401`.

The exact port configuration depends on the FlightGear launch settings. Confirm the configured telnet port before running a script.

## Important limitations

- This project does not provide a complete GUI, flight workflow, or automatic synchronization with FSEconomy.
- The scripts perform direct HTTP requests and may fail if the FSEconomy API or credentials are unavailable.
- Some scripts have minimal input validation and rely on the user to provide correct data.
- The license and FSEconomy terms of service still apply to any flight, account, or aircraft data handled by these scripts.
- The scripts write responses to the local filesystem; review the generated response files before sharing them.

## Project state

This is an experimental project. The scripts are intentionally small and may change as the integration evolves.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
