# IP freely ip scanner

A simple Python script that converts CIDR blocks into IP ranges and pings every IP address in that range to determine if hosts are reachable.

## Features
- Converts IP addresses between **dotted-decimal** and **32-bit integer** formats.
- Calculates **start and end IP addresses from a CIDR block**.
- Performs a **ping scan** across the full IP range.
- Displays whether each host is **UP or DOWN** and shows **ping latency (ms)** if available.

## Requirements
- Python 3
- Linux system with the `ping` command available

## Functions

### `ip_to_int(ip_address)`
Converts a dotted IPv4 address (e.g., `192.168.1.1`) into a 32-bit integer.

### `int_to_ip(ip_int)`
Converts a 32-bit integer back into a dotted IPv4 address.

### `get_ip_range_from_cidr(cidr)`
Takes a CIDR block (e.g., `192.168.1.0/24`) and returns:
- Start IP (network address)
- End IP (broadcast address)

Example:
```python
get_ip_range_from_cidr("192.168.1.0/24")
# Returns: ("192.168.1.0", "192.168.1.255")
```

### `ping_ip_range(start_ip, end_ip)`
Pings every IP address between the start and end IP (inclusive) and prints results.

Output format:
```
[UP]   192.168.1.1 - 0.45 ms
[DOWN] 192.168.1.2 - unreachable
```

## Example Usage

```python
cidr = "192.168.1.0/24"

start_ip, end_ip = get_ip_range_from_cidr(cidr)
ping_ip_range(start_ip, end_ip)
```

## Notes
- Designed for **Linux** (`ping -c 1 -W 1`).
- Large CIDR blocks may take longer to scan because the script runs sequential pings.
- Intended for educational and network troubleshooting use.