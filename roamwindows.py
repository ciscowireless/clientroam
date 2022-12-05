'''
Roaming script, print basic wireless parameters on Windows client
Saves output to CSV
"Timestamp SSID:XXX BSSID:XX:XX:XX:XX:XX:XX Channel:XXX Signal:XXX TX:XXX RX:XXX"
Tested on Windows 10
netpacket.net
'''

from datetime import datetime
import subprocess
import re
import sys
import time

from colorama import init, Fore

output_file_name = 'wifiroam.csv'
output_delay = 0.3
show_as_rssi = False
#show_as_rssi : attempts to convert Windows signal strength % into dBm - this is a best effort calculation


def run():

    roam_counter = 0
    previous_bssid = None
    try:
        output_file = open(output_file_name, "w+")
    except PermissionError:
        print('Error writing file')
        sys.exit()
    try:
        while True:
            try:
                timestamp = str(datetime.now())[:-7]
                output = subprocess.check_output('netsh wlan show interfaces').decode('ascii')
            
                ssid = re.search(r'(SSID.+?:\s)(.+)', output).group(2).rstrip()
                bssid = re.search(r'(BSSID.+?:\s)(.+)', output).group(2).rstrip()
                channel = re.search(r'(Channel.+?:\s)(.+)', output).group(2).rstrip()
                mode = re.search(r'(Radio type.+?:\s)(.+)', output).group(2).rstrip()
                rxrate = re.search(r'(Receive rate.+?:\s)(.+)', output).group(2).rstrip()
                txrate = re.search(r'(Transmit rate.+?:\s)(.+)', output).group(2).rstrip()
                signal = re.search(r'(Signal.+?:\s)(.+)', output).group(2).rstrip()
                
                if show_as_rssi:
                    signal = f"-{str(100-round(int(signal[:-1])/2))}dBm"
            except AttributeError:
                print('No output')
            else:
                if bssid != previous_bssid:
                    previous_bssid = bssid
                    roam_counter += 1
                if roam_counter % 2 == 0:
                    print(timestamp[11:], Fore.GREEN + "SSID:", ssid, Fore.GREEN + "BSSID:", Fore.CYAN + bssid, 
                          Fore.GREEN + "Channel:", channel, Fore.GREEN + "Mode:", mode, Fore.GREEN + "Signal:", signal, 
                          Fore.GREEN + "RX(Mbps):", rxrate, Fore.GREEN + "TX(Mbps):", txrate)
                else:
                    print(timestamp[11:], Fore.GREEN + "SSID:", ssid, Fore.GREEN + "BSSID:", Fore.YELLOW + bssid, 
                          Fore.GREEN + "Channel:", channel, Fore.GREEN + "Mode:", mode, Fore.GREEN + "Signal:", signal, 
                          Fore.GREEN + "RX(Mbps):", rxrate, Fore.GREEN + "TX(Mbps):", txrate)

                output_file.write(f"{timestamp[:11]},{timestamp[11:]},{ssid},{bssid},{channel},{mode},{signal},{rxrate},{txrate}\n")
            time.sleep(output_delay)
    except KeyboardInterrupt:
        output_file.close()
        sys.exit()


if __name__ == "__main__":

    init(autoreset=True)
    run()



