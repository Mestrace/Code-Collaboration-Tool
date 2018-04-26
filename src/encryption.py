from Crypto.Cipher import AES
from Crypto import Random
import base64,string,random,rsa



def gen_key(length):
    '''
    generate rsa public key and private key
    '''

    publicKey, privateKey = rsa.newkeys(length)
    return publicKey, privateKey

def read_key(pubPath,priPath):
    '''
    read public key and private key from file
    '''
    with open(pubPath, 'r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
    with open(priPath, 'r') as f:
        priKey = rsa.PublicKey.load_pkcs1(f.read().encode())
    return pubkey,priKey

def encrypt_rsa(msg, pubkey):
    '''
    encrypt the message with a rsa public key
    '''
    return rsa.encrypt(msg.encode(),pubkey)

def decrypt_rsa(cryptedMessage, prikey):
    '''
    decrypt the message with a rsa private key
    '''
    return rsa.decrypt(cryptedMessage, prikey).decode()

def random_key(n):
    '''
    generate a random key in string with given length
    '''
    # should we use os.urandom(<size>) ?
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(n))

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


def encrypt_aes(msg, key):
    '''
    encrypt the message using aes key
    '''
    aes = AES.new(aespadding(key), AES.MODE_ECB)
    #aes encrypt here
    encrypt_aes = aes.encrypt(aespadding(msg))
    #to string using base64
    return base64.encodebytes(encrypt_aes)


def decrypt_aes(msg, key):
    '''
    decrypt the message using aes key
    '''
    # initilize the decypter
    aes = AES.new(aespadding(key), AES.MODE_ECB)
    #decrypt to base_64
    base64_decrypted = base64.decodebytes(msg.encode(encoding='utf-8'))
    #strip the \0 and return the decrypted string
    return str(aes.decrypt(base64_decrypted),encoding='utf-8').rstrip('\0') # 