#This file will contain the code to read the relay config host.ini file

config_url = 'config/host.ini'

def read_config():
    host_file = open(config_url,'r')
    host_config = host_file.read().splitlines()
    host_file.close()

    for line in host_config:
        if len(line)>0:
            if line[0]!="#" and line[0]!="[" and line[0]!=" ":
                elems = line.split(" ")

                IP = elems[0]
                PORT = int(elems[1])
    
    return [IP, PORT]