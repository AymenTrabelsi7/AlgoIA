"""
Réponses aux question théoriques du TP :

5)Le programme calcule pendant un temps au delà du raisonnable.

6)En estimant très grossèrement que toutes les parties se terminent à la profondeur max, soit 42 (6 lignes et 7 colonnes),
on peut estimer qu'il y a environ 6^42 noeuds à explorer. Avec une fréquence d'horloge de 3 Ghz, cela représente un temps de
calcul de 5000 milliards d'années.


8) Temps de calcul en secondes en fonction de la profondeur max :
Profondeur max de 4 : 0.05
Profondeur max de 5 : 0.34
Profondeur max de 6 : 2.13
Profondeur max de 7 : 13.50
Profondeur max de 8 : 82.21

On peut donc dire que l'ordi joue rapidement jusqu'à une profondeur de 6, voire 7.

11)
Temps de calcul en secondes en fonction de la profondeur max :
Profondeur max de 4 : 0.02
Profondeur max de 5 : 0.08
Profondeur max de 6 : 0.26
Profondeur max de 7 : 1.43
Profondeur max de 8 : 4.46
Profondeur max de 9 : 15.92
Profondeur max de 10 : 43.08

Par rapport à la version sans alpha beta, on peut augmenter la profondeur max jusqu'à 9.


12) Pas faite car je suis tellement nul à ce jeu que l'ordi me bat même avec une profondeur max de 1.
"""



RECOMPENSE = 100  # valeur absolue de la récompense (doit être > evaluation max)
PROFONDEUR_MAXIMALE = 8

def afficheJeu(etat):
    # affiche le jeu
    print("")
    for i in range(6):
        s = ' |'
        for j in range(7):
            if etat[i][j] == 1:
                s = s + ' X |'
            else:
                if etat[i][j] == -1:
                    s = s + ' O |'
                else:
                    s = s + '   |'

        print(s)

    print('-------------------------------')

    s = ' |'
    for j in range(7):
        s = s + ' ' + str(j) + ' |'
    print(s + '\n')


def testFin(etat, joueur):
    # Test si l'état dans lequel c'est à joueur de jouer
    # est un état terminal

    # On peut utiliser la fonction d'évaluation
    # pour savoir si le dernier coup était gagnant
    # et sinon tester le match nul

    ev = evaljoueur(etat, -joueur)
    if ev == RECOMPENSE:
        return True  # le joueur a gagné => partie finie

    # test match nul
    n = 0
    for i in range(6):
        for j in range(7):
            if etat[i][j] == 0:
                return False
    # tout scanné sans trouver de trou => partie finie
    return True


def coupsPossibles(etat):
    """
	Retourne la liste des coups possibles (indices de colonnes)
	"""
    coups = []
    for j in range(7):
        if etat[0][j] == 0:
            coups.append(j)
    return coups


def evaljoueur(etat, joueur):
    # Evalue la position d'un joueur (~ son score indépendamment de l'autre joueur)
    # retourne une valeur positive
    #  = RECOMPENSE si le joueur a gagné
    #  = 0 si match nul
    #  sinon, on doit avoir 0 <= valeur < RECOMPENSE

    value = 0
    n = 0
    # eval le nb max d'alignes
    for i in range(6):
        for j in range(7):
            if etat[i][j] == joueur:
                # compte nb de jetons total
                n = n + 1

                # compte nb alignes
                k = 1
                while k <= 4 and i + k < 6 and etat[i + k][j] == joueur:
                    k = k + 1

                if k == 2:
                    value = value + 1
                elif k == 3:
                    value = value + 3
                elif k == 4:
                    value = value + RECOMPENSE

                k = 1
                while k <= 4 and j + k < 7 and etat[i][j + k] == joueur:
                    k = k + 1

                if k == 2:
                    value = value + 1
                elif k == 3:
                    value = value + 3
                elif k == 4:
                    value = value + RECOMPENSE

                k = 1
                while k <= 4 and i + k < 6 and j + k < 7 and etat[i + k][j + k] == joueur:
                    k = k + 1
                if k == 2:
                    value = value + 1
                elif k == 3:
                    value = value + 3
                elif k == 4:
                    value = value + RECOMPENSE

                k = 1
                while k <= 4 and i + k < 6 and j - k >= 0 and etat[i + k][j - k] == joueur:
                    k = k + 1

                if k == 2:
                    value = value + 1
                elif k == 3:
                    value = value + 3
                elif k == 4:
                    value = value + RECOMPENSE
            elif etat[i][j] != 0:
                n = n + 1

    # Il faut retourner RECOMPENSE si le joueur a gagné et 0 si match nul

    if value >= RECOMPENSE:
        # 4 jetons alignés => c'est gagné !
        value = RECOMPENSE
    else:
        # pour avoir value = 0 en cas de match nul
        if n == 6 * 7:
            value = 0

    return value


