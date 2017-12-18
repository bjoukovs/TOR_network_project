from math import inf

def Dijkstra(departure, arrival, network):

    #We are creating 2 dictionnary
    Load_dict = {} #Dictionnary where each key is a relay, or Alice or Bob and to each key
                    #there is a tuple. 1st element: the load of the node: the total
                    #cost in order to get to this node. 2nd element: True/False in
                    #in order to know if the node has already been explored
    Past_dict = {} #Dictionnary where each key is a relay, or Alice or Bob and to each key
                    #it is assign the previous node, from where come from the message
                    #before arriving at this node

    nodes = [] #List with all the relays
    for key, relais in network.items(): #allows to get access to all the nodes of the system
        for relai in relais:
            nodes.append(relai)

    Final_path = [arrival] #List with the least cost path from alice(departure) to Bob (arrival)
                            #we already know that this list contain arrival

    #initization
    #For the departure
    Load_dict[departure] = [0, True] #The cost is null because we begin from this node and we come
                                    #from this node: (True)
    Past_dict[departure] = None #This is the departure, it has no past nodes

    #For all intermediate relays
    for i, node in enumerate(nodes):
        if not(node is arrival) and not(node is departure):
            Load_dict[node] = [inf, False] #The cost for these nodes are infinite because
                                            #we don't reach them yet
            Past_dict[node] = None

    #Pour l'arrrivée
    Load_dict[arrival] = [inf, False]
    Past_dict[arrival] = None


    #The Dijkstra algorithm is a iterative algorithm: after k iterations, we know
    #the least cost path to k destinations. Which mean that we are able to know the
    #least cost path to Bob after the total number of nodes

    keep_going = True

    for k in range(0,len(nodes)):
        #We crate a  dictionnary where each key is a relay to each of them only the
        #load is attribuate
        temp_load_dict = {}
        for key, val in Load_dict.items():
            temp_load_dict[key] = val[0]

        node_minimum_load = min(temp_load_dict,key=temp_load_dict.get)

        #We are only interested when the minimum load is the arrival
        if not(node_minimum_load is arrival):
            #We are looking at every possible nodes
            for node in nodes:
                #But only the nodes where a path already goes to (True for the explored argument)
                if Load_dict[node][1] == True:
                    #We take from the network a dictionnary where the key = a node and for each
                    #key there is all it's neighbors and the cost of the link in order to go to this neighbor
                    neighbours_costs = node.neighbors_and_costs
                    #we are looking in this dictionnary to each neighbor and the cost to go to it
                    for neighbor, cost_to_neighbor in neighbours_costs.items():
                        if ((Load_dict[node][0] +  cost_to_neighbor) < Load_dict[neighbor][0]) or (Load_dict[neighbor][0] == inf):
                            #Here we are in the case if the path trought this node + throught the neighbor is less expencive
                            #than the actual path to the neighbor: indeed the load of the dictionnary contains the cost of all
                            #the path to it. Or the neighbor has never been visited = the new path is obviously least expencive
                            ##
                            #We then fix the new cost for the path which is going to this neighbor, the load part of the load_dic
                            #and the previous node
                            Load_dict[neighbor][0] = Load_dict[node][0] +  cost_to_neighbor
                            Past_dict[neighbor] = node


                        Load_dict[neighbor][1] = True
        else:
            keep_going = False

    #We are now out of the loop, we have to reconstruct this least cost path: we have to
    #get the previous node of each actual node by begining with the arrival and ending
    #withe departure

    previous_node = Past_dict[arrival]
    while not(previous_node is departure):
        Final_path.append(previous_node)
        previous_node = Past_dict[previous_node]

    #The last step is to add the departure to the list
    Final_path.append(departure)

    #We have now to reverse the list in order to get as a first term the departure and not
    #the arrival...
    Final_path.reverse()

    return Final_path
