from security import *
from Message import *
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

def build_shallot(ls_hops,ls_keys,message,sync=0):
#ATTENTION ls_hops and ls_keys have to be in direct order because we invert them 1 time
#ls_keys est un tuple (key_id,key)
#ls_hops= list of tuples (IP,port)
#ls_hops contains the direct path, but to build the shallot we need to reverse it
    if sync==0:
        ls_hops.reverse()
        ls_keys.reverse()
    if len(ls_hops)>0: #EN CONSIDERANT QUE ALICE N'EST PAS DANS ls_hops
        seq_nb=1 #A MODIFIER, QU EST CE QUE CA REPRESENTE
        key_id=ls_keys[0][0]
        next_hop=ls_hops[0]
        message_relay=MESSAGE_RELAY(seq_nb,key_id,next_hop,message)
        part=message_relay.to_cipher()
        ciphered=encrypt(ls_keys[0][1],part)
        #ciphered=str(ciphered).strip("b'")
        #ciphered = ciphered.decode('unicode_escape').encode('utf-8')
        #print('ciphered:',ciphered.decode('utf-8'))
        total_message=message_relay.plain_text_part()+ciphered

        ls_hops.remove(ls_hops[0])
        ls_keys.remove(ls_keys[0])
        sync=1;
        #print('iteration')
        #print('Total message:',total_message)
        return build_shallot(ls_hops,ls_keys,total_message,sync)

    elif len(ls_hops)==0: #quand ca arrive chez Alice
        return message
