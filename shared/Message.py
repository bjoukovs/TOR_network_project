#from bitarray import bitarray
from math import ceil
from random import getrandbits

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.config.relay_object import Relay as Relay_object

class Message:
    def __init__(self,version,type_,msg_id=0):
        '''Arguments: [int] version (must be 1), [int] type = message type (KEY_INIT,KEY_REPLY,...). '''
        self.version=version
        self.type_=type_
        self.msg_id=msg_id

    @staticmethod
    def int_bytes(x,length):
        '''Return length bytes corresponding to x with big byte order. '''
        return x.to_bytes(length,byteorder='big')

    @staticmethod
    def bytes_int(b):
        '''Return the integer value corresponding to bytes b with big byte order. '''
        return int.from_bytes(b,byteorder = 'big')

    def byte_form(self):
        '''Return the message in his byte form with all the attributes concatenated. '''
        byte_message = Message.int_bytes(self.version*16+self.type_,1) + Message.int_bytes(self.msg_id,1)
        return byte_message

    # @staticmethod
    # def bits_repr(bytes_form):
    #     '''Return the bit representation of the given bytes in a string. '''
    #     temp = bitarray()
    #     temp.frombytes(bytes_form)
    #     return temp.to01()


#class KEY_INIT(Message):
#    def __init__(self,version,type_,msg_length,key_id,g,p,A):
#        Message.__init__(self,version,type_)
#        self.msg_length=msg_length
#        self.key_id=key_id
#        self.g=g
#        self.p=p
#        self.A=A
#    def concatene(self):
#        corpus=(bin(self.version)[2:]+bin(self.type_)[2:]+'00000000'+bin(self.msg_length)[2:]+bin(self.key_id)[2:]
#                +bin(self.g)[2:]+bin(self.p)[2:]+bin(self.A)[2:])
#        return corpus

class KEY_INIT(Message):
    def __init__(self,key_id,g,p,A):
        '''Arguments: [int] key_id, [int] g, [int] p, [int] A. '''
        Message.__init__(self,1,0,getrandbits(8))
        self.msg_length=67 #dword
        self.key_id=key_id
        self.g=g
        self.p=p
        self.A=A

    def byte_form(self):
        '''Return the message in his byte form with all the attributes concatenated. '''
        byte_message = super().byte_form()
        byte_message += (Message.int_bytes(self.msg_length,2) + Message.int_bytes(self.key_id,4) + Message.int_bytes(self.g,4)
                        + Message.int_bytes(self.p,128) + Message.int_bytes(self.A,128))
        return byte_message

    @classmethod
    def init_from_msg(cls,msg):
        '''Construct a KEY_INIT object based on the provided message (supposed starting from key_id). '''
        return cls(Message.bytes_int(msg[:4]),Message.bytes_int(msg[4:8]),Message.bytes_int(msg[8:136]),Message.bytes_int(msg[136:]))



#class KEY_REPLY(Message):
#    def __init__(self,version,type_,msg_length,key_id,B):
#        Message.__init__(self,version,type_)
#        self.msg_length=msg_length
#        self.key_id=key_id
#        self.B=B
#    def concatene(self):
#        corpus=(bin(self.version)[2:]+bin(self.type_)[2:]+'00000000'+bin(self.msg_length)[2:]+bin(self.key_id)[2:]
#                +bin(self.B)[2:])
#        return corpus

class KEY_REPLY(Message):
    def __init__(self,key_id,B):
        '''Arguments: [int] key_id, [int] B. '''
        Message.__init__(self,1,1,getrandbits(8))
        self.msg_length=34
        self.key_id=key_id
        self.B=B

    def byte_form(self):
        '''Return the message in his byte form with all the attributes concatenated. '''
        byte_message = super().byte_form()
        byte_message += Message.int_bytes(self.msg_length,2) + Message.int_bytes(self.key_id,4) + Message.int_bytes(self.B,128)
        return byte_message

    @classmethod
    def init_from_msg(cls,msg):
        '''Construct a KEY_REPLY object based on the provided message (supposed starting from key_id). '''
        return cls(Message.bytes_int(msg[:4]),Message.bytes_int(msg[5:]))

