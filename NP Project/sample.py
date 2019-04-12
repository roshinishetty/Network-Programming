import psutil
for connection in (psutil.net_connections(kind='tcp')):
    print(connection[3])