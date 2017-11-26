Load_list = [] #liste ou chaque elem à 3 composants (matrice (n+2)*3) premier elem:
               #le n° du noeud; 2eme elm: le poids du noeud; 3eme elem: v/f pour savor si oui ou non on est passé par ce noeud
Past_list = [] #liste ou chaque elem à 2 composants (matrice (n+2)*2) premier elem: le n° du noeud
                #2eme noeud donne le noeud antérieur: d'ou viens chaque noeud

#Il faut créer la liste des voisin de chaque noeuds
    Neighbour_list = []#liste (n+1)*(p*x) ou n est le nombre de noeud alice compris mais pas bob...
                       #et p le nmbre de voisin de chaque noeud et x le cout entre les deux relays adjacents
                       #ex: Neighbour_list = [(A,(R1,c1),(R2,c2),(R3,c3)) , (R1,(A,c1),(R4,c4),(R5,c5)) , ...]
                       #Elle doit sortir de l'objet network mais comment?
Final_path = [] #liste contenant le trajet final de moindre cout

def Dijkstra(departure, arrival, network):

    #je considère le point de départ (Alice) comme un relay à la position 0 et l'arrivée
    #(Bob) comme un relay à la position n+1 donc la liste de relay est de longeur n + 2 avec
    #node[0] = depart et node[n+1] = arrivée

    #initization
    #Pour le point de départ
    Load_list[0][0] = 0 #premier relay
    Load_list[0][1] = 0 #son cout est forcément nul puisque l'on part de celui-ci
    Load_list[0][2] = True #on a forcement parcouru le départ: on y est
    Past_list[0][0] = 0 #premier relay
    Past_list[0][1] = None #il n'a pas d'atécédent, c'est la source

    #Pour tout les relays intermédiaires
    n = get_number_of_nodes
    for i = 1:1:n:
        Load_list[i][0] = i
        Load_list[i]][1] = unknow #mise du poids à infini, unknow valable? sinon chiffre arbitrairement grand 1000
        Load_list[i]][2] = False  #rien n'a encoe été parcouru: tt à False
        Past_list[i][0] = i
        Past_list[i][1] = None #pas encore d'antécéden puisque jamais été parcouru

    #Pour l'arrrivée
    Load_list[n+1][0] = 0
    Load_list[n+1][1] = unknow
    Load_list[n+1][2] = False
    Past_list[n+1][0] = n+1
    Past_list[n+1][1] = None

    Neighbour_list = []#liste (n+1)*(p*x) ou n est le nombre de noeud alice compris mais pas bob...
                       #et p le nmbre de voisin de chaque noeud et x le cout entre les deux relays adjacents
                       #ex: Neighbour_list = [(A,(R1,c1),(R2,c2),(R3,c3)) , (R1,(A,c1),(R4,c4),(R5,c5)) , ...]
                       #


    #Algorithme de path-finding en lui même
    #on doit faire tourner l'algo tant que le noeud ayant le point le plus faible est pas arrival
    #il faut continuer à faire tourner sinon ca veut dire que le chemin le plus court n'est pas celui allant à arrival

    keep_going = True

    while (keep_going == True)
        temp_load_list = []
        for alpha = 1:1:n:
            temp_load_list[alpha] = Load_list[alpha][1]

        if(min(temp_load_list) != Load_list[n+1][1])
            for k 0:1:n:  #je regarde tt les node
                if Load_list[k][2] == True: #je prends tt ceux ou je suis
                    for elem in Neighbour_list[k]:    #je regarde tout ceux a qui il est connecté
                        for beta = 1:1:(len(elem) - 1) #on commence avec 1 pour qu'on soit dans les voisins
                                                        #elem[beta][0] va permettre de selectionner l'ensembe des voisins
                            if Load_list[ elem[beta][0] ][2] == False: #je regarde tt ceux qui n'ont pas encore été parccouru
                                                                        #elem[beta][1] donne le cout de la liaison entre le kieme noeud et son voisin
                                if ((Load_list[k][1] + elem[beta][1]) < Load_list[elem][1]) or (Load_list[elem][1] == unknow)):
                                    #ici on est dans le cas ou le fait de passer par le noeud ou l'on est puis par un des voisins
                                    #de ce noeud est plus interessant que le chemin deja existant(pour aller à ce voisin puisque le load[voisin][1]
                                    # comprend le cout de l'ensemble du chemin jusqu'à lui) OU BIEN que le voisin n'a jamais
                                    #été exploré et donc cest une voie à explorer
                                    Load_list[elem][1] = Load_list[k][1] + elem[beta][1]
                                    Past_list[elem][1] = k
                                    #ici on donne un nouveau cout au fait d'aller à ce voisin ET ON dit d'ou vient le pas antérieur, d'ou arrive
                                    #le chemin
        else:
            keep_going = False

    #sors de la boucle
    #on doit remonter l'antécedant de chaque membre en noeud en partant du point d'arrivée

    previous_step = n + 1 #l'arrivée
    while (previous_step != 0)
        Final_path.append(previous_step)
        previous_step = Past_list[previous_step][1] #on prends l'antécédent du previous step

    Final_path.append(0) #on lui met le dernier pas qui est le départ...

    #Maintenant il faut inverser la liste pour que le prmier terme soit le départ et pas l'arrivée
    Final_path = Final_path.reverse()

    return Final_path
