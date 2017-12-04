#This file will contain the code to read the relay config host.ini file

config_url = 'config/host.ini'

def read_config():
    host_file = open(config_url,'r')
    host_config = host_file.read().splitlines()
    host_file.close()

    ip = "0.0.0.0"
    port = 0

    for line in host_config:
        if len(line)>0:
            if line[0]!="#" and line[0]!="[" and line[0]!=" ":
                elems = line.split(" ")

                ip = elems[0]
                port = int(elems[1])
    
    return [ip, port]