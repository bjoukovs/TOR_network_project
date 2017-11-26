from relay_config import read_config

data = read_config()
IP = data[0]    #String
PORT = data[1]  #Integer

print("Relay initialized:",IP,PORT)