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

class KEY_REPLY(Message):
    def __init__(self,version,type_,msg_length,key_id,B):
        Message.__init__(self,version,type_)
        self.msg_length=msg_length
        self.key_id=key_id
        self.B=B

class MESSAGE_RELAY(Message):
    def __init__(self,version,type_,seq_nb,key_id,nexthop,payload,padding):
        Message.__init__(self,version,type_)
        self.seq_nb=seq_nb
        self.key_id=key_id
        self.nexthop=nexthop
        self.payload=payload
        self.padding=padding

class ERROR(Message):
    def __init__(self,version,type_,msg_length,error_code,padding):
        Message.__init__(self,version,type_)
        self.msg_length=msg_length
        self.error_code=error_code
        self.padding=padding