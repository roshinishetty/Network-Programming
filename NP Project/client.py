# Client program that stores logs of using external devices,
#  LAN and internet connection and sends to Server.

import argparse, socket, sys
import  time, schedule
import datetime
import logging

def create_logfile() :
#Keep storing the logs into file till datetime.now().time() != "15:00:00"
    LOG_FILENAME = "sample.log"
    logging.basicConfig(filename = LOG_FILENAME, level = logging.debug, format = '%(asctime)s %(message)s', datefmt = '%H:%M:%S')
    logging.info('Hi')    

def send_data(client_socket) :
    client_socket.send("Hello")
    f = open('sample.log', 'rb')
    print('Sending ...')

    l = f.read(1024)
    while(l) :
        print('Sending ...')
        client_socket.send(l)
        l = f.read(1024)
    f.close()
    print("Done Sending")
    client_socket.shutdown(socket.SHUT_WR)
    #print client_socket.recv(1024)
    client_socket.close()    



#def send_notification() :


def job():

        print("Connecting to server...")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect(('172.16.42.78',1060))
        print('Client connected')
        print('socket name - ', client_socket.getsockname())

        create_logfile()

        send_data(client_socket)
    
if __name__ == "__main__":
    schedule.every(7).day.at("13:00").do(job)    

    while True:
        schedule.run_pending()
        time.sleep(1)