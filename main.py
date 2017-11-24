from config import read_config

#lecture configuration
data = read_config()
RELAYS = data[0]
TOPOLOGY = data[1]

print("\nDictionnaire des relais : ")
print(RELAYS)
print("\nDictionnaire de la topology : ")
print(TOPOLOGY)