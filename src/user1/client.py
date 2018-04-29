import socket
from encryption import *
from base64 import b64encode


"""
Client generates the RSA key sends public key back to server
Then wait for encrypted AES key from server and use private key to decrypt it
All other messages will be sent via AES encryption
"""
def Main():
        host = '127.0.0.1'
        port = 5000
        key_recieved = False
        mySocket = socket.socket()
        mySocket.connect((host,port))
        publicKey,privateKey = rsa.newkeys(1024) 
        
        #message = input(" -> ")
        message = publicKey.save_pkcs1()
        mySocket.send(message)
        while True:          
            if not key_recieved: #should continously listen the inbound packet
                data = mySocket.recv(1024)
                print ('Received from server: ' + b64encode(data).decode("utf-8")) 
                aeskey = decrypt_rsa(data, privateKey)
                print("AES key is: " + aeskey)
                key_recieved = True
            message = input('-> ')
            message = encrypt_aes(aeskey,message)
            mySocket.send(message)
        mySocket.close()
 
if __name__ == '__main__':
    Main()
