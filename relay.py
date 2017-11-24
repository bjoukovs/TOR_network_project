from random import randint

class Relay:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.neighbors=[]

    def connect(self,target_relay,sync):
        cost=randint(1,9)
        sync=sync+1
        self.neighbors.append([target_relay,cost])
        if sync <=1:
            target_relay.connect(self,sync)
        return 0
