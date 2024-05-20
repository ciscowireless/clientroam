'''
Roaming verification script, prints basic wireless parameters on Windows client
Saves output to CSV

"Timestamp SSID:XXX BSSID:XX:XX:XX:XX:XX:XX Channel:XXX Mode:802.11.XXX Signal:XXX TX:XXX RX:XXX"

Tested on Windows 11

netpacket.net/2020/06/client-roaming-and-scripts/
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
                band = re.search(r'(Band\s+:\s)(.+)', output).group(2).rstrip()
                rxrate = re.search(r'(Receive rate.+?:\s)(.+)', output).group(2).rstrip()
                txrate = re.search(r'(Transmit rate.+?:\s)(.+)', output).group(2).rstrip()
                signal = re.search(r'(Signal.+?:\s)(.+)', output).group(2).rstrip()
                
                #show_as_rssi - attempts to convert Windows signal strength % into dBm - believe this at your own risk
                if show_as_rssi:
                    signal = f"-{str(100-round(int(signal[:-1])/2))}dBm"

            except AttributeError:
                print('Data unavailable')
            else:
                if bssid != previous_bssid:
                    previous_bssid = bssid
                    roam_counter += 1
                if roam_counter % 2 == 0:
                    bss_colour = Fore.CYAN
                else:
                    bss_colour = Fore.YELLOW

                print(timestamp[11:], Fore.GREEN + "SSID:", ssid, Fore.GREEN + "BSSID:", bss_colour + bssid, 
                      Fore.GREEN + "Channel:", channel, Fore.GREEN + "Band:", band, Fore.GREEN + "Signal:", signal, 
                      Fore.GREEN + "RX(Mbps):", rxrate, Fore.GREEN + "TX(Mbps):", txrate)
                output_file.write(f"{timestamp[:11]},{timestamp[11:]},{ssid},{bssid},{channel},{band},{signal},{rxrate},{txrate}\n")

            time.sleep(output_delay)
    except KeyboardInterrupt:
        output_file.close()
        sys.exit()


if __name__ == "__main__":

    init(autoreset=True)
    run()



