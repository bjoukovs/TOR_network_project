#Objet relais : utile pour gerer les connections

from random import randint

class Relay:
    def __init__(self,ip,port):
        self._ip=ip
        self._port=port
        self.connections_costs={}
        self.connections_visited={}

    def connect(self,target_relay,cost):

        #Definir une connection uniquement si elle n'existe pas encore
        if self.connections_costs.get(target_relay)==None:
            
            #Defini la connexion reciproque avec un cout egal
            self.connections_costs[target_relay] = cost
            self.connections_visited[target_relay] = False
            target_relay.connect(self,cost)

    @property
    def neighbours_visited(self):
        return self.connections_visited

    @property
    def neighbors_and_costs(self):
        return self.connections_costs

    @property
    def ip(self):
        return self._ip
    
    @property 
    def port(self):
        return self._port

    def get_cost(self,neighbor):
        return self.connections_costs[neighbor]

    def get_port(self):
        return self.port
