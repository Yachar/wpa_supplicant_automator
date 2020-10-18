#!/usr/bin/env python3

import subprocess as sp
from subprocess import Popen as pp
from argparse import ArgumentParser as argp
from sys import argv
from os import getpid
import getpass, time, os
import psutil

#setting arguments
parser = argp()

parser.add_argument("-i", "--interface", dest = "interface", help="your wifi interface ex: 'wlan0'")
parser.add_argument("-s", "--ssid", dest = "ssid", help="SSID / the name of your acess point")
parser.add_argument("-p", "--password", dest = "password", help="wifi password")
parser.add_argument("-l", "--list", dest = "list", help="prints current active SSID", action="store_true")
parser.add_argument("-v", "--verbose", dest = "verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

#handeling list flag
if args.list:
    if args.password:
        print(f'current active SSID: {args.ssid}')
    else:
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as config:
            current_ssid = config.readlines()
            print(current_ssid[1])
    exit()

#inputs comands
envpass = os.environ.get('PW')
#mypass = getpass.getpass('This needs administrator privileges: ')
pass_in_bytes = bytes(envpass, 'utf-8')


def wpa_pass():
    """ if the arguments are satisfied for --password send
    SSID and Password to the wpa_passphrase in order to create a config file for wpa_supplicant. """

    if args.password:
        command_pass = [f"wpa_passphrase {args.ssid} {args.password} > /etc/wpa_supplicant/wpa_supplicant.conf"]
        proc = pp(['su', '-c'] + command_pass, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        try:
            proc.stdin.write(pass_in_bytes)
            o, e = proc.communicate(timeout=15)
        except TimeoutExpired:
            proc.kill()
            o, e = proc.communicate()

        if proc.returncode:
            print('connection failed \n')
        else:
            print('success \n')

        print(o.decode())
        #print("proc", e.decode())
    else:
        pass


#wpa_supplicant
def wpa_con():
    ''' main function for sending commands to wpa_supplicant  '''

    command = ["wpa_supplicant -B -i wlp0s4f1u1 -c /etc/wpa_supplicant/wpa_supplicant.conf"]
    proc = pp(['su', '-c'] + command, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    try:
        proc.stdin.write(pass_in_bytes)
        o, e = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        o, e = proc.communicate()

    if proc.returncode:
        print('connection failed \n')
    else:
        print('success \n')

    print(o.decode())
    #print("proc", e.decode())

    #Waiting for wpa_supplicant to establish the connection:
    print("waiting for wpa_supplicant...")
    time.sleep(2)
    print("starting DHCP")



#kill old processes
def kill_process():
    ''' find and terminate any wconnect, wpa_supplicant and dhcpcd processes '''
    myname = argv[0]
    mypid = getpid()
    for process in psutil.process_iter():
        if process.pid != mypid:
            for path in process.cmdline():
                if myname in path:
                    print("process found")
                    process.terminate()

    procname = "wpa_supplicant"

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == procname:
            proc.terminate()

#    os.system(f"killall -9 wpa_supplicant")


def dhcp():
    ''' launches the dhcpc service  '''

    command_dhcp = ['dhcpcd']

    proc2 = pp(['su', '-c'] + command_dhcp, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    proc2.stdin.write(pass_in_bytes)

    if proc2.returncode:
        print('DHCP failed establishing the connection... \n')
    else:
        print('DHCP: successful \n')

def main():
    ''' main function '''

    wpa_pass()
    kill_process()
    wpa_con()
    dhcp()


if __name__ == "__main__":
    main()
