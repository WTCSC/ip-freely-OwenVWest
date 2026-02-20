import subprocess as subp
import re

# Converts a dotted-decimal IP address string to a 32-bit integer
def ip_to_int(ip_address):
    
    parts = list(map(int, ip_address.split('.')))
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
# Converts a 32-bit integer to its dotted-decimal IP address string.
def int_to_ip(ip_int):
    
    return f"{ (ip_int >> 24) & 255 }.{ (ip_int >> 16) & 255 }.{ (ip_int >> 8) & 255 }.{ ip_int & 255 }"


def get_ip_range_from_cidr(cidr):
    """Calculates the start and end IP addresses for a given CIDR block."""
    try:
        ip_str, prefix_len_str = cidr.split('/')
        prefix_len = int(prefix_len_str)
        ip_int = ip_to_int(ip_str)

        # Calculate the network mask
        # A mask has 'prefix_len' leading 1s and '32 - prefix_len' trailing 0s
        net_mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF

        # Calculate the network address (start of range) using bitwise AND
        network_address_int = ip_int & net_mask

        # Calculate the broadcast address (end of range) using bitwise OR with the host mask
        # The host mask is the inverse of the net mask
        host_mask = ~net_mask & 0xFFFFFFFF
        broadcast_address_int = network_address_int | host_mask

        # Convert back to IP strings
        start_ip = int_to_ip(network_address_int)
        end_ip = int_to_ip(broadcast_address_int)

        return start_ip, end_ip

    except ValueError:
        return "Invalid CIDR notation or IP address format"
    
# ...existing code...
def ping_ip_range(start_ip, end_ip):
    """
    Pings a range of IP addresses from start_ip to end_ip (inclusive) on Linux.
    Prints whether each address is up or down and the ping time in ms.
    """
    start_int = ip_to_int(start_ip)
    end_int = ip_to_int(end_ip)
    if start_int > end_int:
        start_int, end_int = end_int, start_int

    print(f"Starting ping scan from {start_ip} to {end_ip}...")

    for ip_int in range(start_int, end_int + 1):
        ip_address = int_to_ip(ip_int)
        command = ["ping", "-c", "1", "-W", "1", ip_address]  # Linux: 1 packet, 1s wait

        try:
            result = subp.run(command, capture_output=True, text=True, timeout=2)

            if result.returncode == 0:
                m = re.search(r'time=([\d\.]+)\s*ms', result.stdout)
                if m:
                    print(f"[UP]   {ip_address} - {m.group(1)} ms")
                else:
                    print(f"[UP]   {ip_address} - reply received")
            else:
                print(f"[DOWN] {ip_address} - unreachable")
        except subp.TimeoutExpired:
            print(f"[DOWN] {ip_address} - timeout")
        except Exception as e:
            print(f"[ERROR] {ip_address} - {e}")
