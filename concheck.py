import socket
import subprocess
import os
import sys
import time
import argparse
import tkinter

from tkinter import ttk


#argparse
parser = argparse.ArgumentParser(description='Checks connection in intervals via ping command')
parser.add_argument('-u', '--url', metavar='', required=True, help='target_url')
parser.add_argument('-i', '--interval', metavar='', type=int, default=10, help='change interval')
parser.add_argument('-l', '--limit', metavar='', type=float, default=32, help='sets threshold ping limit -> above limit font color changed to red; default 32 ms')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode - extra information') 
parser.add_argument('-a', '--alert', action='store_true', help='get an error window if connection get interrupted')
args = parser.parse_args()


#color
class Color:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    BLUE = '\033[0;034m'



#alert window 
window = tkinter.Tk()
window.title("Connection check")
window.geometry("300x30")
msg = "Connection interrupted: " + args.url
ip_lable = ttk.Label(window, text=msg)
ip_lable.pack()



#FUNCTION'S
def get_url_parm():
    ip = socket.gethostbyname(args.url)                             # always ip 
    cmd = "ping", "-c", "1", ip
    ping_output = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = str(ping_output.communicate())                         #returns ping output as a string
    
    split_out = output.split()             
    ping_ip = split_out[2][1:-1]           
    ping_ms = split_out[12].split("=")[1]
      
    return ping_ms, ping_ip



def ms_handler(time_interval, low_ping_limit, verbose):   
    ms_value, ip_value = get_url_parm()
    if float(ms_value) < low_ping_limit:
        print(Color.GREEN + ms_value + " ms " + ((ip_value + " " + args.url ) if verbose==True else "") + "\033[m")    # WHY: \033 => STOP coloring everything after if/else print
    else:
        print(Color.RED + ms_value + " ms " + ((ip_value + " " + args.url) if verbose==True else "") + "\033[m")

    time.sleep(time_interval)
    ms_handler(time_interval, low_ping_limit, verbose)
    
    


if __name__ == "__main__":
    try:
        ms_handler(args.interval, args.limit, args.verbose)
    except socket.gaierror:                                         #handle no valid arg.url => socket.gethostbyname()
        print("No valid url")
        if args.alert == True:
            window.mainloop()                                        
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)       


