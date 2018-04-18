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
    return str(base64.encodebytes(encrypt_aes), encoding='utf-8')  
#decrypt the message
def decrypt_aes(key,msg):
    # initilize the decypter
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #decrypt to base_64
    base64_decrypted = base64.decodebytes(msg.encode(encoding='utf-8'))
    #strip the \0 and return the decrypted string
    return str(aes.decrypt(base64_decrypted),encoding='utf-8').rstrip('\0') # 

 
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
                    break
            if data.startswith('-----BEGIN RSA PUBLIC KEY-----'):
                pubkey = rsa.PublicKey.load_pkcs1(data.encode())
                data = encrypt_rsa(aeskey,pubkey)
                print ("sending: " + str(data))
                conn.send(data)
            else:
                data = decrypt_aes(aeskey,data)
                print ("recieved: " + str(data))
                #conn.send(data.encode())
             
    conn.close()
     
if __name__ == '__main__':
    Main()
