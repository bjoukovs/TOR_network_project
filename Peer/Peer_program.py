from pynput.keyboard import Key, Listener
from tkinter import Tk
from peer_gui import Peer_gui
from Peer_relay import Peer
import atexit

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.Relay import Relay as Relay
from shared.config.peer_config import read_config as read_config_peer
from shared.config.host_config import read_config as read_config_host
from shared.config.relay_object import Relay as Relay_object

host_data = read_config_host()

## MAIN VARIABLES ##
IP = host_data[0]    #String
PORT = host_data[1]  #Integer
TOPOLOGY = read_config_peer()

#Manual topology for less than 3 computers
Alice = Relay_object("192.168.0.10",9000)
Bob = Relay_object("192.168.0.24",9999)
r1 = Relay_object("192.168.0.24",9001)
r2 = Relay_object("192.168.0.24",9002)
Alice.connect(r1,5)
r1.connect(r2,5)
r2.connect(Bob,5)
TOPOLOGY = {}
TOPOLOGY["192.168.0.10"] = [Alice]
TOPOLOGY["192.168.0.24"] = [r1,r2,Bob]


PEER = Peer(IP,PORT,TOPOLOGY) #Objet peer héritant de la classe Relay

#Initialisation du relais interne du peer
PEER.create_server_socket()
PEER.activate_server_socket()

def close_peer():
    PEER.desactivate_server_socket()
    PEER.close_server_socket()
    exit()

atexit.register(close_peer)

#####
#ECRIRE LE CODE A TESTER ICI

#Interface graphique
GUI = Tk()
GUI.geometry("400x300+300+300")
app = Peer_gui(PEER)
GUI.mainloop() 

#####

close_peer()