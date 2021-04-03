"""
	Jeu des bâtonnets

	joueur = 1  => ordinateur
	joueur = -1 => humain
"""

# Constantes globales

# RECOMPENSE = valeur donnée à un état terminal dans une partie gagnée
# si la partie est perdue, la valeur est -RECOMPENSE.
# Toutes les valeurs minimax sont comprises dans [-RECOMPENSE, RECOMPENSE]
RECOMPENSE = 1


def affiche(N):
    # Affichage du jeu
    s = ""
    for i in range(N):
        s = s + "|"
    print(s)


def humainJoue(N):
    # Retourne le coup joué par l'humain
    coups = coupsPossibles(N)

    print("choix possibles : ")
    print(coups)

    n = None
    while n not in coups:
        n = int(input("combien de bâtonnets ? "))
    return n


def ordiJoue(N):
    # Retourne le coup joué par l'ordinateur

    # Détermination du meilleur coup

    #Version sans alpha beta
    #coups = [[valeurMin(N - i), i] for i in range(1, len(coupsPossibles(N)) + 1)]

    #Version avec
    #On initialise alpha et beta à -infini et +infini respectivement
    #On calcule le score de chaque coups possible, en associant le coup correspondant à chaque
    #fois
    coups = [[valeurMinAlphaBeta(N - i, -2, 2), i] for i in range(1, len(coupsPossibles(N)) + 1)]

    #On extrait les scores pour calculer le max
    valeursCoups = [coups[i][0] for i in range(len(coups))]
    maxScore = max(valeursCoups)

    return coups[valeursCoups.index(maxScore)][1]


def coupsPossibles(N):
    coups = []
    for i in range(1, 4):
        if i <= N:
            coups.append(i)

    return coups


def valeurMax(N):

    global nbNoeudsExplores

    #On est dans une feuille de l'arbre
    if N == 0:
        #L'ordi a gagné, donc récompense positive
        return RECOMPENSE
    # On est dans une branche de l'arbre
    else:
        #On initialise la valeur max à -infini (le pire des cas pour l'ordinateur)
        maxEval = -2
        coups = len(coupsPossibles(N))
        i = 1
        while i <= coups:
            nbNoeudsExplores += 1
            #On évalue le coups actuel
            currentEval = valeurMin(N - i)
            #On remplace la valeur max actuelle SI le coup en cours d'évaluation donne un score plus élevé
            maxEval = max(maxEval, currentEval)
            i += 1
    return maxEval


def valeurMin(N):

    global nbNoeudsExplores

    if N == 0:
        # L'ordi a perdu, donc récompense négative
        return -RECOMPENSE
    else:
        # On initialise la valeur min à +infini (le meilleur des cas pour l'adversaire)
        minEval = 2
        coups = len(coupsPossibles(N))
        i = 1
        while i <= coups:
            nbNoeudsExplores += 1
            currentEval = valeurMax(N - i)
            minEval = min(minEval, currentEval)
            i += 1
    return minEval

def valeurMaxAlphaBeta(N, alpha, beta):

    global nbNoeudsExplores

    if N == 0:
        return RECOMPENSE
    else:
        maxEval = -2
        coups = len(coupsPossibles(N))
        i = 1
        #On s'arrête si le coup actuellement étudié (alpha) est plus grand que la valeur minimale actuelle (beta)
        #Si oui, alors cette partie de l'arbre ne sera jamais atteinte, donc inutile de la parcourir
        while i <= coups and beta > alpha:
            nbNoeudsExplores += 1
            currentEval = valeurMinAlphaBeta(N - i, alpha, beta)
            maxEval = max(maxEval, currentEval)
            alpha = max(alpha, currentEval)
            i += 1
    return maxEval

def valeurMinAlphaBeta(N, alpha, beta):

    global nbNoeudsExplores

    if N == 0:
        return -RECOMPENSE
    else:
        minEval = 2
        coups = len(coupsPossibles(N))
        i = 1
        while i <= coups and beta > alpha:
            nbNoeudsExplores += 1
            currentEval = valeurMaxAlphaBeta(N - i, alpha, beta)
            minEval = min(minEval, currentEval)
            beta = min(beta, currentEval)
            i += 1
    return minEval




######### Programme principal ##########

# Etat initial
N = 27

# Qui commence ?
joueur = int(input("Qui commence ? (1 pour ordinateur, -1 pour humain) "))

# Boucle de jeu (tant que la partie n'est pas finie)
while N > 0:
    # afficher l'état du jeu:
    affiche(N)

    if joueur == -1:
        n = humainJoue(N)
    else:
        nbNoeudsExplores = 0
        n = ordiJoue(N)
        print("(après une réflexion basée sur l'exploration de " + str(nbNoeudsExplores) + " noeuds)")
        print("je prends " + str(n) + " batonnets")

    # jouer le coup
    N = N - n

    # passer à l'autre joueur:
    joueur = -joueur

# affichage final:
affiche(N)
if joueur == 1:
    print("PERDU (ordi a gagné) !")
else:
    print("GAGNE (ordi a perdu) !")
