from socket import *
import os

IP = '192.168.43.10'
PORT = 4444
SHARED_FOLDER= '/sdcard/SHARED_FOLDER'
s = socket()
def Recive(file_name):
    with open(os.path.join(SHARED_FOLDER,file_name),'wb') as file:
        data =s.recv(1024)
        while not data == '__Done__'.encode():

            file.write(data)
            data =s.recv(1024)
            #print('while loop')
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
print('[sending client File list]')
s.send(" ".join(os.listdir(SHARED_FOLDER)).encode())    #2-Send Client Folder List
print('[client File list send]')
print('[reciving ServerOnly File list')
get_list = s.recv(1024).decode().split()       #3-Recive ServerOnly Files List
print(f'[ServerOnly File list recived: {get_list}')
print('[reciving clientOnly File list')
send_list = s.recv(1024).decode().split()     #4-Recive ClientOnly Files List 
print(f'[ClientOnly File list recived: {send_list}')
print(get_list)
print(send_list)
for file_name in get_list:
    print(f'[Reciving {file_name} from server')
    Recive(file_name)
    print(f'{file_name} seccssesfully! recived') 

for file_name in send_list:
    print(f'[sending {file_name}  to server')
    Send(file_name)
    print(f'{file_name} seccssesfully! sent') 