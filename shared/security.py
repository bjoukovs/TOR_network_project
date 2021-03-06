#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
####################
# Security library #
####################
#
#

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import hashlib
from Crypto import Random
import base64
from Crypto.Util import number

# not protected
# p prime nb
# g base (need not to be a big value, 2 is usually good)

# a < p-1 Alice secret
# b < p-1 Bob secret

def DH_exchange(base,secret,prime_nb):
    """
    Computes the Diffie-Hellmann exchange value. This value is to be send to the target.
    It takes in arguments the agreed base and prime number as well as the secret.
    """
    #return (base**secret)%prime_nb # A=g^a mod p   ou  B=g^b mod p
    return pow(base,secret)%prime_nb # A=g^a mod p   ou  B=g^b mod p

    # utiliser la commande pow est bcp plus rapide

def DH_shared_secret(exchange_sender,secret_receiver,prime_nb):
    """
    Computes the Diffie-Hellmann shared secret using the exchange value received from the SENDER,
    the secret of the RECEIVER and the agreed prime number.
    """
    #return (exchange_sender**secret_receiver)%prime_nb  #=K_A=A^b mod p    ou   K_B=B^a mod p
    return (pow(exchange_sender,secret_receiver))%prime_nb  #=K_A=A^b mod p    ou   K_B=B^a mod p


def generate_prime_nb(bits):
    return number.getPrime(bits)

def generate_random_nb(bits):
    return number.getRandomInteger(bits)

## code perso pour le cryptage
def encrypt(key,message):
    # iv=generate_random_nb(128)  #ATTENTION ARBITRARY CHOICE OF 128 BITS FOR IV, IS IT OK?
    # iv=str(iv)
    #iv = Random.new().read(AES.block_size) #Return a random 16 bytes encoded as utf-8
    iv='This is an IV123'.encode('utf-8') #on 16 bytes because 1 caracter=1 byte

    # Hashing of the key to get a 32 bytes key
    h = SHA256.new()
    h.update(key.encode('utf-8'))
    key = h.digest()

    obj=AES.new(key, AES.MODE_CBC, iv)
    message=pad(message)
    #print(message)
    # obj=AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    if isinstance(message,str):
        ciphertext=obj.encrypt(message.encode('utf-8'))
    elif isinstance(message,bytes):
        ciphertext = obj.encrypt(message)
    #print('type_ciphertext:',type(ciphertext))
    #return [ciphertext,iv]
    #print(len(ciphertext))
    return ciphertext

def decrypt(key,ciphertext):
    #ATTENTION si iv fixe alors pas en argument, sinon le rajouter en argument

    # Hashing of the key to get a 32 bytes key
    iv='This is an IV123'.encode('utf-8') #on 16 bytes because 1 caracter=1 byte
    h = SHA256.new()
    h.update(key.encode('utf-8'))
    key = h.digest()
    #print(len(ciphertext))
    obj2=AES.new(key, AES.MODE_CBC, iv)
    # obj2=AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    decrypted_msg=obj2.decrypt(ciphertext)
    decrypted_msg=unpad(decrypted_msg)
    #print('type_decrypted_msg:',type(decrypted_msg))
    return decrypted_msg

def pad(s):
    if isinstance(s,str):
        bs=32
        padded = s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    elif isinstance(s,bytes):
        bs=32
        #padded = s + bytes(16 - len(s)%16)
        padded = s + (bs - len(s) % bs) * bytes([bs - len(s) % bs])
    return padded
def unpad(s):
    #print(ord(s[len(s)-1:]))
    return s[:-ord(s[len(s)-1:])]
##





""" Code de stackoverflow --> bug
class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
"""
