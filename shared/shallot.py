import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.security import *
from shared.Message import *
from copy import deepcopy
from random import getrandbits

def negociate_key(sender,receiver):
    g=2 #A METTRE SUR 32 BITS!
    #A= ...
    key_init=KEY_INIT(key_id,g,A)

#def build_shallot(ls_hops,ls_keys,message,sync=0):
##ATTENTION ls_hops and ls_keys have to be in direct order because we invert them 1 time
##ls_keys est un tuple (key_id,key)
##ls_hops= list of tuples (IP,port)
##ls_hops contains the direct path, but to build the shallot we need to reverse it
#    if sync==0:
#        ls_hops.reverse()
#        ls_keys.reverse()
#    if len(ls_hops)>0: #EN CONSIDERANT QUE ALICE N'EST PAS DANS ls_hops
#        seq_nb=1 #A MODIFIER, QU EST CE QUE CA REPRESENTE
#        key_id=ls_keys[0][0]
#        next_hop=ls_hops[0]
#        message_relay=MESSAGE_RELAY(1,2,seq_nb,key_id,next_hop,message)
#        part=message_relay.part_to_cipher()
#        ciphered=encrypt(ls_keys[0][1],part)
#        ciphered=str(ciphered).strip("b'")
#        # ciphered = ciphered.decode('unicode_escape').encode('utf-8')
#        # print('ciphered:',ciphered.decode('utf-8'))
#        total_message=message_relay.part_non_cipher()+ciphered
#
#        ls_hops.remove(ls_hops[0])
#        ls_keys.remove(ls_keys[0])
#        sync=1;
#        #print('iteration')
#        #print('Total message:',total_message)
#        return build_shallot(ls_hops,ls_keys,total_message,sync)
#
#    elif len(ls_hops)==0: #quand ca arrive chez Alice
#        return message

def build_list_for_shallot(ls_hops,ls_keys):
    hops = deepcopy(ls_hops)
    keys = deepcopy(ls_keys)

    hops.append(ls_hops[-1])
    hops.reverse()
    keys.reverse()

    return hops, keys
    


def build_shallot(ls_hops,ls_keys,message,sync=0,msg_id=0):
#ATTENTION ls_hops and ls_keys have to be in direct order because we invert them 1 time
#ls_keys est un tuple (key_id,key)
#ls_hops= list of Relay_object
#ls_hops contains the direct path, but to build the shallot we need to reverse it
    if sync==0:
        ls_hops, ls_keys = build_list_for_shallot(ls_hops,ls_keys)
        print(ls_keys)
        msg_id = getrandbits(8)

    if len(ls_keys)>0:
        seq_nb=1 #A MODIFIER, QU EST CE QUE CA REPRESENTE
        key_id=ls_keys[0][0]
        next_hop=ls_hops[0]
        previous_hop = ls_hops[2]
        message_relay=MESSAGE_RELAY(msg_id,seq_nb,key_id,next_hop,previous_hop,message)
        part=message_relay.to_cipher()
        ciphered=encrypt(ls_keys[0][1],part)
        message_relay.update_length(ciphered)
        #ciphered=str(ciphered).strip("b'")
        #ciphered = ciphered.decode('unicode_escape').encode('utf-8')
        #print('ciphered:',ciphered.decode('utf-8'))
        total_message=message_relay.plain_text_part()+ciphered

        ls_hops.remove(ls_hops[0])
        ls_keys.remove(ls_keys[0])
        sync=1
        #print('iteration')
        #print('Total message:',total_message)
        return build_shallot(ls_hops,ls_keys,total_message,sync,msg_id)

    elif len(ls_keys)==0: #quand ca arrive chez Alice
        return message, msg_id
