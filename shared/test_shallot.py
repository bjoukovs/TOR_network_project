from security import *
from shallot import *

ls_hops=[]
ls_hops=[('00000000000000000','100000000000000'),('00000000000000001','110000000000000'),('00000000000000011','111000000000000')]

print(type(ls_hops))
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
    key_id=generate_random_nb(32)
    temp=(key_id,key)
    ls_keys.append(temp)

print(ls_keys)

message='bonjour les zamis'
message_final=build_shallot(ls_hops,ls_keys,message)
