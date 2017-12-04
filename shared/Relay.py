import socket
import select
from threading import Thread

class Relay(Thread):

    def __init__(self,IP,PORT):
        self._IP = IP
        self._PORT = PORT
        self._server_socket = None
        self._thread_running = False
        self._active_clients = []

    def create_tcp_socket(self):
        print("Initializing TCP socket",self.IP,self.PORT,end="...")
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self.IP, self.PORT))
        self._server_socket.setblocking(0)
        print("OK")

    def activate_tcp_socket(self):
        
        self._server_socket.listen(1)
        print("Start listening...",end='')
        if self._server_socket is None:
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
            print("ERROR : THREAD STILL LISTENING, DESACTIVATE_server_socket() FIRST")
        else:
            self._server_socket.close()
            print("OK")



    def message_received(self,data,client):
        print()
        print("Message received from",client.getpeername())
        print(data)
        print()
        #TEST
        #self.send_datagram(data,client)


    def send_datagram(self, data, client):
        client.send(data)
        print()
        print("Message sent to",client.getpeername())
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
        return self._server_socket
    #UDP IPv4 Socket


    #FONCTION DU THREAD
    def run(self):
        while self._thread_running:

            #Des que le socket a du data disponible, readable contient alors la liste des sockets ayant du data.
            #Cependant, il y a un timeout de 1 seconde, ce qui permet que si aucune donnée n'est arrivée dans la seconde, la boucle recommence.
            #Sans cette manipulation, il serait impossible de fermer le thread (_thread_running = false) parce que la commande accept() est bloquante
            readable,_,_ = select.select(self._active_clients + [self._server_socket] , [], [], 1)

            for sock in readable:
                
                #Si le socket qui a reçu un message est _server_socket alors il s'agit d'une demande de connexion
                if sock is self._server_socket:
                    client_socket, address = self._server_socket.accept()
                    self._active_clients.append(client_socket)
                    print("New client connected", address)

                #Sinon il s'agit du socket d'un client connecté qui désire envoyer un message
                else:
                    data = sock.recv(1024)
                    
                    #Si data est non vide il s'agit d'un message
                    if data:
                        self.message_received(data,sock)

                    #Si data est vide cela veux dire fin de connexion
                    else:
                        addr = sock.getpeername()
                        sock.close()
                        self._active_clients.remove(sock)
                        print("Client disconnected",addr)