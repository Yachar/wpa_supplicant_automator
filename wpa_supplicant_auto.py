#!/usr/bin/env python3

import getpass
import subprocess as sp
import time


COMMAND = ['wpa_supplicant -B -i wlp1s0b1 -c /etc/wpa_supplicant.conf']

mypass = getpass.getpass('This needs administrator privileges: ')
pass_in_bytes = bytes(mypass, 'utf-8')

proc = sp.Popen(['su', '-c'] + COMMAND, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
proc.stdin.write(pass_in_bytes)
o, e = proc.communicate()

if proc.returncode:
    print('\nconnection failed \n')
else:
    print('\nsuccess \n')

print(o.decode())
print(e.decode())

#Waiting for wpa_supplicant to establish the connection:
print("waiting for wpa_supplicant...")
time.sleep(3)

#DHCPCD
COMMAND2 = ['dhcpcd wlp1s0b1']

proc2 = sp.Popen(['su', '-c'] + COMMAND2, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
proc2.stdin.write(pass_in_bytes)
o2, e2 = proc2.communicate()

if proc.returncode:
    print('\nDHCP failed establishing the connection... \n')
else:
    print('\nDHCP: successful \n')

print(o2.decode())
#print(e2.decode())

