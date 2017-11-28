from math import inf

def Dijkstra(departure, arrival, network):

    Load_list = {} #liste ou chaque elem à 3 composants (matrice (n+2)*3) premier elem:
               #le n° du noeud; 2eme elm: le poids du noeud; 3eme elem: v/f pour savor si oui ou non on est passé par ce noeud
    Past_list = {} #liste ou chaque elem à 2 composants (matrice (n+2)*2) premier elem: le n° du noeud
                #2eme noeud donne le noeud antérieur: d'ou viens chaque noeud

    nodes = [] #Liste de tous les relais
    for key, relais in network.items():
        for relai in relais:
            nodes.append(relai)

    Final_path = [arrival] #liste contenant le trajet final de moindre cout

    #je considère le point de départ (Alice) comme un relay à la position 0 et l'arrivée
    #(Bob) comme un relay à la position n+1 donc la liste de relay est de longeur n + 2 avec
    #node[0] = depart et node[n+1] = arrivée

    #initization
    #Pour le point de départ
    Load_list[departure] = [0, True] #premier relay
    Past_list[departure] = None #premier relay

    #Pour tout les relays intermédiaires
    for i, node in enumerate(nodes):
        if not(node is arrival) and not(node is departure):
            Load_list[node] = [inf, False]
            Past_list[node] = None

    #Pour l'arrrivée
    Load_list[arrival] = [inf, False]
    Past_list[arrival] = None

    print(Load_list)
    print(Past_list)


    #Algorithme de path-finding en lui même
    #on doit faire tourner l'algo tant que le noeud ayant le point le plus faible est pas arrival (bob)
    #il faut continuer à faire tourner sinon ca veut dire que le chemin le plus court n'est pas celui allant à arrival

    keep_going = True

    for k in range(0,len(nodes)):

        temp_load_list = {}
        for key, val in Load_list.items():
            temp_load_list[key] = val[0] #recupere le load
        
        node_minimum_load = min(temp_load_list,key=temp_load_list.get)
        print(Load_list[network['b'][0]][0])

        if not(node_minimum_load is arrival):
            for node in nodes:  #je regarde tt les node
                if Load_list[node][1] == True: #je prends tt ceux ou je suis

                    neighbours_costs = node.neighbors_and_costs
                    #neighbours_visited = node.neighbours_visited

                    for neighbor, cost_to_neighbor in neighbours_costs.items():    #je regarde tout ceux a qui il est connecté
                        
                        #if neighbours_visited[neighbor] == False: #je regarde tt ceux qui n'ont pas encore été parccouru
                                                                    #elem[beta][1] donne le cout de la liaison entre le kieme noeud et son voisin
                        if ((Load_list[node][0] +  cost_to_neighbor) < Load_list[neighbor][0]) or (Load_list[neighbor][0] == inf):
                            #ici on est dans le cas ou le fait de passer par le noeud ou l'on est puis par un des voisins
                            #de ce noeud est plus interessant que le chemin deja existant(pour aller à ce voisin puisque le load[voisin][1]
                            # comprend le cout de l'ensemble du chemin jusqu'à lui) OU BIEN que le voisin n'a jamais
                            #été exploré et donc cest une voie à explorer
                            Load_list[neighbor][0] = Load_list[node][0] +  cost_to_neighbor
                            Past_list[neighbor] = node
                            #neighbours_visited[neighbor] = True
                            #ici on donne un nouveau cout au fait d'aller à ce voisin ET ON dit d'ou vient le pas antérieur, d'ou arrive
                            #le chemin

                        Load_list[neighbor][1] = True
        else:
            keep_going = False

    #sors de la boucle
    #on doit remonter l'antécedant de chaque membre en noeud en partant du point d'arrivée

    previous_node = Past_list[arrival]
    while not(previous_node is departure): 
        Final_path.append(previous_node)
        previous_node = Past_list[previous_node]

    Final_path.append(departure) #on lui met le dernier pas qui est le départ...

    #Maintenant il faut inverser la liste pour que le prmier terme soit le départ et pas l'arrivée
    Final_path.reverse()

    return Final_path
