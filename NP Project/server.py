import argparse, socket, sys
import threading
import time, schedule
import datetime
import string

def handle_client_connections(client_socket) :
    client_ip = client_socket.getpeername()[0]
    print("Connected to ", client_ip)
    filename=client_ip + '.txt'
    # Append all the data received to a file with client IP as name
    request = client_socket.recv(1024)
    while(request is not None):
        f=open(filename,"a")
        f.write(request)
        request=client_socket.recv(1024)
    f.close()
    print('Received {}'.format(request))
    client_socket.send('ACK!')
    client_socket.close()

def job():
    bind_ip = socket.gethostbyname(socket.gethostname())
    bind_port = 1060

    print("TCP Server up")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((bind_ip, bind_port))
    server_socket.listen(5) #max backlog of connections
    print("Listening")

    while (datetime.datetime.now().time() != "15:00:00"):
        client_socket, address = server_socket.accept()
        print("Accepted connection from {}:{}".format(address[0], address[1])) 
        client_handler = threading.Thread(
            target=handle_client_connections,
            args=(client_socket,) 
        )
        client_handler.start()

if __name__ =="__main__":
    print("Server program")
    #schedule.every(7).days.at("12:50").do(job)    
    job()
    while True:
        schedule.run_pending()
        time.sleep(1)