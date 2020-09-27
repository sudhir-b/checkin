# if you change the name of this file, you must update
# the sudoers file so that this script can continue
# to be run as sudo without requiring a password
nmap -sn $@ | egrep -o '([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
