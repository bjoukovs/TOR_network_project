
Permanent_nodes = []
Temporary_nodes = []
New_permanent_nodes = []
New_permanent_link = []
Nodes = [] #y mettre tout les relays disponibles du network
N_tild = []#set of nodes whose least cost path definitively known
Cost = [] #liste de 0 de taille = au nb de relay dans le network, l'elem i de la liste
#est le cout pour aller depuis le ponit de départ au noeud i.

#temporynode: ((son numero, le cout actuel depuis le début du chemin),la provenance: pas antérieur)
#departure and arrival are peers, but they have the same cara than a relay: a relay_list,
#all his neighbour
def Dijkstra(departure, arrival, network):
    #initialize phase
    # #the departure is automatically a permanent node
    # Permanent_nodes.append(departure)
    # #all neighbour  of the deart (memeber of the his relay list) is a temporary node
    # for elem in departure.relay_list:
    #     #on ajoute à chaque membre de la relay list son lieu de provenance ici le départ
    #     Temporary_nodes = elem , departure


#? est ce que le port est le numéro du relay?

    #initialize phase
    N_tild.append(departure)
    for node in Nodes:
        for elem in departure.relay_list:
            if elem == node:
                Cost(elem.port) = cost_path(path_list, departure, node)
            else:
                Cost(elem.port) = infinity


    n = network.number_of_relay
    while (length(N_tild) < n)
        for node in Nodes:
            if (node in N_tild) == False








    return 0

#each relay have a matrix (n-1)*2 where n is the number of relay
#and 1st culumn is the next relay and the 2nd one is the cost between the
#actual one and the target

#function which gives the cost of the path, the entry is path_list which is a list
#with all the relays (just the number of the relay) contain in the path. Warning,
#the relay has to be in the exact order of the path in that list, otherwise we connot
# know the cost between them
def cost_path(path_list, departure, arrival):
    total_cost = 0
    for i in length(path_list):
        next_relay = path_list[i+1]
        total_cost = total_cost + path_list[i].relay_list[next_relay][1]
    return total_cost
