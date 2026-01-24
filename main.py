import random

# --- 1. CRÉATION DE LA GRILLE (9x9) ---
# Une grille vide remplie de 0 (Eau)
grille = []
for ligne in range(9):
    grille.append([0] * 9)

# Dictionnaire pour suivre l'état de chaque bateau
# Structure : { "Nom du bateau": [(x,y), (x,y)...] }
flotte = {}

# Liste des bateaux à placer (Nom, Taille)
types_bateaux = [
    ("Porte-Avions", 5),
    ("Croiseur", 4),
    ("Contre-Torpilleur", 3),
    ("Torpilleur", 2)
]

# --- 2. PLACEMENT DES BATEAUX ---
print("Initialisation de la flotte en cours...")

for nom, taille in types_bateaux:
    place = False
    while place == False:
        # On choisit une direction (0: Horizontal, 1: Vertical)
        direction = random.randint(0, 1)
        
        if direction == 0: # Horizontal
            # On limite le départ pour ne pas sortir du cadre (9 - taille)
            col_depart = random.randint(0, 9 - taille)
            lig_depart = random.randint(0, 8)
            
            # Vérification des collisions
            libre = True
            for i in range(taille):
                if grille[lig_depart][col_depart + i] != 0:
                    libre = False
                    break
            
            # Si tout est libre, on place le bateau
            if libre:
                coords_bateau = [] # Pour mémoriser les positions
                for i in range(taille):
                    grille[lig_depart][col_depart + i] = 1
                    coords_bateau.append((col_depart + i, lig_depart)) # On stocke (col, lig)
                
                flotte[nom] = coords_bateau # On ajoute le bateau au dictionnaire
                place = True

        else: # Vertical
            col_depart = random.randint(0, 8)
            lig_depart = random.randint(0, 9 - taille)
            
            libre = True
            for i in range(taille):
                if grille[lig_depart + i][col_depart] != 0:
                    libre = False
                    break
            
            if libre:
                coords_bateau = []
                for i in range(taille):
                    grille[lig_depart + i][col_depart] = 1
                    coords_bateau.append((col_depart, lig_depart + i))
                
                flotte[nom] = coords_bateau
                place = True

print("La flotte est prête ! À l'attaque Capitaine !")
print("Zone de tir : X entre -4 et 4, Y entre -4 et 4")
print("-" * 30)

# --- 3. BOUCLE DE JEU ---
while True:
    print(flotte)
    try:
        # Demande des coordonnées
        print("\nEntrez vos coordonnées de tir :")
        x = int(input("X : "))
        y = int(input("Y : "))
    except ValueError:
        print("Erreur : Veuillez entrer un nombre entier relatif.")
        continue

    # Vérification des limites (-4 à 4)
    if x < -4 or x > 4 or y < -4 or y > 4:
        print("Attention, la torpille est en dehors de la zone de tir !")
        continue

    # Conversion en indices de tableau (0 à 8)
    # x = -4 -> col 0, x = 0 -> col 4, x = 4 -> col 8
    colonne = x + 4
    # y = 4 -> lig 0, y = 0 -> lig 4, y = -4 -> lig 8
    ligne = 4 - y 

    # --- 4. ANALYSE DU TIR ---
    valeur_case = grille[ligne][colonne]

    if valeur_case == 0:
        print("Plouf ! C'est raté, dans l'eau.")
        grille[ligne][colonne] = 2 # Marqué comme raté

    elif valeur_case == 2 or valeur_case == 3:
        print("Nous avons déjà tiré ici Capitaine, concentrez-vous !")

    elif valeur_case == 1:
        print("BOUM ! Touché !")
        grille[ligne][colonne] = 3 # Marqué comme touché

        # On cherche quel bateau a été touché pour le mettre à jour
        # On parcourt le dictionnaire (nom du bateau, liste des coordonnées)
        nom_bateau_coule = "" # Variable temporaire
        
        for nom, coords in flotte.items():
            if (colonne, ligne) in coords:
                coords.remove((colonne, ligne)) # On enlève cette partie du bateau
                
                # Si la liste est vide, le bateau est coulé
                if coords == []:
                    print(f"⚓ INCROYABLE ! Vous avez coulé le {nom} !")
                    nom_bateau_coule = nom # On note le nom pour le supprimer après
                break
        
        # Si un bateau a coulé, on le supprime du dictionnaire
        if nom_bateau_coule != "":
            del flotte[nom_bateau_coule]

        # Condition de VICTOIRE
        if flotte == {}:
            print("\n" + "="*40)
            print("FÉLICITATIONS ! Toute la flotte ennemie est anéantie !")
            print("="*40)
            break # Fin du jeu