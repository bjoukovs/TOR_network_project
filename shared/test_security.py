from security import *
from Crypto.Cipher import AES
import math as m

################ Working example ####################################################################
# obj = AES.new('This is a key123'.encode('utf-8'), AES.MODE_CBC, 'This is an IV456'.encode('utf-8'))
# message = "The answer is no".encode('utf-8')
# print('Message:',message)
# ciphertext = obj.encrypt(message)
# print('Ciphered message:',ciphertext)

# obj2 = AES.new('This is a key123'.encode('utf-8'), AES.MODE_CBC, 'This is an IV456'.encode('utf-8')) #attention iv must be the same as used for encryption
# print('Decrypted message:',obj2.decrypt(ciphertext))
#####################################################################################################



############### Using security file (not working for now) #################################################################

#erreurs: incorrect AES key size --> solved if size adjusted with while             (Zhao) Use a hash to solve this error
#         ValueError: Error 65537 while instatiating the CBC mode --> not solved    (Zhao) I don't have this error

p=generate_prime_nb(1024)
g=2
a=generate_random_nb(8)
b=generate_random_nb(8)

#si a et b sont sur + que 16 bits ca prend bcp de temps

A=DH_exchange(g,a,p)
B=DH_exchange(g,b,p)

key=DH_shared_secret(A,b,p)

## to adjust bit size of key if needed
# taille=104
# while(key.bit_length()!=taille):
#     key=m.floor(key/2)
##

print(key.bit_length())

key=str(key)
# print(key)
#key=key.ljust(32)
# print(key.encode('utf-8'))
# print(' '.join(map(bin,bytearray(key,'utf8'))))

message="Bonjour les kehs"
print('Message:',message)
[ciphertext,iv]=encrypt(key,message)
print('Encrypted message:',ciphertext)
decrypted_msg=decrypt(key,iv,ciphertext)
print('Decrypted message:',decrypted_msg)


#####################################################################################################

