import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
import base64,string,random,rsa

#AES-demo


def gen_key(length):
    publicKey, privateKey = rsa.newkeys(length)
   # with open("public.pem", 'w+') as f:
    #    f.write(publicKey.save_pkcs1().decode())
    #with open("private.pem", 'w+') as f:
     #   f.write(privateKey.save_pkcs1().decode())
    return publicKey, privateKey

def read_key(pubPath,priPath):
    with open(pubPath, 'r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
    with open(priPath, 'r') as f:
        priKey = rsa.PublicKey.load_pkcs1(f.read().encode())
    return pubkey,priKey

def encrypt_rsa(msg, pubkey):
    return rsa.encrypt(msg.encode(),pubkey)

def decrypt_rsa(cryptedMessage, prikey):
    return rsa.decrypt(cryptedMessage, prikey).decode()

#random key with given length
def random_key(n):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(n))

# add the key to 16-bytes
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  
#encrypt the message
def encrypt_aes(key,msg):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #aes encrypt here
    encrypt_aes = aes.encrypt(add_to_16(msg))
    #to string using base64
    return base64.encodebytes(encrypt_aes)
#decrypt the message
def decrypt_aes(key,msg):
    # initilize the decypter
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #decrypt to base_64
    base64_decrypted = base64.decodebytes(msg.encode(encoding='utf-8'))
    #strip the \0 and return the decrypted string
    return str(aes.decrypt(base64_decrypted),encoding='utf-8').rstrip('\0') # 

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
        asekey = None
        
        #message = input(" -> ")
        message = publicKey.save_pkcs1()
        mySocket.send(message)
        while True:#message != '           
                if not key_recieved: #should continously listen the inbound packet
                    data = mySocket.recv(1024)
                    print ('Received from server: ' + str(data)) 
                    aeskey = decrypt_rsa(data, privateKey)
                    print("AES key is: " + aeskey)
                    key_recieved = True
                message = input('-> ')
                message = encrypt_aes(aeskey,message)
                mySocket.send(message)
                 
        mySocket.close()
 
if __name__ == '__main__':
    Main()
