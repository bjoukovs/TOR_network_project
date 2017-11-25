from security import *
from Crypto.Cipher import AES

p=generate_prime_nb(1024)
g=2
a=generate_random_nb(8)
b=generate_random_nb(8)

#si a et b sont sur + que 16 bits ca prend bcp de temps

A=DH_exchange(g,a,p)
B=DH_exchange(g,b,p)

key=DH_shared_secret(A,b,p)

# IV generation
iv = Random.new().read(16)
iv=iv.encode('utf-8')
# test key
key='123'.encode('utf-8')
# Encryption
encryption_suite = AES.new('123', AES.MODE_CBC, '456')
cipher_text = encryption_suite.encrypt("A really secret message. Not for prying eyes.")

# Decryption
decryption_suite = AES.new('123', AES.MODE_CBC, '456')
plain_text = decryption_suite.decrypt(cipher_text)

##encipherer=AESCipher(key)
##message=145
##msg_cryp=encipherer=encipherer.encrypt(message)
