from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from Crypto.Cipher import AES
from Crypto import Random
from random import randint
from os import urandom
from base64 import b64encode
import rsa



class Client:
    '''
    a abstract class that includes all informations that server needs to connect with the client
    '''

    def __init__(self, name, socket, address, pubkey):
        self.name = name
        self.socket = socket
        self.address = address
        self.aes_key = urandom(16)
        self.aes_iv = urandom(16)
        self.aes_cipher = AES.new(self.aes_key, AES.MODE_ECB, self.aes_iv)
        self.SERVER_SOCKET_public_key, self.SERVER_SOCKET_private_key = rsa.newkeys(1024)
        self.client_public_key = rsa.PublicKey.load_pkcs1(pubkey.encode("utf-8"))

    def send_encrypting(self, msg):
        '''
        obtain an encrypted message by aes
        '''
        encrypted_msg = self.aes_cipher.encrypt(self.aespadding(msg).encode("utf-8"))
        return b64encode(encrypted_msg).decode("utf-8")
    
    # Not implemented
    def recv_decrypting(self, encrypted_msg):
        '''
        decrypted a received message
        '''
        return 0

    @staticmethod
    def aespadding(text, padding = ' '):
        '''
        add paddings to the end of text so that the length of the text is a multiply of 16
        AES requires that the message to be encrypted can be divided into blocks
        '''
        l = len(text) % 16
        n = int((16 - l)/len(padding))
        if not l == 0:
            return text + padding*n
        else:
            return text


def welcome():
    '''
    server's welcome method
    '''
    while True:
        client, client_address = SERVER_SOCKET.accept()
        # TODO:
        # Welcome message, contains the rsa key and encrypted aes
        # pass the control to thread

# not implemented
def session():
    '''
    handles the communication with the client
    '''
    return 0

# not implemented
def broadcast():
    '''
    broadcast all messages to all the other clients
    '''
    return 0
    
# the dictionary indexed by sockets and stores a Client typed client informations
clients = {}

HOST = '127.0.0.1'
PORT = 5000
ADDR = (HOST, PORT)
SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_SOCKET.bind(ADDR)
