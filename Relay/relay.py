from relay_config import read_config
from relay_thread import Relay
from pynput.keyboard import Key, Listener


data = read_config()
IP = data[0]    #String
PORT = data[1]  #Integer

print("Initializing relay...",end='')
relay = Relay(IP,PORT)
print("OK")
print("Relay initialized:",relay.IP,relay.PORT)

relay.create_tcp_socket()
relay.activate_tcp_socket()

print("----------------------------")
print("Press ESC to close the relay")
print("----------------------------")

#Fonction qui s'execute quand on appuye sur une touche
def onPress(key):
    if key == Key.esc:
        print("CLOSE RELAY REQUEST BY USER")
        relay.desactivate_tcp_socket()
        relay.close_tcp_socket()
        exit()

with Listener(on_press = onPress) as listener:
    listener.join()

