import subprocess
import os

GET_MAC_ADDRESS_SCRIPT = 'get_MAC_address.sh'

def get_mac_address(ip_addr):
    path = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(path, GET_MAC_ADDRESS_SCRIPT)
    result = subprocess.run(['sudo', script_path, ip_addr], stdout=subprocess.PIPE)
    addrs = result.stdout.decode('utf-8').split('\n')

    return [addr.strip() for addr in addrs if addr.strip()]

if __name__ == '__main__':
    result = get_mac_address('192.168.0.0/24')
    print(result)