def evaluation(etat):
    # Fonction d'évaluation pour un jeu à somme nulle
    #	= evaljoueur(ordi) - evaljoueur(humain)
    # sauf si un des deux joueurs a gagné
    # dans ce cas, il faut retourner
    #	+RECOMPENSE si l'ordinateur a gagné
    #  -RECOMPENSE si l'ordinateur a perdu

    evalHumain = evaljoueur(etat, -1)
    evalOrdi = evaljoueur(etat, 1)

    if evalHumain == RECOMPENSE:
        return -RECOMPENSE
    elif evalOrdi == RECOMPENSE:
        return RECOMPENSE
    else:
        return evalOrdi - evalHumain


def jouerCoup(etat, coup, joueur):
    # Modifier l'état en jouant un coup
    # et retourne True/False si le coup est/n'est pas possible

    if etat[0][coup] != 0:
        return False

    h = 0
    while h < 6 and etat[h][coup] == 0:
        h = h + 1

    etat[h - 1][coup] = joueur
    return True


def copieEtat(etat):
    """
	 copie un état du jeu (pour pouvoir réfléchir en jouant des coups
	 sans modifier l'état réel de la partie)
	"""
    copie = [[0 for j in range(7)] for i in range(6)]
    for i in range(6):
        for j in range(7):
            copie[i][j] = etat[i][j]
    return copie

def getEtatsPossibles(etat, coups):
    #Retourne les états correspondants aux différents coups possibles
    etatsPossibles = []
    for i in range(len(coups)):
        etatCop = copieEtat(etat)
        jouerCoup(etatCop, coups[i], joueur)
        etatsPossibles.append(etatCop)
    return etatsPossibles


def ordiJoue(etat, profondeur_max):
    # retourne le meilleur coup à jouer selon l'algorithme minimax
    # avec une certaine profondeur_max de recherche

    # Détermination du meilleur coup
    coups = coupsPossibles(etat)
    etatsPossibles = getEtatsPossibles(etat, coups)


    #evalCoups = [valeurMin(etatsPossibles[i], 1, profondeur_max) for i in range(len(etatsPossibles))]

    evalCoups = [valeurMinAlphaBeta(etatsPossibles[i], 1, profondeur_max, -2*RECOMPENSE, 2*RECOMPENSE) for i in range(len(etatsPossibles))]

    maxEval = max(evalCoups)
    meilleurCoup = coups[evalCoups.index(maxEval)]

    print("Estimation de l'ordi (Eval = " + str(maxEval) + ") : ")

    estimation(maxEval)

    return meilleurCoup

def estimation(score):
    #Estime l'issue en fonction du score du coup
    if score == RECOMPENSE:
        print("Je vais gagner")
    elif score > 0:
        print("Je vais sûrement gagner")
    elif score < 0:
        print("Je peux faire match nul")
    elif score == -RECOMPENSE:
        print("Je vais perdre")


