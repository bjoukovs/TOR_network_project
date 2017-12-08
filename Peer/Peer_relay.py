import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.Relay import Relay


class Peer(Relay):

    def __init__(self,ip,port,topology):
        super().__init__(ip,port)

        self.linked_gui = None
        self.network_topology = topology


    def link_gui(self,GUI):
        self.linked_gui = GUI

    def send_message(self,message,ip,port):
        pass
        #METTRE LE CODE PERMETTANT D'ENVOYER UN MESSAGE A BOB
        #UTILIER LA COMMANDE self.send_datagram()

    def message_received(self,data,client):
        #Quelque chose de ce genre là
        decrypted = super().message_received(data,client)

        #Faire un test pour voir si le message est bien un message destiné à Alice
        self.linked_gui.receive_message(decrypted,IP_BOB,PORT_BOB)