#class MESSAGE_RELAY(Message):
#    def __init__(self,version,type_,seq_nb,key_id,nexthop,payload):
#        #nexthop=tuple contenant (IP,port) sur 16 bits chacun
#        Message.__init__(self,version,type_)
#        self.seq_nb=seq_nb
#        self.key_id=key_id
#        self.nexthop_ip=nexthop.ip
#        self.nexthop_port=nexthop.port
#        self.payload=payload
#        #self.padding=padding #le padding va etre fait dans la fct concatene et n'est plus un attribut
#    def part_non_cipher(self):
#        corpus=(bin(self.version)[2:]+bin(self.type_)[2:]+'00000000'+bin(self.seq_nb)[2:]+bin(self.key_id)[2:])
#        return corpus
#
#    def part_to_cipher(self):
#        corpus=self.nexthop_ip+self.nexthop_port+self.payload #on considere que nexthop est un nombre binaire en string deja
#        residual=len(corpus)%32
#        if residual!=0:
#            for i in range(0,residual):
#                corpus=corpus+'0'
#        return corpus

class MESSAGE_RELAY(Message):
    def __init__(self,msg_id,seq_nb,key_id,nexthop,previoushop,payload):
        '''Arguments: [int] seq_nb, [int] key_id, [Tuple (IP,port)] nexthop ([String] IP, [int] port),
            [Tuple (IP,port)] nexthop ([String] IP, [int] port), [String||Bytes] payload. '''
        super().__init__(1,2,msg_id)
        self.key_id=key_id
        self.nexthop_ip=nexthop.ip
        self.nexthop_port=nexthop.port
        self.previoushop_ip=previoushop.ip
        self.previoushop_port=previoushop.port
        self.payload=payload
        self.seq_nb = 0 #2 + ceil(len(self.to_cipher())/4)

    def update_length(self,payload):
        self.payload = payload
        length = int(2 + len(self.payload)/4)
        print(len(payload))
        print(length)
        self.seq_nb = length

    def to_cipher(self):
        '''Return the part of the message to cipher in his byte form with all the relevant attributes concatenated. '''
        to_cipher = (bytes([int(elem) for elem in self.nexthop_ip.split('.')]) + Message.int_bytes(self.nexthop_port,4))
        if isinstance(self.payload,str):
            to_cipher += self.payload.encode('utf-8')
        elif isinstance(self.payload,bytes):
            to_cipher += self.payload
        return to_cipher

    def plain_text_part(self):
        '''Return the plain-text part of the message in his byte form with all the relevant attributes concatenated. '''
        byte_message = super().byte_form()
        byte_message += Message.int_bytes(self.seq_nb,2) + Message.int_bytes(self.key_id,4)
        byte_message += bytes([int(elem) for elem in self.previoushop_ip.split('.')]) + Message.int_bytes(self.previoushop_port,4)
        return byte_message

    @staticmethod
    def get_key_id_and_ciphtext(msg):
        '''Return the key ID and the ciphered part of the provided message in a tuple (key ID,ciphered part). '''
        return Message.bytes_int(msg[:4]),msg[12:]

    @staticmethod
    def get_next_hop(decrypted_msg):
        '''Return the next hop IP address of the provided message. '''
        return '.'.join([str(elem) for elem in list(decrypted_msg[:4])]), Message.bytes_int(decrypted_msg[4:8])

    @staticmethod
    def get_previous_hop(msg):
        '''Return the previous hop IP address of the provided message. '''
        return '.'.join([str(elem) for elem in list(msg[4:8])]), Message.bytes_int(decrypted_msg[8:12])

    @staticmethod
    def get_payload(decrypted_msg):
        '''Return the payload of the provided message. '''
        return decrypted_msg[8:]

class ERROR(Message):
    def __init__(self,msg_id,error_code):
        '''Arguments: [int] error_code. '''
        Message.__init__(self,1,3,msg_id)
        self.msg_length=2
        self.error_code=error_code
        #self.padding=padding  #padding fait dans concatene
    def concatene(self):
        corpus=(bin(self.version)[2:]+bin(self.type_)[2:]+'00000000'+bin(self.msg_length)[2:]+bin(self.error_code)[2:])
        if residual!=0:
            for i in range(0,residual):
                corpus=corpus+'0'
        return corpus

    def byte_form(self):
        '''Return the message in his byte form with all the attributes concatenated. '''
        byte_message = super().byte_form()
        byte_message += Message.int_bytes(self.msg_length,2) + Message.int_bytes(self.error_code,2)
        return byte_message

    @staticmethod
    def get_error_code(msg):
        '''Return the error code based on the provided message (supposed starting from error_code). '''
        return Message.bytes_int(msg[:2])
