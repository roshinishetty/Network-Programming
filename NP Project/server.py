import argparse, socket, sys
import threading
import time , schedule
import datetime

def handle_client_connections(client_socket) :
    # Append all the data received to a file with client IP as name
    request = client_socket.recv(1024)
    print('Received {}'.format(request))
    client_socket.send('ACK!')
    client_socket.close()

def job():
    bind_ip = '172.16.42.78'
    bind_port = 1060

    print("TCP Server up")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((bind_ip, bind_port))
    server_socket.listen(5) #max backlog of connections
    print("Listening")

    while (datetime.now().time() != "15:00:00"):
        client_socket, address = server_socket.accept()
        print("Accepted connection from {}:{}".format(address[0], address[1])) 
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_socket,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        )
        client_handler.start()

if __name__ =="__main__":
    schedule.every(7).day.at("12:50").do(job)    

    while True:
        schedule.run_pending()
        time.sleep(1)