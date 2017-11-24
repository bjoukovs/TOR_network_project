#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
####################
# Security library #
####################
#
#

from Crypto.Cipher import AES
import hashlib
from Crypto import Random
import base64

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
    return (base**secret)%prime_nb

def DH_shared_secret(exchange,secret,prime_nb):
    """
    Computes the Diffie-Hellmann shared secret using the exchange value received from the sender,
    the secret of the receiver and the agreed prime number.
    """
    return (exchange**secret)%prime_nb


class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

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
