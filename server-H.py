from socket import *
import os
#IP = '127.0.0.1'
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
    conn.shutdown(SHUT_RDWR)
    conn.close()


def Recive(file_name):
    with open(os.path.join(SHARED_FOLDER,file_name),'wb') as file:
        data =conn.recv(1024)
        while data :

            file.write(data)
            data =conn.recv(1024)
        file.close()
        print('[file closed]')
        conn.shutdown(SHUT_RDWR)
        conn.close()







s = socket()
s.bind((IP,PORT))
print(f'[binded to {IP}:{PORT}]')
s.listen(100)
conn, addr = s.accept()                                                  #1-Accept Client Connection
print(f'[connection accepted from {addr}]')

client_files = conn.recv(1024).decode().split(' ')                       #2-Recive Client File List

send_list,get_list = comprehence(client_files)
send_msg = ' '.join(send_list).encode('utf-8')
conn.send(send_msg)                                                      #3-Send ServerOnly Files list
print(f'[ServerOnly file list sent: {send_list}]')
get_msg = ' '.join(get_list).encode('utf-8')
get_msg+=b'-'*(1024-len(get_msg))
conn.send(get_msg)                                                       #4-Send ClientOnly Files list
print(f'[ClientOnly file list sent: {get_list}]')

for file_name in send_list:
    print(f'[sending {file_name}  to client]')
    Send(file_name)                                                      #5-Send ServerOnly Files 
    print(f'[{file_name} seccssesfully! sent]')
    print('[accepting..]')
    conn, addr = s.accept()
    print('[accepted]')

for file_name in get_list:
    print(f'[Reciving {file_name} from client]')
    Recive(file_name)
    print(f'[{file_name} seccssesfully! recived]')
    print('[accepting..]')
    conn, addr = s.accept()
    print('[accepted]')



print('*********** File Transfer Done!***********')