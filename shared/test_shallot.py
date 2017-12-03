from security import *
from shallot import *
from copy import *
from Message import Message
from random import *

ls_hops=[]
ls_hops=[('172.16.1.1',5005),('172.16.2.1',6006),('172.16.3.1',7007)]

#print(type(ls_hops))
ls_keys=[]
for i in range(0,3):
    p=generate_prime_nb(1024)
    g=2
    a=generate_random_nb(8)
    b=generate_random_nb(8)

    A=DH_exchange(g,a,p)
    B=DH_exchange(g,b,p)
    key=DH_shared_secret(A,b,p)
    key=str(key)
    #key_id=generate_random_nb(32) #Does not generate exactly 32 bits every time
    key_id = getrandbits(32)
    #print(len(bin(key_id)))
    temp=(key_id,key)
    ls_keys.append(temp)

#print(ls_keys)
ls_keys_copy=deepcopy(ls_keys)

message='Bonjour les zamis'
message_final=build_shallot(ls_hops,ls_keys,message)
#print('Message final:',message_final)

####### Decoding the shallot #######

#print(Message.bits_repr(message_final[:4]))
message_final = message_final[4:]

for i in range(0,3):
    #print(len(bin(ls_keys_copy[i][0])))
    #key_id_received = message_final[12:12+len(bin(ls_keys_copy[i][0]))-2]
    key_id_received, ciphered = MESSAGE_RELAY.get_key_id_and_ciphtext(message_final)
    print('\nIteration',i,'\nKey ID received:',key_id_received,'    Same as original?',key_id_received == ls_keys_copy[i][0])
    #ciphered = message_final[12+len(bin(ls_keys_copy[i][0]))-2:]
    #print(type(ciphered))
    decrypted = decrypt(ls_keys_copy[i][1],ciphered)
    #next_hop_received = (decrypted[:16],decrypted[16:32])
    next_hop_received = MESSAGE_RELAY.get_next_hop(decrypted)
    #print('\nIP received:',next_hop_received[0],'Port received:',next_hop_received[1])
    print('IP received:',next_hop_received)
    #print(len(decrypted))
    if i == 2:
        message_final = decrypted[4:]
    else:
        message_final=decrypted[4+4:]
    #print(message_final)
#print(message_final)
print('\n' + message_final.decode('utf-8'))
