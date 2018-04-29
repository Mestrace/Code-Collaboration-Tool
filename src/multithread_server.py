from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import urandom
from base64 import b64encode
from encryption import *
import rsa

KEY_LENGTH = 1024
BUFFER_SIZE = 1024
PORT = 5001
SYSTEM_MESSAGE_PREFIX = "SYSTEM"
INVALID_NAME_MESSAGE = "The user name {0} is invalid, please try a new one"
JOINED_CHAT_MESSAGE = "User {0} has joined the chat."
LEFT_CHAT_MESSAGE = "User {0} has left the chat. >>"

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
    connect_cnt = 2
    # generate random aeskey of 16
    # note the differences between b64 decoding
    aeskey = b64encode(urandom(12)).decode('utf-8')
    while connect_cnt != 0:
        # string data
        data = socket.recv(BUFFER_SIZE).decode()
    
        if connect_cnt == 2 and  data.startswith('-----BEGIN RSA PUBLIC KEY-----'):
            #obtain public key from the user send encrypted aes key
            pubkey = rsa.PublicKey.load_pkcs1(data.encode())
            data = encrypt_rsa(aeskey, pubkey)
            print("sending " + b64encode(data).decode("utf_8"))
            socket.send(data)
            connect_cnt -= 1
        elif connect_cnt == 1:
            name = decrypt_aes(data, aeskey)
            print(name + ' connected')
            # TODO: name validation
            clients[socket] = Client(name, socket, address, aeskey)
            broadcast(JOINED_CHAT_MESSAGE.format(name), SYSTEM_MESSAGE_PREFIX)
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
        if msg != 'QUIT':
            broadcast(msg, name)
        elif msg == '*PUSH':
            broadcast('*PUSH' + FILE.read())
        else:
            send_aes_encrypted(socket, "Quitting", aeskey)
            socket.close()
            del clients[socket]
            broadcast(LEFT_CHAT_MESSAGE.format(name), SYSTEM_MESSAGE_PREFIX)
            break
    

def broadcast(msg, prefix = ""):
    '''
    broadcast all messages to all the other clients
    '''
    
    for socket,client in clients.items():
        send_aes_encrypted(socket, prefix + ": " + msg, client.aeskey)
        print('broadcasting: {0}'.format(msg))


def send_aes_encrypted(socket, msg, aeskey):
    '''
    send aes encrypted message to the given socket 
    '''
    socket.send(encrypt_aes(msg, aeskey))

# the dictionary indexed by sockets and stores a Client typed client informations
clients = {}

HOST = '127.0.0.1'
ADDR = (HOST, PORT)
SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_SOCKET.bind(ADDR)



if __name__ == "__main__":
    SERVER_SOCKET.listen(5)
    filename = 'test.txt'
    #FILE = open(filename,'rb')
    print("Waiting for connection...")
    try:
        ACCEPT_THREAD = Thread(target=accept)
        ACCEPT_THREAD.start()
    except KeyboardInterrupt:
        print('keyboardInterrupted!')
        ACCEPT_THREAD.join()
        SERVER_SOCKET.close()

