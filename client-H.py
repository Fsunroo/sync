from socket import *
import os

#IP = '127.0.0.1'
IP = '192.168.43.10'
PORT = 4444
SHARED_FOLDER= '/sdcard/SHARED_FOLDER/'
#SHARED_FOLDER= 'Client Folder'
s = socket()
def Recive(file_name):
    with open(os.path.join(SHARED_FOLDER,file_name),'wb') as file:
        data =s.recv(1024)
        while data:
            file.write(data)
            data =s.recv(1024)
        file.close()
        print('[file closed]')
        s.shutdown(SHUT_RDWR)
        s.close()
        

def Send(file_name):
    file = open(os.path.join(SHARED_FOLDER,file_name),'rb')
    data = file.read(1024)
    while data:
        s.send(data)
        data = file.read(1024)
    s.shutdown(SHUT_RDWR)
    s.close()

def reconnect():
    s = socket()    
    s.connect((IP, PORT))

s.connect((IP, PORT))
print(f'[Connected to {IP}:{PORT}]')
s.send(" ".join(os.listdir(SHARED_FOLDER)).encode()) 
print('[client File list send]')
get_msg = s.recv(1024)
get_list = get_msg.decode('utf-8',errors = 'ignore').split(' ')
print(f'[ServerOnly File list recived: {get_list}]')
send_msg = s.recv(1024)
send_list = send_msg.decode('utf-8',errors = 'ignore').replace('-','').split(' ')
print(f'[ClientOnly File list recived: {send_list}]')
for file_name in get_list:
    print(f'[Reciving {file_name} from server]')
    Recive(file_name)
    print(f'[{file_name} seccssesfully! recived]')
    s = socket()
    s.connect((IP, PORT))
    print('[connected again]') 

for file_name in send_list:
    print(f'[sending {file_name}  to server]')
    Send(file_name)
    print(f'[{file_name} seccssesfully! sent]')
    s = socket()
    s.connect((IP, PORT))


print('*********** File Transfer Done!***********')