def valeurMax(etat, profondeur, profondeur_max):
    global nbNoeudsExplores

    if testFin(etat, joueur) or profondeur == profondeur_max:
        return evaluation(etat)
    else:
        maxEval = -2 * RECOMPENSE  # -infini
        coups = coupsPossibles(etat)
        i = 1
        while i < len(coups):
            nbNoeudsExplores += 1
            currentEtat = copieEtat(etat)
            jouerCoup(currentEtat, coups[i], joueur)
            currentEval = valeurMin(currentEtat, profondeur + 1,profondeur_max)
            maxEval = max(maxEval, currentEval)
            i += 1
        return maxEval


def valeurMin(etat, profondeur, profondeur_max):

    global nbNoeudsExplores

    if testFin(etat, -joueur) or profondeur == profondeur_max:
        return evaluation(etat)
    else:
        minEval = 2 * RECOMPENSE  # +infini
        coups = coupsPossibles(etat)
        i = 1
        while i < len(coups):
            nbNoeudsExplores += 1
            currentEtat = copieEtat(etat)
            jouerCoup(currentEtat, coups[i], -joueur)
            currentEval = valeurMax(currentEtat, profondeur + 1, profondeur_max)
            minEval = min(minEval, currentEval)
            i += 1
        return minEval

def valeurMaxAlphaBeta(etat, profondeur, profondeur_max, alpha, beta):
    global nbNoeudsExplores

    if testFin(etat, joueur) or profondeur == profondeur_max:
        return evaluation(etat)
    else:
        maxEval = -2 * RECOMPENSE  # -infini
        coups = coupsPossibles(etat)
        i = 1
        while i < len(coups) and beta > alpha:
            nbNoeudsExplores += 1
            currentEtat = copieEtat(etat)
            jouerCoup(currentEtat, coups[i], joueur)
            currentEval = valeurMinAlphaBeta(currentEtat, profondeur + 1, profondeur_max, alpha, beta)
            maxEval = max(maxEval, currentEval)
            alpha = max(alpha, currentEval)
            i += 1
        return maxEval

def valeurMinAlphaBeta(etat, profondeur, profondeur_max, alpha, beta):

    global nbNoeudsExplores

    if testFin(etat, -joueur) or profondeur == profondeur_max:
        return evaluation(etat)
    else:
        minEval = 2 * RECOMPENSE  # +infini
        coups = coupsPossibles(etat)
        i = 1
        while i < len(coups) and beta > alpha:
            nbNoeudsExplores += 1
            currentEtat = copieEtat(etat)
            jouerCoup(currentEtat, coups[i], -joueur)
            currentEval = valeurMaxAlphaBeta(currentEtat, profondeur + 1, profondeur_max, alpha, beta)
            minEval = min(minEval, currentEval)
            beta = min(beta, currentEval)
            i += 1
        return minEval

########## Programme principal ###############

# Etat initial : matrice de 0
etat = [[0 for j in range(7)] for i in range(6)]

# Choisir qui commence : 
joueur = int(input('Qui commence (-1 : humain, 1 : ordinateur) ? '))

# Boucle de jeu


while not testFin(etat, joueur):

    afficheJeu(etat)

    if joueur == -1:
        # tour de l'humain
        ok = False
        while not ok:
            coup = int(input(' quelle colonne ? '))
            ok = jouerCoup(etat, coup, joueur)

    else:
        # tour de l'Ordinateur

        nbNoeudsExplores = 0

        coup = ordiJoue(etat, PROFONDEUR_MAXIMALE)

        print("(après une réflexion basée sur l'exploration de " + str(nbNoeudsExplores) + " noeuds)")
        jouerCoup(etat, coup, joueur)

    # passer à l'autre joueur:
    joueur = -joueur

afficheJeu(etat)

r = evaluation(etat)
if r > 0:
    print('** Ordinateur a gagné  **')
elif r == 0:
    print(' Match nul ! ')
else:
    print('** BRAVO, ordinateur a perdu **')
