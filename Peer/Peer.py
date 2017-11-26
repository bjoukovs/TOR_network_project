from peer_config import read_config

IP = "0.0.0.0"
PORT = 0

RELAYS = read_config()

##########
#IMPORTANT
##########

#RELAYS est un dictionnaire contennant comme clé des ADRESSES IP
#A chaque clé est associé une liste d'objets 'Relay'
#Chaque Relay contient lui même un dictionnaire neighbors_and_costs qui contient comme clé les objets relais qui lui sont connectés et comme valeur le cout de la connection



print("Peer initialized with:",IP, PORT)
print("Dictionnary of relays with their IP as a key",RELAYS)

#Test pour voir si les connections sont bien faites
for key,item in RELAYS.items():
    print("Pour l'adresse", key)
    for relay in item:
        print("     Le relais",relay.ip, relay.port,"est connecté aux relais")
        for item,key in relay.neighbors_and_costs.items():
            print("           ",item.ip,item.port,"avec un cout de",key)