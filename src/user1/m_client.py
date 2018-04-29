from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from encryption import *
from os import urandom
import rsa,os,shutil,time

KEY_LENGTH = 1024
BUFFER_SIZE = 4096
HOST = 5003
FILENAME = None
FOLDER = os.path.dirname(os.path.realpath(__file__)) + '\\files'




def receive(socket, aeskey):
    '''
    receive message from socket
    '''
    while True:
        try:
            msg = socket.recv(BUFFER_SIZE)
            msg = decrypt_aes(msg.decode('utf-8'), aeskey)
            global FOLDER
            global FILENAME
            if msg.startswith('PUSH*'):
                print('A new verison available')
                print('->',end='',flush = True)
                f = open(FOLDER  + "\\" + FILENAME.rsplit('.',1)[0]  + '_temp.bak', 'w+') #FILENAME.rsplit('.',1)[*] splits the extension and filename
                f.write(msg.split('*',1)[1])
                f.close()
            else:
                print(msg)
                print('->',end='',flush = True)
        except OSError:
            break

def send(socket, aeskey):
    while True:
        try:
            msg = input(' -> ')
            global FOLDER
            global FILENAME
            if not msg:
                continue
            elif msg == 'PUSH*': #push the file to server
                f = open(FOLDER + '\\' + FILENAME,'rb')
                send_aes_encrypted(socket, msg + f.read().decode('utf-8'), aeskey)
                print('Push successfully')
                print('->',end='',flush = True)
            elif msg == 'PULL*': #pull the newest verison to local repo
                temp = open(FOLDER  + "\\" + FILENAME.rsplit('.',1)[0]  + '_temp.bak', 'rb')
                f = open(FOLDER + '\\' + FILENAME,'w')
                f.write(temp.read().decode('utf-8'))
                f.close()
                temp.close()
                print('pull finished')
                print('->',end='',flush = True)
            elif msg == 'debug':
                f = open(FOLDER + '\\' + FILENAME,'rb')
                print(msg + f.read().decode('utf-8'))
            elif msg == 'QUIT':
                send_aes_encrypted(socket, msg, aeskey)
                print('Exitted')
                socket.close()
            else:
                send_aes_encrypted(socket, msg, aeskey)
        except OSError:
            break
        

def send_aes_encrypted(socket, msg, aeskey):
    '''
    send aes encrypted message to the given socket 
    '''
    socket.send(encrypt_aes(msg, aeskey))
    
def emptyFolder(dir):
    for the_file in os.listdir(dir):
        file_path = os.path.join(dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)



def Main():
    user_name = None
    while not user_name:
        user_name = input('Enter user name: ')
    

    addr = ('127.0,0,1',HOST)
    emptyFolder(FOLDER)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(('localhost',HOST))
    public_key, private_key = rsa.newkeys(1024)

    # send public key
    client_socket.send(public_key.save_pkcs1())
    aeskey = client_socket.recv(BUFFER_SIZE)
    aeskey = decrypt_rsa(aeskey, private_key)
    
    # send name
    send_aes_encrypted(client_socket, user_name, aeskey)
    
    
    #recieve welcome msg
    welcome_msg = decrypt_aes(client_socket.recv(BUFFER_SIZE).decode('utf-8'),aeskey)
    print(welcome_msg)
    #recieve file
    global FILE 
    FILE = decrypt_aes(client_socket.recv(BUFFER_SIZE).decode('utf-8'),aeskey)
    global FILENAME 
    FILENAME = FILE.split('*',1)[0] #strings before first * is filename
    print('{0} is up to date'.format(FILENAME))
    f = open(FOLDER + '\\' + FILENAME, 'w+')
    f.write(FILE.split('*',1)[1])
    f.close()
    try:
        recv_thread = Thread(target=receive, args=(client_socket, aeskey,))
        send_thread = Thread(target=send, args=((client_socket, aeskey)))
        recv_thread.start()
        send_thread.start()
    except KeyboardInterrupt:
        recv_thread.join()
        send_thread.join()
        client_socket.close()

if __name__ == "__main__":
    try:
        Main()
    except KeyboardInterrupt:
        print("quit")


    



