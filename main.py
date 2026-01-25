import tkinter as tk
from tkinter import messagebox
import random
import webbrowser # Import nécessaire pour ouvrir le lien internet

# ==============================================================================
# 1. VARIABLES GLOBALES ET LOGIQUE DU JEU
# ==============================================================================

grille = []
flotte = {}
# On définit ces variables graphiques en global pour qu'elles soient accessibles
canvas = None
entree_x = None
entree_y = None
label_info = None
fenetre_principale = None 

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

# ==============================================================================
# 2. FONCTIONS GRAPHIQUES DU JEU
# ==============================================================================

ECHELLE = 40
CENTRE_X = 200
CENTRE_Y = 200

def dessiner_point(x, y, couleur):
    canvas.delete("trace")
    px = CENTRE_X + (x * ECHELLE)
    py = CENTRE_Y - (y * ECHELLE)
    
    canvas.create_line(px, py, px, CENTRE_Y, fill=couleur, dash=(4, 4), tags="trace")
    canvas.create_line(px, py, CENTRE_X, py, fill=couleur, dash=(4, 4), tags="trace")
    
    rayon = 8
    canvas.create_oval(px - rayon, py - rayon, px + rayon, py + rayon, 
                       fill=couleur, outline="black")

def tirer():
    try:
        x_saisi = int(entree_x.get())
        y_saisi = int(entree_y.get())
    except ValueError:
        label_info.config(text="Erreur : Entrez des nombres entiers !", fg="orange")
        return

    if x_saisi < -4 or x_saisi > 4 or y_saisi < -4 or y_saisi > 4:
        label_info.config(text="Hors zone ! (-4 à 4)", fg="orange")
        return

    colonne = x_saisi + 4
    ligne = 4 - y_saisi
    valeur = grille[ligne][colonne]

    if valeur == 0: # EAU
        grille[ligne][colonne] = 2
        dessiner_point(x_saisi, y_saisi, "grey")
        label_info.config(text=f"Tir en ({x_saisi}, {y_saisi}) : PLOUF !", fg="black")

    elif valeur == 1: # BATEAU
        grille[ligne][colonne] = 3
        dessiner_point(x_saisi, y_saisi, "red")
        
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
                fenetre_principale.quit()
        else:
            label_info.config(text="BOUM ! Touché !", fg="red")

    elif valeur >= 2:
        label_info.config(text=f"Vous avez déjà visé le point ({x_saisi}, {y_saisi})", fg="blue")
    
    entree_x.delete(0, tk.END)
    entree_y.delete(0, tk.END)

# ==============================================================================
# 3. CONSTRUCTION DES INTERFACES
# ==============================================================================

def ouvrir_lien(event):
    """ Fonction appelée lors du clic sur le lien GitHub """
    webbrowser.open("https://github.com/Raph81212/bataille-navalle")

