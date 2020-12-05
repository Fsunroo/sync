from socket import *
import os

IP = '192.168.43.10'
PORT = 4444
SHARED_FOLDER= '/sdcard/SHARED_FOLDER'
s = socket()
def Recive(file_name):
    with open(os.path.join(SHARED_FOLDER,file_name),'wb') as file:
        while 1:
            data =s.recv(1024)

            if data == '__Done__'.encode():
                break

            file.write(data)
        file.close()

def Send(file_name):
    file = open(os.path.join(SHARED_FOLDER,file_name),'rb')
    data = file.read(1024)
    while data:
        s.send(data)
        data = file.read(1024)
    s.send('__Done__'.encode())



print('[Connecting...]')
s.connect((IP, PORT))                                   #1-Connect
print(f'[Connected to {IP}:{PORT}]')

s.send(" ".join(os.listdir(SHARED_FOLDER)).encode())    #2-Send Client Folder List

get_list = s.recv(1024).decode().split()       #3-Recive ServerOnly Files List
send_list = s.recv(1024).decode().split()     #4-Recive ClientOnly Files List 
print(get_list)
print(send_list)
for file_name in get_list:
    Recive(file_name)

for file_name in send_list:
    Send(file_name)