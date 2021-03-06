import socket
import select
from threading import Thread

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.Message import *
from shared.security import *

class Relay(Thread):

    def __init__(self,IP,PORT):
        self._IP = IP
        self._PORT = PORT
        self._server_socket = None
        self._thread_running = False
        self._active_clients = []
        self.dict_keys = {} # Dict with key_id = DH Key
        self.dict_msg = {} # Dict with msg_id = (Previous hop)
        self.is_peer = False

    @property
    def IP(self):
        return self._IP

    @property
    def PORT(self):
        return self._PORT

    @property
    def active_clients(self):
        return self._active_clients

    def create_server_socket(self):
        print("Initializing TCP socket",self.IP,self.PORT,end="...")
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self.IP, self.PORT))
        self._server_socket.setblocking(0)
        print("OK")

    def activate_server_socket(self):
        
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

    def desactivate_server_socket(self):
        print("Stop listening...",end="")
        self._thread_running = False

        #Wait for thread being terminated
        while self.isAlive()==True:
            pass
       
        print("OK")


    def close_server_socket(self):
        print("Closing TCP socket...",end='')
        if self.isAlive()==True:
            print("ERROR : THREAD STILL LISTENING, DESACTIVATE_server_socket() FIRST")
        else:
            self._server_socket.close()
            print("OK")

    
    def send_to_next_hop(self,decrypted):
        next_hop_ip_received, next_hop_port_received = MESSAGE_RELAY.get_next_hop(decrypted)
        print('IP received:',next_hop_ip_received, 'Port received:',next_hop_port_received)
        msg_to_send = MESSAGE_RELAY.get_payload(decrypted)
        IP = next_hop_ip_received
        PORT = next_hop_port_received #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ASK FOR PORT
        sock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_STREAM) # TCP
        sock.connect((IP,PORT))
        sock.sendall(msg_to_send)
        sock.close()

    def open_message(self,data,client):
        # data is the header of the message
        length = (Message.bytes_int(data[2:4]) - 1)*4 # Nb of bytes to read next
        payload = client.recv(length)
        print(data[0])
        print(bin(data[0]))
        msg_version = (data[0] - data[0]%16)/16
        print("Version : ", msg_version)
        msg_type = data[0]%16 # to extract type from version (=1) + type of the header
                                #data[0] est deja un int
        msg_id = data[1] # to extract the message id to send error back if necessary

        print("Message type", msg_type)
        return payload, msg_version, msg_type, msg_id

    def manage_error(self,data,payload,msg_id):
        error_msg = data + payload
        IP, PORT = self.dict_msg[msg_id]
        sock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_STREAM) # TCP
        sock.connect((IP,PORT))
        sock.sendall(error_msg)
        sock.close()

    def send_error(self,msg_id,error_code,client=None):
        error_msg = ERROR(msg_id,error_code).byte_form()
        if client is not None:
            self.send_datagram(error_msg, client)
        else:
            IP, PORT = self.dict_msg[msg_id]
            sock = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_STREAM) # TCP
            sock.connect((IP,PORT))
            sock.sendall(error_msg)
            sock.close()

    def message_received(self,data,client,from_super=False,payload=None,msg_type=None,msg_id=None,msg_version=None):
        
        decrypted = None

        print("message received")

        if from_super==False:
            payload, msg_version, msg_type, msg_id = self.open_message(data,client)

        print(msg_type)

        if msg_type == 0: #KEY_INIT
            if msg_version != 1:
                self.send_error(msg_id,0,client)

            key_init = KEY_INIT.init_from_msg(payload)
            b = generate_random_nb(8)
            key = DH_shared_secret(key_init.A,b,key_init.p)
            self.dict_keys[key_init.key_id] = str(key)

            print("Key received")

            #Send Key reply
            B = DH_exchange(key_init.g,b,key_init.p)
            key_reply = KEY_REPLY(key_init.key_id,B)
            msg_to_send = key_reply.byte_form()
            self.send_datagram(msg_to_send,client)

            print("Reply sent")
       

        elif msg_type == 2: #MESSAGE_RELAY
            key_id_received, ciphered = MESSAGE_RELAY.get_key_id_and_ciphtext(payload)
            self.dict_msg[msg_id] = MESSAGE_RELAY.get_previous_hop(payload)
            print("Previous hop: ",msg_id,self.dict_msg[msg_id])
            print(key_id_received)
            print(self.dict_keys)
            try:
                key = self.dict_keys[key_id_received]
            except Exception as e:
                print("NO KEY",e)
                self.send_error(msg_id,1)
            try:
                decrypted = decrypt(key,ciphered)

                if msg_version != 1:
                    print("BAD VERSION",msg_version)
                    self.send_error(msg_id,0)
                else:
                    self.send_to_next_hop(decrypted)
            except Exception as e:
                print("ERROR",e)
                self.send_error(msg_id,0)

        elif msg_type == 3:
            self.manage_error(data,payload,msg_id)

            
        return(decrypted)


    def send_datagram(self, data, client):
        client.sendall(data)
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
                    port = client_socket.getsockname()
                    client_socket.setblocking(0)
                    self._active_clients.append(client_socket)
                    print("New client connected", address,port)

                #Sinon il s'agit du socket d'un client connecté qui désire envoyer un message
                else:
                    data = sock.recv(4) # Bytes ?
                    print(data)
                    
                    #Si data est non vide il s'agit d'un message
                    if data:
                        self.message_received(data,sock)

                    #Si data est vide cela veux dire fin de connexion
                    else:
                        addr = sock.getpeername()
                        sock.close()
                        self._active_clients.remove(sock)
                        print("Client disconnected",addr)