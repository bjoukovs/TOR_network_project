from pynput.keyboard import Key, Listener
import os,sys,inspect
import atexit

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.Relay import Relay
from shared.config.host_config import read_config

data = read_config()
IP = data[0]    #String
PORT = data[1]  #Integer

print("Initializing relay...",end='')
relay = Relay(IP,PORT)
print("OK")
print("Relay initialized:",relay.IP,relay.PORT)

relay.create_server_socket()
relay.activate_server_socket()

print("----------------------------")
print("Press ESC to close the relay")
print("----------------------------")

#Fonction qui s'execute quand on appuye sur une touche
def close_relay():
    relay.desactivate_server_socket()
    relay.close_server_socket()
    exit()

atexit.register(close_relay)

def onPress(key):
    if key == Key.esc:
        print("CLOSE RELAY REQUEST BY USER")
        close_relay()

with Listener(on_press = onPress) as listener:
    listener.join()