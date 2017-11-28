from peer_config import read_config
from relay import Relay

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.Path_finding_V3 import Dijkstra

IP = "0.0.0.0"
PORT = 0

RELAYS = read_config()
print(RELAYS)

##########
#IMPORTANT
##########

#RELAYS est un dictionnaire contennant comme clé des ADRESSES IP
#A chaque clé est associé une liste d'objets 'Relay'
#Chaque Relay contient lui même un dictionnaire neighbors_and_costs qui contient comme clé les objets relais qui lui sont connectés et comme valeur le cout de la connection


a = Relay('a',1)
b = Relay('b',1)
c = Relay('c',1)
d = Relay('d',1)
e = Relay('e',1)
f = Relay('f',1)
g = Relay('g',1)
h = Relay('h',1)
i = Relay('i',1)

a.connect(c,1)
c.connect(d,2)
c.connect(i,4)
c.connect(h,1)
d.connect(e,8)
e.connect(b,1)
e.connect(i,2)
e.connect(f,1)
f.connect(h,5)
f.connect(g,2)
g.connect(h,1)


RELAYS = {}
RELAYS['a'] = [a]
RELAYS['b'] = [b]
RELAYS['c'] = [c]
RELAYS['d'] = [d]
RELAYS['e'] = [e]
RELAYS['f'] = [f]
RELAYS['g'] = [g]
RELAYS['h'] = [h]
RELAYS['i'] = [i]

print("Peer initialized with:",IP, PORT)
print()
print("Dictionnary of relays with their IP as a key",RELAYS)
print()

#Test pour voir si les connections sont bien faites
for key,item in RELAYS.items():
    print("Pour l'adresse", key)
    for relay in item:
        print("     Le relais",relay.ip, relay.port,"est connecté aux relais")
        for item,key in relay.neighbors_and_costs.items():
            print("           ",item.ip,item.port,"avec un cout de",key)

    print()

path = Dijkstra(RELAYS['a'][0], RELAYS['b'][0], RELAYS)
for i in path:
    print(i.ip)