import socket
import select
from threading import Thread

class Relay(Thread):

    def __init__(self,IP,PORT):
        self._IP = IP
        self._PORT = PORT
        self._udp_socket = None
        self._thread_running = False


    def create_udp_socket(self):
        print("Initializing UDP socket on",self._IP,self._PORT,'...',end='')
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._udp_socket.bind((self.IP,self.PORT))
        self._udp_socket.setblocking(0)


    def activate(self):
        print("Start listening...",end='')
        if self._udp_socket == None:
            print("ERROR : SOCKET NOT INITIALIZED")
        else:
            Thread.__init__(self)
            self._thread_running = True
            self.start()
            while self.isAlive()==False:
                pass
            print("OK")


    def desactivate(self):
        print("Stop listening...",end="")
        self._thread_running = False
        while self.isAlive()==True:
            pass
       
        print("OK")


    def close_udp_socket(self):
        print("Closing UDP socket...",end='')
        if self.isAlive()==True:
            print("ERROR : THREAD STILL LISTENING, DESACTIVATE() FIRST")
        else:
            self._udp_socket.close()
            print("OK")



    def message_received(self,data,addr):
        print()
        print("Message received from",addr)
        print(data)
        print()


    @property
    def IP(self):
        return self._IP

    @property
    def PORT(self):
        return self._PORT

    @property
    def udp_socket(self):
        return self.udp_socket
    #UDP IPv4 Socket


    #FONCTION DU THREAD
    def run(self):
        while self._thread_running:

            #Des que le socket a du data disponible, ready[0] devient true et on récupère le message reçu.
            #Cependant, il y a un timeout de 1 seconde, ce qui permet que si aucune donnée n'est arrivée dans la seconde, la boucle recommence.
            #Sans cette manipulation, il serait impossible de fermer le thread (_thread_running = false) parce que la commande recv_from est une commande bloquante
            ready = select.select([self._udp_socket], [], [], 1)
            if ready[0]:
                data, addr = self._udp_socket.recvfrom(1024)
                self.message_received(data,addr)