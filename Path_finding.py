
Permanent_nodes = []
Temporary_nodes = []
New_permanent_nodes = []
New_permanent_link = []

#temporynode: ((son numero, )
def Dijkstra(departure, arrival):
    Permanent_nodes.append(departure)
    Temporary_nodes.append(departure.relay_list)
    
    
    
    return 0 

#each relay have a matrix (n-1)*2 where n is the number of relay
#and 1st culumn is the next relay and the 2nd one is the cost between the
#actual one and the target

#function which gives the cost of the path, the entry is path_list which is a list
#with all the relays (just the number of the relay) contain in the path. Warning,
#the relay has to be in the exact order of the path in that list, otherwise we connot
# know the cost between them
def cost_path(path_list):
    total_cost = 0
    for i in length(path_list):
        next_relay = path_list[i+1]
        total_cost = total_cost + path_list[i].relay_list[next_relay][1]    
    return total_cost