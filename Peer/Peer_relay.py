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
import time

class Peer(Relay):

    def __init__(self,ip,port,topology):
        super().__init__(ip,port)

        self.linked_gui = None
        self.network_topology = topology
        self.is_peer = True

        #Selection du relais qui correspond au peer
        self.relay_object = Relay_object.select_relay(topology,ip,port)
        print(self.relay_object)

        self.dict_msg = {} #Stock les messages envoyés avec leur id
        


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
            print(hops)
            self.buffered_message = (message,hops)
            self.negociate_keys(hops)

        #METTRE LE CODE PERMETTANT D'ENVOYER UN MESSAGE A BOB + LA NEGOCIATION DES CLES
        #UTILIER LA COMMANDE self.send_datagram() pour enoyer des paquets à des clients connectés

    def when_keys_negociated(self):
        
        message,hops = self.buffered_message
        keys_ordered = [(k,val) for k,val in self.keys.items()]
        keys_ordered.sort(key=lambda x: x[1][4])
        keys_ordered = [(x[0],x[1][3]) for x in keys_ordered]
        print(keys_ordered)

        message_to_send, msg_id = build_shallot(hops,keys_ordered,message)

        self.dict_msg[msg_id] = (self.IP, int(self.PORT))
            
        sock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_STREAM) # TCP
        sock.connect((hops[1].ip,hops[1].port))
        sock.sendall(message_to_send)
        sock.close()

    def send_to_next_hop(self,decrypted):
        print('Overrided')
        next_hop_ip_received, next_hop_port_received = MESSAGE_RELAY.get_next_hop(decrypted)
        
        #If IP and PORT correspond to the Peer's address, then the message is arrived at destination
        if next_hop_ip_received == self.IP and next_hop_port_received == self.PORT:
            print("MESSAGE ARRIVED AT DESTINATION")
        else:
            super().send_to_next_hop(decrypted)

    def manage_error(self,data,payload,msg_id):
        message, ip, port = self.dict_msg[msg_id]
        if ip = self.IP and port = self.PORT:
            print("ERROR RECEIVED")
            print(message)
        else:
            super.manage_error(data,payload,msg_id)

    def message_received(self,data,client):
        
        payload, msg_version, msg_type, msg_id = self.open_message(data,client)

        #Message Key_reply
        if msg_type==1:

            key_reply = KEY_REPLY.init_from_msg(payload)
            key_id = key_reply.key_id
            print("Key reply received")

            B = key_reply.B
            self.keys[key_id][2] = B

            key = DH_shared_secret(self.keys[key_id][2],self.keys[key_id][0],self.keys[key_id][1])#B,a,p
            key=str(key)
            print(key)
            #key_id=generate_random_nb(32) #Does not generate exactly 32 bits every time
            #print(len(bin(key_id)))
            self.keys[key_id][3] = key

            client.close()
            self.active_clients.remove(client)
            print("connection closed")

            all_negociated = True
            for k,val in self.keys.items():
                if val[3] is None:
                    all_negociated = False
                    break
            print(all_negociated)

            print(len(self.keys),self.keys_to_negociate)

            if all_negociated and len(self.keys)==self.keys_to_negociate:
                print("all keys negociated")
                self.when_keys_negociated()


        else:
            decrypted = super().message_received(data,client,True,payload,msg_type,msg_id,msg_version)

            if decrypted is not None:
                final_message = MESSAGE_RELAY.get_payload(decrypted)
                print(final_message)
                self.linked_gui.receive_message(final_message.decode('utf-8'))


    def negociate_keys(self,hops):
        ls_keys=[]
        self.keys = {}
        self.keys_to_negociate = len(hops)-1 #Tous les hops sauf alice

        #hops[0] is Alice
        for i in range(1,len(hops)):
            p=generate_prime_nb(1024)
            g=2
            a=generate_random_nb(8)
            A = DH_exchange(g,a,p)
            key_id = getrandbits(32)

            key_init = KEY_INIT(key_id,g,p,A)
            message = key_init.byte_form()

            self.keys[key_id] = [a,p,None,None,i]

            self.negociate_key_with_relay(hops[i],message)

        #return ls_keys


    def negociate_key_with_relay(self,relay,message):
        sock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_STREAM) # TCP
    
        self.active_clients.append(sock)
        
        print(relay.ip, relay.port)
        sock.connect((relay.ip,relay.port))
        sock.sendall(message)

        #Wait for key reply response
        print("Waiting for key reply")


