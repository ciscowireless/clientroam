'''
Roaming script, print basic wireless parameters on Windows client

Saves output to CSV
"2026-01-01 12:00:00  SSID:xxxxxxxx  Band:x GHz  Channel:x  RSSI:-xdBm  Rx:xxx  Tx:xxx BSSID:00:00:00:00:00:00"

Usage: roamwindows.py

Tested on Windows 11
'''
from datetime import datetime
import subprocess, re, sys, time
from colorama import Fore, init

init(autoreset=True)
output_file_name = "wifiroam.csv"
previous_bssid = None
roam_counter = 0
try:
    output_file = open(output_file_name, "w+")
    #creates new file, overwriting existing, in folder from which the script is executed
except PermissionError:
    print("Error writing file")
    sys.exit()
try:
    while True:
        try:
            timestamp = str(datetime.now())[:-7]
            output = subprocess.check_output("netsh wlan show interfaces").decode("ascii")
            ssid = f"{Fore.MAGENTA} SSID:{Fore.WHITE}" + re.search(r'(SSID.+?:\s)(.+)', output).group(2).rstrip()
            bssid = re.search(r'(BSSID.+?:\s)(.+)', output).group(2).rstrip()
            channel = f"{Fore.MAGENTA} Channel:{Fore.WHITE}" + re.search(r'(Channel.+?:\s)(.+)', output).group(2).rstrip()
            band = f"{Fore.MAGENTA} Band:{Fore.WHITE}" + re.search(r'(Band +?:\s)(.+)', output).group(2).rstrip()
            rxrate = f"{Fore.MAGENTA} Rx:{Fore.WHITE}" + re.search(r'(Receive rate.+?:\s)(.+)', output).group(2).rstrip()
            txrate = f"{Fore.MAGENTA} Tx:{Fore.WHITE}" + re.search(r'(Transmit rate.+?:\s)(.+)', output).group(2).rstrip()
            rssi = f"{Fore.MAGENTA} RSSI:{Fore.WHITE}" + re.search(r'(Rssi.+?:\s)(.+)', output).group(2).rstrip() + "dBm"
            #signal = f"-{str(100-round(int(signal[:-1])/2))}"
        except AttributeError:
            print('No output')
        else:
            if bssid != previous_bssid:
                previous_bssid = bssid
                roam_counter += 1
            if roam_counter % 2 == 0:
                print(timestamp, ssid, band, channel, rssi, rxrate, txrate, Fore.MAGENTA + "BSSID:" + Fore.CYAN + bssid)
            else:
                print(timestamp, ssid, band, channel, rssi, rxrate, txrate, Fore.MAGENTA + "BSSID:" + Fore.YELLOW + bssid)
            output_file.write(f"{timestamp},{ssid},{bssid},{channel},{band},{rxrate},{txrate},{rssi}\n")
        time.sleep(0.5)
except KeyboardInterrupt:
    output_file.close()
    sys.exit()
