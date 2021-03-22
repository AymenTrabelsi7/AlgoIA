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

    meilleurCoup = valeurMax(N)  # à modifier...

    return meilleurCoup


def coupsPossibles(N):
    coups = []
    for i in range(1, 4):
        if i <= N:
            coups.append(i)
    return coups


def valeurMax(N):
    """
    Retourne la valeur minimax d'un noeud MAX avec N batônnets

    Si le joueur précédent a perdu (N=0),
        retourne RECOMPENSE car ordi a gagné
    """

    # pour connaître le nombre total de noeuds explorés:
    global nbNoeudsExplores
    nbNoeudsExplores = nbNoeudsExplores + 1

    if N == 0:
        return RECOMPENSE
    else:
        coupsTest = coupsPossibles(N)
        noeuds = [valeurMin(N-i) for i in range(1, len(coupsTest)+1)]
        valeur = max(noeuds)
        return valeur


def valeurMin(N):
    """
    Retourne la valeur minimax d'un noeud MINI avec N batônnets

    Si le joueur précédent a perdu (N=0),
        retourne -RECOMPENSE car ordi a perdu
    """

    # pour connaître le nombre total de noeuds explorés:
    global nbNoeudsExplores
    nbNoeudsExplores = nbNoeudsExplores + 1

    if N == 0:
        return RECOMPENSE
    else:
        coupsTest = coupsPossibles(N)
        noeuds = [valeurMax(N-i) for i in range(1, len(coupsTest)+1)]
        valeur = min(noeuds)
        return valeur


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

