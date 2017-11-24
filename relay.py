from random import randint

class Relay:
    def __init__(self,ip,port):
        self._ip=ip
        self._port=port
        self._neighbors_costs={}

    def connect(self,target_relay,sync,cost=0):
        
        sync=sync+1
        if sync <=1:
            cost=randint(1,9)
            target_relay.connect(self,sync,cost)

        self._neighbors_costs[target_relay] = cost


    @property
    def neighbors(self):
        return self._neighbors_costs

    def get_cost(self,neighbor):
        return self._neighbors_costs[neighbor]
