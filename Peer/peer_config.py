#This file will contain the code to read the topology config file
from relay import Relay
from random import randint

config_url = "config/topology.ini"

def read_config():
    topology_file = open(config_url,'r')
    topology_config = topology_file.read().splitlines()
    topology_file.close()

    relays = {}
    read_mode = 0

    for line in topology_config:
        if line=="[relays]":
            read_mode = 1
        elif line=="[topology]":
            read_mode = 2

        if len(line)>0:
            if line[0]!="#" and line[0]!="[" and line[0]!=" ":
                elems = line.split(" ")

                #Lecture relais
                if read_mode==1:
                    ip = elems[0]
                    port = elems[1]

                    if relays.get(ip)==None:
                        relays[ip] = []

                    relays[ip].append(Relay(ip,port))

                #Lecture topology
                elif read_mode==2:
                    source_ip = elems[0]
                    relays_source = relays[source_ip]

                    dests = elems[1:]

                    #Pour chaque relais ayant source_ip comme adresse IP, le connecter avec tous les autres relais ayant une adresse IP contenue dans dests
                    for dest_ip in dests:

                        #Cout de connection aléatoire
                        cost = randint(1,16)

                        for relay_source in relays_source:
                            for relay_dest in relays[dest_ip]:
                                relay_source.connect(relay_dest,cost)

    return relays