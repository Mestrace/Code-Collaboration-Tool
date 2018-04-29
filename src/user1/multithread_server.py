from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import urandom
from base64 import b64encode
from encryption import *
from time import gmtime, strftime
import rsa,os,shutil


KEY_LENGTH = 1024
BUFFER_SIZE = 8192
PORT = 5003
SYSTEM_MESSAGE_PREFIX = "SYSTEM"
INVALID_NAME_MESSAGE = "The user name {0} is invalid, please try a new one"
JOINED_CHAT_MESSAGE = "User {0} has joined the chat."
LEFT_CHAT_MESSAGE = "User {0} has left the chat. >>"
FILENAME = 'test.py'
VERSION = 1
FOLDER = os.path.dirname(os.path.realpath(__file__)) + '\\server_files\\'

class Client:
    '''
    a abstract class that includes all informations that server needs to connect with the client
    '''
    def __init__(self, name, socket, address, aeskey):
        self.name = name
        self.socket = socket
        self.address = address
        self.aeskey = aeskey


def accept():
    '''
    server's welcome method
    '''
    while True:
        sock, addr = SERVER_SOCKET.accept()
        Thread(target=welcome, args=(sock, addr,)).start()


def welcome(socket, address):
    disconnect_cnt = 0
    connect_cnt = 3
    # generate random aeskey of 16
    # note the differences between b64 decoding
    aeskey = b64encode(urandom(12)).decode('utf-8')
    global FILENAME 
    global FOLDER
    while connect_cnt != 0:
        # string data
        if (connect_cnt != 1 ): #no msg needed for that prase
            data = socket.recv(BUFFER_SIZE).decode()
    
        if connect_cnt == 3 and  data.startswith('-----BEGIN RSA PUBLIC KEY-----'):
            #obtain public key from the user send encrypted aes key
            pubkey = rsa.PublicKey.load_pkcs1(data.encode())
            data = encrypt_rsa(aeskey, pubkey)
            socket.send(data)
            connect_cnt -= 1
        elif connect_cnt == 2:
            name = decrypt_aes(data, aeskey)
            print(name + ' connected')
            # TODO: name validation
            clients[socket] = Client(name, socket, address, aeskey)
            broadcast(JOINED_CHAT_MESSAGE.format(name), SYSTEM_MESSAGE_PREFIX)
            connect_cnt -= 1
        elif connect_cnt == 1: #transfer file
            FILE = open(FOLDER + FILENAME,'rb')
            filemsg = '{0}*{1}'.format(FILENAME,FILE.read().decode('utf-8'))
            socket.send(encrypt_aes(filemsg, aeskey))
            FILE.close()
            connect_cnt -= 1
        else:
            # invalid connection without setting up phase
            disconnect_cnt += 1
            if disconnect_cnt > 20:
                socket.send("Invalid connection.")
                del clients[socket]
                socket.close()
                return
    session(name, socket, aeskey)
                

# not implemented
def session(name, socket, aeskey):
    '''
    handles the communication with the client
    '''
    while True:
        msg = decrypt_aes(socket.recv(BUFFER_SIZE).decode('utf-8'), aeskey)
        if msg.startswith('PUSH*'):
            print('push recieved')
            global VERSION 
            global FOLDER
            f = open(FOLDER + FILENAME.rsplit('.',1)[0]  + '_v' + str(VERSION) + '.' + FILENAME.rsplit('.',1)[1], 'w+') #FILENAME.rsplit('.',1)[*] splits the extension and filename
            f.write(msg.split('*',1)[1])
            f.close()
            VERSION += 1
            broadcast(msg,mode = 'CUSTOM')
        elif msg == 'QUIT':
            send_aes_encrypted(socket, "Quitting", aeskey)
            socket.close()
            del clients[socket]
            broadcast(LEFT_CHAT_MESSAGE.format(name), SYSTEM_MESSAGE_PREFIX)
            break
        else:
            broadcast(msg, name)
    

def broadcast(msg, prefix = "", mode = 'DEFAULT'):
    '''
    broadcast all messages to all the other clients
    '''
    if mode == 'DEFAULT':
        for socket,client in clients.items():
            send_aes_encrypted(socket, prefix + '  ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n' + msg, client.aeskey)
            print('broadcasting: {0}'.format(msg))
    elif mode == 'CUSTOM':
        for socket,client in clients.items():
            send_aes_encrypted(socket, msg, client.aeskey)
            print('broadcasting: {0}'.format(msg))


def send_aes_encrypted(socket, msg, aeskey):
    '''
    send aes encrypted message to the given socket 
    '''
    socket.send(encrypt_aes(msg, aeskey))
    
def emptyFolder(dir,filename = FILENAME):
    for the_file in os.listdir(dir):
        if the_file == filename:
            pass
        else:
            file_path = os.path.join(dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


    


# the dictionary indexed by sockets and stores a Client typed client informations
clients = {}

HOST = '127.0.0.1'
ADDR = (HOST, PORT)
SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_SOCKET.bind(ADDR)



if __name__ == "__main__":
    SERVER_SOCKET.listen(5)
    emptyFolder(FOLDER)
    print("Waiting for connection...")
    try:
        ACCEPT_THREAD = Thread(target=accept)
        ACCEPT_THREAD.start()
    except KeyboardInterrupt:
        print('keyboardInterrupted!')
        ACCEPT_THREAD.join()
        SERVER_SOCKET.close()

