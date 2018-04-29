from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from encryption import *
from os import urandom
import rsa

KEY_LENGTH = 1024
BUFFER_SIZE = 1024
HOST = 5001




def receive(socket, aeskey):
    '''
    receive message from socket
    '''
    while True:
        try:
            msg = socket.recv(BUFFER_SIZE)
            msg = decrypt_aes(msg.decode('utf-8'), aeskey)
            print(msg)
        except OSError:
            break

def send(socket, aeskey):
    while True:
        try:
            msg = input(' -> ')
            if not msg:
                continue
            send_aes_encrypted(socket, msg, aeskey)
        except OSError:
            break
        

def send_aes_encrypted(socket, msg, aeskey):
    '''
    send aes encrypted message to the given socket 
    '''
    socket.send(encrypt_aes(msg, aeskey))


def Main():
    user_name = None
    while not user_name:
        user_name = input('Enter user name: ')
    

    addr = ('127.0,0,1',HOST)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(('localhost',HOST))
    public_key, private_key = rsa.newkeys(1024)

    # send public key
    client_socket.send(public_key.save_pkcs1())
    aeskey = client_socket.recv(BUFFER_SIZE)
    aeskey = decrypt_rsa(aeskey, private_key)
    # send name
    send_aes_encrypted(client_socket, user_name, aeskey)
    try:
        recv_thread = Thread(target=receive, args=(client_socket, aeskey,))
        send_thread = Thread(target=send, args=((client_socket, aeskey,)))
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


    



