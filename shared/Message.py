class Message:
    def __init__(self,version,type_):
        self.version=version
        self.type_=type_

class KEY_INIT(Message):
    def __init__(self,version,type_,msg_length,key_id,g,p,A):
        Message.__init__(self,version,type_)
        self.msg_length=msg_length
        self.key_id=key_id
        self.g=g
        self.p=p
        self.A=A
    def concatene(self):
        corpus=(bin(self.version)[2:]+bin(self.type_)[2:]+'00000000'+bin(self.msg_length)[2:]+bin(self.key_id)[2:]
                +bin(self.g)[2:]+bin(self.p)[2:]+bin(self.A)[2:])
        return corpus

class KEY_REPLY(Message):
    def __init__(self,version,type_,msg_length,key_id,B):
        Message.__init__(self,version,type_)
        self.msg_length=msg_length
        self.key_id=key_id
        self.B=B
    def concatene(self):
        corpus=(bin(self.version)[2:]+bin(self.type_)[2:]+'00000000'+bin(self.msg_length)[2:]+bin(self.key_id)[2:]
                +bin(self.B)[2:])
        return corpus

class MESSAGE_RELAY(Message):
    def __init__(self,version,type_,seq_nb,key_id,nexthop,payload):
        #nexthop=tuple contenant (IP,port) sur 16 bits chacun
        Message.__init__(self,version,type_)
        self.seq_nb=seq_nb
        self.key_id=key_id
        self.nexthop_ip=nexthop[0]
        self.nexthop_port=nexthop[1]
        self.payload=payload
        #self.padding=padding #le padding va etre fait dans la fct concatene et n'est plus un attribut
    def part_non_cipher(self):
        corpus=(bin(self.version)[2:]+bin(self.type_)[2:]+'00000000'+bin(self.seq_nb)[2:]+bin(self.key_id)[2:]
                +self.nexthop_ip) #on considere que nexthop est un nombre binaire en string deja
        return corpus

    def part_to_cipher(self):
        corpus=self.nexthop_port+self.payload
        residual=len(corpus)%32
        if residual!=0:
            for i in range(0,residual):
                corpus=corpus+'0'
        return corpus

class ERROR(Message):
    def __init__(self,version,type_,msg_length,error_code):
        Message.__init__(self,version,type_)
        self.msg_length=msg_length
        self.error_code=error_code
        #self.padding=padding  #padding fait dans concatene
    def concatene(self):
        corpus=(bin(self.version)[2:]+bin(self.type_)[2:]+'00000000'+bin(self.msg_length)[2:]+bin(self.error_code)[2:])
        if residual!=0:
            for i in range(0,residual):
                corpus=corpus+'0'
        return corpus
