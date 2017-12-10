import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.Relay import Relay
from shared.Path_finding_V3 import Dijkstra
from shared.config.relay_object import Relay as Relay_object
from shared.security import *
from shared.shallot import *
from copy import *
from shared.Message import Message
from random import *


class Peer(Relay):

    def __init__(self,ip,port,topology):
        super().__init__(ip,port)

        self.linked_gui = None
        self.network_topology = topology

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

        #METTRE LE CODE PERMETTANT D'ENVOYER UN MESSAGE A BOB + LA NEGOCIATION DES CLES
        #UTILIER LA COMMANDE self.send_datagram() pour enoyer des paquets à des clients connectés

    def message_received(self,data,client):
        #Quelque chose de ce genre là
        decrypted = super().message_received(data,client)

        #Faire un test pour voir si le message est bien un message destiné à Alice
        self.linked_gui.receive_message(decrypted,IP_BOB,PORT_BOB)
