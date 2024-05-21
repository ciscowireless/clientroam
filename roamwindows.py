'''
Roaming verification script, prints basic wireless parameters on Windows client
Saves output to CSV

"Timestamp SSID:XXX BSSID:XX:XX:XX:XX:XX:XX Channel:XXX Mode:802.11.XXX Signal:XXX TX:XXX RX:XXX"

Tested on Windows 11

netpacket.net/2020/06/client-roaming-and-scripts/
'''

from datetime import datetime
import subprocess
import platform
import re
import sys
import time

from colorama import init, Fore


class scan:

    roam_counter = 0
    previous_bssid = None
    scan_output = ""
    output_file_name = 'wifiroam.csv'
    output_delay = 0.3
    show_as_rssi = False


def run_windows():

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
        if scan.show_as_rssi:
            signal = f"-{str(100-round(int(signal[:-1])/2))}dBm"

    except AttributeError:
        print('Data unavailable')
    else:
        if bssid != scan.previous_bssid:
            scan.previous_bssid = bssid
            scan.roam_counter += 1
        if scan.roam_counter % 2 == 0:
            bss_colour = Fore.CYAN
        else:
            bss_colour = Fore.YELLOW

        print(timestamp[11:], Fore.GREEN + "SSID:", ssid, Fore.GREEN + "BSSID:", bss_colour + bssid, 
              Fore.GREEN + "Channel:", channel, Fore.GREEN + "Band:", band, Fore.GREEN + "Signal:", signal, 
              Fore.GREEN + "RX(Mbps):", rxrate, Fore.GREEN + "TX(Mbps):", txrate)
        
        scan.scan_output = f"{timestamp[:11]},{timestamp[11:]},{ssid},{bssid},{channel},{band},{signal},{rxrate},{txrate}\n"


def run_apple():
    
    try:
        timestamp = str(datetime.now())[:-7]
        output = subprocess.check_output("profile sudo wdutil info").decode("ascii")
        ssid = re.search(r'(SSID\s+:\s)(.+)', output).group(2).rstrip()
        bssid = re.search(r'(BSSID\s+:\s)(.+)', output).group(2).rstrip()
        channel = re.search(r'(Channel\s+:\s)(.+)', output).group(2).rstrip()
        txrate = re.search(r'(Tx Rate\s+:\s)(.+)', output).group(2).rstrip()
        rssi = re.search(r'(RSSI\s+:\s)(.+)', output).group(2).rstrip()

    except AttributeError:
        print('Data unavailable')
    else:
        if bssid != scan.previous_bssid:
            scan.previous_bssid = bssid
            scan.roam_counter += 1
        if scan.roam_counter % 2 == 0:
            bss_colour = Fore.CYAN
        else:
            bss_colour = Fore.YELLOW    

        print(timestamp[11:], Fore.GREEN + "SSID:", ssid, Fore.GREEN + "BSSID:", bss_colour + bssid, 
              Fore.GREEN + "Channel:", channel, Fore.GREEN + "RSSI:", rssi, Fore.GREEN + "TX(Mbps):", txrate)

        scan.scan_output = f"{timestamp[:11]},{timestamp[11:]},{ssid},{bssid},{channel},{rssi},{txrate}\n"


def run():

    os = platform.system()
    try:
        output_file = open(scan.output_file_name, "w+")
    except PermissionError:
        print("Error writing file")
        sys.exit()
    try:
        while True:
            if os == "Windows":
                run_windows()
            elif os =="Darwin":
                pass
                #Apple functionality not implemented
                #run_apple()
            
            output_file.write(scan.scan_output)
            time.sleep(scan.output_delay)
    
    except KeyboardInterrupt:
        output_file.close()
        sys.exit()


if __name__ == "__main__":

    init(autoreset=True)
    run()



