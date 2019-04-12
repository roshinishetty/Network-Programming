# Client program that stores logs of using external devices,
#  LAN and internet connection and sends to Server.
from __future__ import print_function
import scapy
import argparse, socket, sys
import  time, schedule
from datetime import datetime 
import urllib.request
import psutil
import win32com.client

def create_file() :
#Keep storing the logs into file till datetime.now().time() != "15:00:00"
    start = datetime.now()
    #finish = datetime.now()
    f=open("logs.txt","w+")
    while((datetime.now()-start).seconds<2*60*60):

        # For checking internet connection
        for connection in (psutil.net_connections(kind='tcp')):
            f.write(connection[3].encode())

        # For usb
        loop_value = 1 
        while (loop_value==1):
            try:
                urllib.request.urlopen("https://www.google.com/")
            except urllib.request.URLError:
                f.write("Network down.")
                loop_value = 0
            else:
                f.write("Up and running.")
                loop_value = 0
        
        # For checking usb connection        
        wmi = win32com.client.GetObject ("winmgmts:")
        for usb in wmi.InstancesOf ("Win32_USBHub"):
            print(usb.DeviceID)
        
        # for checking local server connection
        sniff(filter="arp", prn=handle_arp_packet)                    


def send_data(client_socket) :
    client_socket.send("Hello")
    f = open('sample.log', 'rb')
    print('Sending ...')

    l = f.read(1024)
    while(l) :
        print('Sending ...')
        client_socket.send(l.encode())
        l = f.read(1024)
    f.close()
    message="\t"
    client_socket.send(message)
    print("Done Sending")
    client_socket.shutdown(socket.SHUT_WR)
    #print client_socket.recv(1024)
    client_socket.close()    


def job():

        print("Connecting to server...")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("hellooo")    
        client_socket.connect(('127.0.0.1',1060))
        print('Client connected')
        print('socket name - ', client_socket.getsockname())

        create_file()

        send_data(client_socket)

    
if __name__ == "__main__":
    print("Client program")
    #schedule.every(7).days.at("12:50").do(job)    
    job()
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)