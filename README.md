# wpa_supplicant_automator
A simple python script to automate wifi connection using wpa_supplicant and wpa_passphrase tools using subprocess module of python on Linux systems.

## Instructions:

1. make it executable with 'chmod +x' or run it with python3.4+
2. un 1st run you can set the SSID and password with : wsa -s <SSID> <Password>
  2.1. edit the interface name in the script for your wifi card (ex: wlan0) -- there will be an argument to set this in next release.
3. save and exit the editor.
4. run the script.
5. -l or --list = shows the current configured SSID.

### Optional:
6. it's recommended to add the executable script to '/usr/bin' or just add its address to the environment.
