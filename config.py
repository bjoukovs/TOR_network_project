from relay import Relay


host_url = "config/host.ini"
topology_url = "config/topology.ini"


def read_config():

    host_file = open(host_url,'r')
    host_config = host_file.readlines()
    host_file.close()

    topology_file = open(topology_url,'r')
    topology_config = topology_file.readlines()
    topology_file.close()

    relays = {}
    topology = {}
    lecture_mode = 0

    #Lecture des relais
    for line in host_config:
        if line=="[relays]":
            lecture_mode = 1
        elif line=="[topology]":
            lecture_mode = 2

        if len(line)>0:
            if line[0]!="#" or line[0]!="[" or line[0]!=" ":
                elems = line.split(" ")

                #Lecture relais
                if read_mode==1:
                    ip = elems[0]
                    port = elems[1]

                    #creation du relay et ajout dans un dictionnaire
                    relay = Relay(ip, port)
                    key = ip
                    relays[key] = relay

                #Lecture topology
                elif read_mode==2:
                    source_ip = elems[0]
                    dests = elems[1:-1]

                    #ajout des connections dans la topologie
                    topology{source_ip} = dests

                    #connection du relais avec ses voisins
                    for dest in dests:
                        relays[source_ip].connect(relays[dest])

    return [relays, topology]


