from peer_config import read_config

data = read_config()

IP = data[0]
PORT = data[1]

TOPOLOGY = data[2]
#The topology will consist of a dictionnary
#The keys are the IP of the relays
#The entries are a list of the neighbors of the key