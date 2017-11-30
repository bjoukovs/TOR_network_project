import socket
import select
from threading import Thread

class Relay(Thread):

    def __init__(self,IP,PORT):
        self._IP = IP
        self._PORT = PORT
        self._tcp_socket = None
        self._thread_running = False
        self._active_clients = []

    def create_tcp_socket(self):
        print("Initializing TCP socket",self.IP,self.PORT,end="...")
        self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_socket.bind((self.IP, self.PORT))
        self._tcp_socket.setblocking(0)
        print("OK")

    def activate_tcp_socket(self):
        
        self._tcp_socket.listen(1)
        print("Start listening...",end='')
        if self._tcp_socket == None:
            print("ERROR : SOCKET NOT INITIALIZED")
        else:
            Thread.__init__(self)
            self._thread_running = True
            self.start()

            #Wait for thread being lauched
            while self.isAlive()==False:
                pass
            print("OK")

    def desactivate_tcp_socket(self):
        print("Stop listening...",end="")
        self._thread_running = False

        #Wait for thread being terminated
        while self.isAlive()==True:
            pass
       
        print("OK")


    def close_tcp_socket(self):
        print("Closing TCP socket...",end='')
        if self.isAlive()==True:
            print("ERROR : THREAD STILL LISTENING, DESACTIVATE_TCP_SOCKET() FIRST")
        else:
            self._tcp_socket.close()
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
    def tcp_socket(self):
        return self._tcp_socket
    #UDP IPv4 Socket


    #FONCTION DU THREAD
    def run(self):
        while self._thread_running:

            #Des que le socket a du data disponible, readable contient alors la liste des sockets ayant du data.
            #Cependant, il y a un timeout de 1 seconde, ce qui permet que si aucune donnée n'est arrivée dans la seconde, la boucle recommence.
            #Sans cette manipulation, il serait impossible de fermer le thread (_thread_running = false) parce que la commande accept() est bloquante
            readable,_,_ = select.select(self._active_clients + [self._tcp_socket] , [], [], 1)

            for s in readable:
                
                if s is self._tcp_socket:
                    client_socket, address = self._tcp_socket.accept()
                    self._active_clients.append(client_socket)
                    print("Connection from", address)

                else:
                    data = s.recv(1024)
                    print(data)
                    if data:
                        s.send(data)
                    else:
                        s.close()
                        self._active_clients.remove(s)