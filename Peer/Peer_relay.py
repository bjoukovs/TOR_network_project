import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.Relay import Relay
from shared.Path_finding_V3 import Dijkstra
from shared.config.relay_object import Relay as Relay_object
from shared.Message import MESSAGE_RELAY, KEY_INIT, Message
from shared.security import DH_exchange
from shared.shallot import *
from random import *
import socket

class Peer(Relay):

    def __init__(self,ip,port,topology):
        super().__init__(ip,port)

        self.linked_gui = None
        self.network_topology = topology
        self.is_peer = True

        #Selection du relais qui correspond au peer
        self.relay_object = Relay_object.select_relay(topology,ip,port)
        print(self.relay_object)
        


    def link_gui(self,GUI):
        self.linked_gui = GUI

    def send_message(self,message,ip,port):
        #Selection du relay_object de topology correspondant à BOB
        dest_relay = Relay_object.select_relay(self.network_topology,ip,port)
        if dest_relay is None:
            print("--- ERROR : Destination not in topology ---")

        else:
            #Attention hops contient aussi Alice
            hops = Dijkstra(self.relay_object,dest_relay,self.network_topology)
            ls_keys = self.negociate_keys(hops)
            message_to_send = build_shallot(hops,ls_keys,message)
            
            sock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_STREAM) # TCP
            sock.connect((hops[1].IP,hops[1].PORT))
            sock.sendall(message)
            sock.close()


        #METTRE LE CODE PERMETTANT D'ENVOYER UN MESSAGE A BOB + LA NEGOCIATION DES CLES
        #UTILIER LA COMMANDE self.send_datagram() pour enoyer des paquets à des clients connectés

    def send_to_next_hop(self,decrypted):
        print('Overrided')
        next_hop_ip_received, next_hop_port_received = MESSAGE_RELAY.get_next_hop(decrypted)
        
        #If IP and PORT correspond to the Peer's address, then the message is arrived at destination
        if next_hop_ip_received == self.IP and next_hop_port_received == self.PORT:
            print("MESSAGE ARRIVED AT DESTINATION")
        else:
            super().send_to_next_hop(decrypted)


    def message_received(self,data,client):
        
        payload, msg_type = self.open_message(data,client)

        #Message Key_reply
        if msg_type==1:
            key_reply = KEY_REPLY.init_from_msg(payload)
            self.key_buffer = key_reply.B

        else:
            decrypted = super().message_received(data,client,True,payload,msg_type)

            if decrypted is not None:
                self.linked_gui.receive_message(decrypted)


    def negociate_keys(self,hops):
        ls_keys=[]

        #hops[0] is Alice
        for i in range(1,len(hops)):
            p=generate_prime_nb(1024)
            g=2
            a=generate_random_nb(8)
            A = DH_exchange(g,a,p)
            key_id = getrandbits(32)

            key_init = KEY_INIT(key_id,g,p,A)
            message = key_init.byte_form()

            self.key_buffer = None
            #Blocked until key_buffer is not None
            B = self.negociate_key_with_relay(hops[i],message)

            key = DH_shared_secret(B,a,p)
            key=str(key)
            #key_id=generate_random_nb(32) #Does not generate exactly 32 bits every time
            #print(len(bin(key_id)))
            temp=(key_id,key)
            ls_keys.append(temp)

        return ls_keys


    def negociate_key_with_relay(self,relay,message):
        sock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_STREAM) # TCP
        
        print(relay.ip, relay.port)
        sock.connect((relay.ip,relay.port))
        sock.sendall(message)

        #Wait for key reply response
        while self.key_buffer is None:
            pass

        sock.close()
        return self.key_buffer

