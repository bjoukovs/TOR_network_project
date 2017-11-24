#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
####################
# Security library #
####################
# 
# 

from Crypto.Cipher import AES

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

