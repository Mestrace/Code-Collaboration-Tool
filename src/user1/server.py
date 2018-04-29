import socket
from encryption import *
from base64 import b64encode

 
def Main():
    host = "127.0.0.1"
    port = 5000
     
    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    #preparing the AES key
    aeskey = random_key(16)
    print ("Connection from: " + str(addr) + "AES ksy: " + aeskey)
    while True:
            data = conn.recv(1024).decode()
            print ("from connected  user: " + str(data))

            if not data:
                continue
            if data.startswith('-----BEGIN RSA PUBLIC KEY-----'):
                pubkey = rsa.PublicKey.load_pkcs1(data.encode())
                data = encrypt_rsa(aeskey,pubkey)
                print ("sending: " + b64encode(data).decode("utf-8"))
                conn.send(data)
            else:
                data = decrypt_aes(aeskey,data)
                print ("recieved: " + str(data))
                #conn.send(data.encode())
             
    conn.close()
     
if __name__ == '__main__':
    Main()
