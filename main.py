import tkinter as tk
from tkinter import messagebox
import random

# --- 1. LOGIQUE DU JEU (Inchangée) ---
grille = []
flotte = {}

def init_jeu():
    global grille, flotte
    grille = []
    flotte = {}
    # Grille 9x9 vide
    for ligne in range(9):
        grille.append([0] * 9)

    types_bateaux = [("Porte-Avions", 5), ("Croiseur", 4), 
                     ("Contre-Torpilleur", 3), ("Torpilleur", 2)]

    for nom, taille in types_bateaux:
        place = False
        while not place:
            direction = random.randint(0, 1)
            if direction == 0: # Horizontal
                c_dep = random.randint(0, 9 - taille)
                l_dep = random.randint(0, 8)
                libre = True
                for i in range(taille):
                    if grille[l_dep][c_dep + i] != 0: libre = False; break
                if libre:
                    coords = []
                    for i in range(taille):
                        grille[l_dep][c_dep + i] = 1
                        coords.append((c_dep + i, l_dep))
                    flotte[nom] = coords
                    place = True
            else: # Vertical
                c_dep = random.randint(0, 8)
                l_dep = random.randint(0, 9 - taille)
                libre = True
                for i in range(taille):
                    if grille[l_dep + i][c_dep] != 0: libre = False; break
                if libre:
                    coords = []
                    for i in range(taille):
                        grille[l_dep + i][c_dep] = 1
                        coords.append((c_dep, l_dep + i))
                    flotte[nom] = coords
                    place = True

# --- 2. FONCTIONS GRAPHIQUES ---

# Paramètres du repère
ECHELLE = 40  # Nombre de pixels pour 1 unité
CENTRE_X = 200 # Le 0 en X (milieu de 400)
CENTRE_Y = 200 # Le 0 en Y (milieu de 400)

def dessiner_point(x, y, couleur):
    """ Dessine un petit rond sur le repère aux coordonnées x, y """
    # Conversion Math -> Pixels écran
    # Pour X : on ajoute au centre
    px = CENTRE_X + (x * ECHELLE)
    # Pour Y : on soustrait au centre (car en informatique Y descend, en math Y monte)
    py = CENTRE_Y - (y * ECHELLE)
    
    rayon = 10
    canvas.create_oval(px - rayon, py - rayon, px + rayon, py + rayon, fill=couleur, outline="black")

def tirer():
    try:
        #print(flotte) # Pour debug
        x_saisi = int(entree_x.get())
        y_saisi = int(entree_y.get())
    except ValueError:
        label_info.config(text="Erreur : Entrez des nombres entiers !", fg="orange")
        return

    if x_saisi < -4 or x_saisi > 4 or y_saisi < -4 or y_saisi > 4:
        label_info.config(text="Hors zone ! (-4 à 4)", fg="orange")
        return

    # Conversion indices
    colonne = x_saisi + 4
    ligne = 4 - y_saisi
    
    valeur = grille[ligne][colonne]

    if valeur == 0: # EAU
        grille[ligne][colonne] = 2
        dessiner_point(x_saisi, y_saisi, "grey") # Point GRIS
        label_info.config(text=f"Tir en ({x_saisi}, {y_saisi}) : PLOUF !", fg="black")

    elif valeur == 1: # BATEAU
        grille[ligne][colonne] = 3
        dessiner_point(x_saisi, y_saisi, "red") # Point ROUGE
        
        # Vérification Coulé
        nom_coule = ""
        for nom, coords in flotte.items():
            if (colonne, ligne) in coords:
                coords.remove((colonne, ligne))
                if coords == []:
                    nom_coule = nom
                break
        
        if nom_coule:
            del flotte[nom_coule]
            label_info.config(text=f"BOUM ! Vous avez COULÉ le {nom_coule} !", fg="red")
            if not flotte:
                messagebox.showinfo("Victoire !", "Félicitations Capitaine ! Toute la flotte est coulée !")
                fenetre.quit()
        else:
            label_info.config(text="BOUM ! Touché !", fg="red")

    elif valeur >= 2:
        label_info.config(text=f"Vous avez déjà visé le point ({x_saisi}, {y_saisi})", fg="blue")
    
    entree_x.delete(0, tk.END)
    entree_y.delete(0, tk.END)

# --- 3. INTERFACE ---

init_jeu()

fenetre = tk.Tk()
fenetre.title("Bataille Navale - Repère Cartésien")

# Cadre Gauche : Le Repère (Canvas)
frame_graph = tk.Frame(fenetre, padx=10, pady=10)
frame_graph.pack(side=tk.LEFT)

canvas = tk.Canvas(frame_graph, width=400, height=400, bg="white")
canvas.pack()

# DESSIN DU REPÈRE
# 1. La grille (papier millimétré)
for i in range(-4, 5):
    pos = i * ECHELLE
    # Lignes verticales
    canvas.create_line(CENTRE_X + pos, 0, CENTRE_X + pos, 400, fill="lightgrey")
    # Lignes horizontales
    canvas.create_line(0, CENTRE_Y + pos, 400, CENTRE_Y + pos, fill="lightgrey")

# 2. Les Axes principaux (X et Y)
canvas.create_line(CENTRE_X, 0, CENTRE_X, 400, width=2, arrow=tk.LAST) # Axe Y (Vertical)
canvas.create_line(0, CENTRE_Y, 400, CENTRE_Y, width=2, arrow=tk.LAST) # Axe X (Horizontal)

# 3. Les numéros sur les axes
for i in range(-4, 5):
    if i == 0: continue # On ne marque pas le 0 deux fois
    px = CENTRE_X + (i * ECHELLE)
    py = CENTRE_Y - (i * ECHELLE)
    # Chiffres sur l'axe X
    canvas.create_text(px, CENTRE_Y + 15, text=str(i), font=("Arial", 8))
    # Chiffres sur l'axe Y
    canvas.create_text(CENTRE_X - 15, py, text=str(i), font=("Arial", 8))

canvas.create_text(380, CENTRE_Y - 15, text="X", font=("Arial", 10, "bold"))
canvas.create_text(CENTRE_X + 15, 20, text="Y", font=("Arial", 10, "bold"))


# Cadre Droit : Commandes
frame_commandes = tk.Frame(fenetre, padx=20)
frame_commandes.pack(side=tk.RIGHT)

tk.Label(frame_commandes, text="Coordonnées", font=("Arial", 14, "bold")).pack(pady=10)

# Champ X
frame_x = tk.Frame(frame_commandes)
frame_x.pack(pady=5)
tk.Label(frame_x, text="X :", font=("Arial", 12)).pack(side=tk.LEFT)
entree_x = tk.Entry(frame_x, width=5, font=("Arial", 12))
entree_x.pack(side=tk.LEFT)

# Champ Y
frame_y = tk.Frame(frame_commandes)
frame_y.pack(pady=5)
tk.Label(frame_y, text="Y :", font=("Arial", 12)).pack(side=tk.LEFT)
entree_y = tk.Entry(frame_y, width=5, font=("Arial", 12))
entree_y.pack(side=tk.LEFT)

btn_feu = tk.Button(frame_commandes, text="FEU !", font=("Arial", 12, "bold"), bg="red", fg="white", command=tirer)
btn_feu.pack(pady=20, ipadx=10, ipady=5)

label_info = tk.Label(frame_commandes, text="En attente de tir...", font=("Arial", 11), wraplength=150)
label_info.pack(pady=10)

fenetre.mainloop()