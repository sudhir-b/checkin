import subprocess
import os

# if you change the name of this script, you must
# alter the sudoers file so that the script can be
# run as sudo without having to provide a password
GET_MAC_ADDRESS_SCRIPT = "get_MAC_address.sh"


def get_mac_address(ip_addr):
    path = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(path, GET_MAC_ADDRESS_SCRIPT)

    # The script must be run as sudo for nmap to work properly
    result = subprocess.run(["sudo", script_path, ip_addr], stdout=subprocess.PIPE)
    addrs = result.stdout.decode("utf-8").split("\n")

    return [addr.strip() for addr in addrs if addr.strip()]