def lancer_le_jeu(frame_menu_a_detruire):
    frame_menu_a_detruire.destroy()
    fenetre_principale.configure(bg="#f0f0f0")

    global canvas, entree_x, entree_y, label_info

    # Cadre Gauche : Le Repère
    frame_graph = tk.Frame(fenetre_principale, padx=10, pady=10)
    frame_graph.pack(side=tk.LEFT)

    canvas = tk.Canvas(frame_graph, width=400, height=400, bg="white")
    canvas.pack()

    # DESSIN DU REPÈRE
    for i in range(-4, 5):
        pos = i * ECHELLE
        canvas.create_line(CENTRE_X + pos, 0, CENTRE_X + pos, 400, fill="lightgrey")
        canvas.create_line(0, CENTRE_Y + pos, 400, CENTRE_Y + pos, fill="lightgrey")

    canvas.create_line(CENTRE_X, 0, CENTRE_X, 400, width=2, arrow=tk.LAST)
    canvas.create_line(0, CENTRE_Y, 400, CENTRE_Y, width=2, arrow=tk.LAST)

    for i in range(-4, 5):
        if i == 0: 
            canvas.create_text(CENTRE_X - 10, CENTRE_Y + 12, text="0", font=("Arial", 8, "bold"))
            continue 
        px = CENTRE_X + (i * ECHELLE)
        py = CENTRE_Y - (i * ECHELLE)
        canvas.create_text(px, CENTRE_Y + 15, text=str(i), font=("Arial", 8))
        canvas.create_text(CENTRE_X - 15, py, text=str(i), font=("Arial", 8))

    canvas.create_text(380, CENTRE_Y - 15, text="X", font=("Arial", 10, "bold"))
    canvas.create_text(CENTRE_X + 15, 20, text="Y", font=("Arial", 10, "bold"))

    # Cadre Droit : Commandes
    frame_commandes = tk.Frame(fenetre_principale, padx=20)
    frame_commandes.pack(side=tk.RIGHT)

    tk.Label(frame_commandes, text="Coordonnées", font=("Arial", 14, "bold")).pack(pady=10)

    frame_x = tk.Frame(frame_commandes)
    frame_x.pack(pady=5)
    tk.Label(frame_x, text="X :", font=("Arial", 12)).pack(side=tk.LEFT)
    entree_x = tk.Entry(frame_x, width=5, font=("Arial", 12))
    entree_x.pack(side=tk.LEFT)

    frame_y = tk.Frame(frame_commandes)
    frame_y.pack(pady=5)
    tk.Label(frame_y, text="Y :", font=("Arial", 12)).pack(side=tk.LEFT)
    entree_y = tk.Entry(frame_y, width=5, font=("Arial", 12))
    entree_y.pack(side=tk.LEFT)

    btn_feu = tk.Button(frame_commandes, text="FEU !", font=("Arial", 12, "bold"), 
                        bg="#d32f2f", fg="white", activebackground="#b71c1c", cursor="hand2",
                        command=tirer, relief=tk.FLAT, borderwidth=0)
    btn_feu.pack(pady=20, ipadx=15, ipady=5)

    label_info = tk.Label(frame_commandes, text="En attente de tir...", font=("Arial", 11), wraplength=150)
    label_info.pack(pady=10)

def afficher_menu():
    fenetre_principale.configure(bg="white")
    frame_menu = tk.Frame(fenetre_principale, bg="white")
    frame_menu.pack(fill="both", expand=True)

    # 1. Le Titre
    tk.Label(frame_menu, text="Bataille Navale Relative", font=("Helvetica", 26, "bold"), 
             bg="white", fg="#333333").pack(pady=(60, 10))

    # 2. Le Nom (Sans "Par")
    tk.Label(frame_menu, text="Raphaël CHAILLIÉ", font=("Helvetica", 14, "italic"), 
             bg="white", fg="#666666").pack(pady=(0, 20))

    # 3. Le Descriptif
    description = (
        "Bienvenue Capitaine !\n\n"
        "La flotte ennemie est cachée dans le brouillard.\n"
        "Votre mission est de la détruire en utilisant le repère cartésien.\n\n"
        "Entrez les coordonnées X (abscisse) et Y (ordonnée)\n"
        "pour lancer vos torpilles."
    )
    tk.Label(frame_menu, text=description, font=("Helvetica", 12), bg="white", 
             justify="center", wraplength=500).pack(pady=20)

    # 4. Le Bouton JOUER (ROUGE)
    btn_jouer = tk.Button(frame_menu, text="JOUER", font=("Helvetica", 16, "bold"),
                          bg="#d32f2f", fg="white", activebackground="#b71c1c", # ROUGE
                          relief=tk.FLAT, borderwidth=0, padx=30, pady=10, cursor="hand2",
                          command=lambda: lancer_le_jeu(frame_menu))
    btn_jouer.pack(pady=30)

    # 5. Le Lien GitHub
    lien_github = tk.Label(frame_menu, text="https://github.com/Raph81212/bataille-navalle", 
                           font=("Helvetica", 10, "underline"), bg="white", fg="blue", cursor="hand2")
    lien_github.pack(pady=5)
    # On "lie" (bind) le clic gauche de la souris à la fonction ouvrir_lien
    lien_github.bind("<Button-1>", ouvrir_lien)

    # 6. La Licence
    tk.Label(frame_menu, text="Licence libre copyleft (ɔ)", font=("Helvetica", 9), 
             bg="white", fg="#999999").pack(side=tk.BOTTOM, pady=10)

# ==============================================================================
# 4. LANCEMENT DU PROGRAMME
# ==============================================================================

init_jeu()
fenetre_principale = tk.Tk()
fenetre_principale.title("Bataille Navale Relative")
fenetre_principale.geometry("650x600") # Un peu plus haut pour faire tenir le lien
afficher_menu()
fenetre_principale.mainloop()