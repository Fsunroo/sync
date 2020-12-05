from socket import *
import os
IP = '192.168.43.10'
PORT = 4444
SHARED_FOLDER= 'Server Folder'

def comprehence(client_files):
    SHARED_FOLDER = 'Server Folder'
    send_list = []
    get_list = []
    server_files = os.listdir(SHARED_FOLDER)
    for file in server_files:
        if not file in client_files:
            send_list.append(file)
    for file in client_files:
        if not file in server_files:
            get_list.append(file)
    return send_list,get_list

def Send(file_name):
    file = open(os.path.join(SHARED_FOLDER,file_name),'rb')
    data = file.read(1024)
    while data:
        conn.send(data)
        data = file.read(1024)
    conn.send('__Done__'.encode())

def Recive(file_name):
    with open(os.path.join(SHARED_FOLDER,file_name),'wb') as file:
        while 1:
            data = conn.recv(1024)

            if data == '__Done__'.encode():
                break

            file.write(data)
        file.close()






s = socket()
s.bind((IP,PORT))
print(f'[binded to{IP}:{PORT}]')
s.listen(100)
conn, addr = s.accept()                                                 #1-Accept Client Connection
print(f'[connection accepted from {addr}')

client_files = conn.recv(1024).decode().split(' ')                      #2-Recive Client File List

send_list,get_list = comprehence(client_files)

conn.send(' '.join(send_list).encode())                 #3-Send ServerOnly Files list
conn.send(' '.join(get_list).encode())                  #4-Send ClientOnly Files list

for file_name in send_list:
    Send(file_name)                                                     #5-Send ServerOnly Files 

for file_name in get_list:
    Recive(file_name)