import tkinter as tk
from tkinter import messagebox
import random
import webbrowser

# ==============================================================================
# 1. VARIABLES GLOBALES ET LOGIQUE DU JEU
# ==============================================================================

grille = []
flotte = {}
canvas = None
entree_x = None
entree_y = None
label_info = None
fenetre_principale = None
labels_bateaux = {} 

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
    
    canvas.create_line(px, py, px, CENTRE_Y, fill="red", width=2, dash=(4, 4), tags="trace")
    canvas.create_line(px, py, CENTRE_X, py, fill="red", width=2, dash=(4, 4), tags="trace")
    
    rayon = 8
    canvas.create_oval(px - rayon, py - rayon, px + rayon, py + rayon, 
                       fill=couleur, outline="black")

def changer_valeur(entree, delta):
    """Fonction pour augmenter ou diminuer la valeur d'une entrée"""
    try:
        valeur_actuelle = int(entree.get())
    except ValueError:
        valeur_actuelle = 0
    
    nouvelle_valeur = valeur_actuelle + delta
    
    # On bloque entre -4 et 4
    if -4 <= nouvelle_valeur <= 4:
        entree.delete(0, tk.END)
        entree.insert(0, str(nouvelle_valeur))

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
            
            if nom_coule in labels_bateaux:
                labels_bateaux[nom_coule].config(fg="grey", font=("Arial", 10, "overstrike"))
            
            if not flotte:
                messagebox.showinfo("Victoire !", "Félicitations Capitaine ! Toute la flotte est coulée !")
                fenetre_principale.quit()
        else:
            label_info.config(text="BOUM ! Touché !", fg="red")

    elif valeur >= 2:
        label_info.config(text=f"Vous avez déjà visé le point ({x_saisi}, {y_saisi})", fg="blue")
    
    # On ne vide plus les entrées pour faciliter les tirs proches, 
    # ou on peut les remettre à 0 si tu préfères. Ici je laisse la valeur.

# ==============================================================================
# 3. CONSTRUCTION DES INTERFACES
# ==============================================================================

def ouvrir_lien(event):
    # Changement URL
    webbrowser.open("https://github.com/Raph81212/bataille-navale")

def lancer_le_jeu(frame_menu_a_detruire):
    frame_menu_a_detruire.destroy()
    fenetre_principale.configure(bg="#f0f0f0")

    global canvas, entree_x, entree_y, label_info, labels_bateaux

    # --- Cadre Gauche : Le Repère ---
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
            canvas.create_text(CENTRE_X - 10, CENTRE_Y + 12, text="0", font=("Arial", 8))
            continue 
        px = CENTRE_X + (i * ECHELLE)
        py = CENTRE_Y - (i * ECHELLE)
        canvas.create_text(px, CENTRE_Y + 15, text=str(i), font=("Arial", 8))
        canvas.create_text(CENTRE_X - 15, py, text=str(i), font=("Arial", 8))

    canvas.create_text(380, CENTRE_Y - 15, text="x", font=("Arial", 12, "bold"))
    canvas.create_text(CENTRE_X + 15, 20, text="y", font=("Arial", 12, "bold"))

    # --- Cadre Droit : Commandes ---
    frame_commandes = tk.Frame(fenetre_principale, padx=20)
    frame_commandes.pack(side=tk.RIGHT)

    tk.Label(frame_commandes, text="🎯 CIBLES :", font=("Arial", 10, "bold"), 
             bg="#f0f0f0").pack(pady=(0, 5), anchor="w")

    liste_affichage = [("Porte-Avions", 5), ("Croiseur", 4), 
                       ("Contre-Torpilleur", 3), ("Torpilleur", 2)]
    
    labels_bateaux = {} 
    
    for nom, taille in liste_affichage:
        lbl = tk.Label(frame_commandes, text=f"• {nom} ({taille})", 
                       font=("Arial", 10), bg="#f0f0f0", fg="#333333")
        lbl.pack(anchor="w")
        labels_bateaux[nom] = lbl

    tk.Label(frame_commandes, text="", bg="#f0f0f0").pack(pady=5)

    tk.Label(frame_commandes, text="Coordonnées de tir", font=("Arial", 14, "bold")).pack(pady=10)

    # --- NOUVEAU SYSTÈME DE SAISIE X (Boutons +/-) ---
    frame_x = tk.Frame(frame_commandes, bg="#f0f0f0")
    frame_x.pack(pady=5)
    
    tk.Label(frame_x, text="x : ", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(side=tk.LEFT)
    
    # On crée l'entrée d'abord pour pouvoir la référencer dans les boutons
    entree_x = tk.Entry(frame_x, width=4, font=("Arial", 12), justify='center')
    entree_x.insert(0, "0") # Valeur par défaut
    
    btn_x_moins = tk.Button(frame_x, text="-", font=("Arial", 10, "bold"), width=3,
                            command=lambda: changer_valeur(entree_x, -1))
    btn_x_plus = tk.Button(frame_x, text="+", font=("Arial", 10, "bold"), width=3,
                           command=lambda: changer_valeur(entree_x, 1))

    # On affiche dans l'ordre : Bouton Moins | Entrée | Bouton Plus
    btn_x_moins.pack(side=tk.LEFT, padx=5)
    entree_x.pack(side=tk.LEFT)
    btn_x_plus.pack(side=tk.LEFT, padx=5)

    # --- NOUVEAU SYSTÈME DE SAISIE Y (Boutons +/-) ---
    frame_y = tk.Frame(frame_commandes, bg="#f0f0f0")
    frame_y.pack(pady=5)
    
    tk.Label(frame_y, text="y : ", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(side=tk.LEFT)
    
    entree_y = tk.Entry(frame_y, width=4, font=("Arial", 12), justify='center')
    entree_y.insert(0, "0") 
    
    btn_y_moins = tk.Button(frame_y, text="-", font=("Arial", 10, "bold"), width=3,
                            command=lambda: changer_valeur(entree_y, -1))
    btn_y_plus = tk.Button(frame_y, text="+", font=("Arial", 10, "bold"), width=3,
                           command=lambda: changer_valeur(entree_y, 1))

    btn_y_moins.pack(side=tk.LEFT, padx=5)
    entree_y.pack(side=tk.LEFT)
    btn_y_plus.pack(side=tk.LEFT, padx=5)


    # Bouton FEU
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
             bg="white", fg="#333333").pack(pady=(50, 10))

    # (Nom retiré d'ici)

    # 3. Le Descriptif
    description = (
        "Bienvenue Capitaine !\n\n"
        "La flotte ennemie est cachée dans le brouillard.\n"
        "Votre mission est de la détruire en utilisant le repère cartésien.\n\n"
        "Entrez les coordonnées x (abscisse) et y (ordonnée)\n"
        "pour lancer vos torpilles."
    )
    
    tk.Label(frame_menu, text=description, font=("Helvetica", 12), bg="white", 
             justify="center", wraplength=550).pack(pady=20)

    # 4. Le Bouton JOUER
    btn_jouer = tk.Button(frame_menu, text="JOUER", font=("Helvetica", 16, "bold"),
                          bg="#d32f2f", fg="white", activebackground="#b71c1c",
                          relief=tk.FLAT, borderwidth=0, padx=30, pady=10, cursor="hand2",
                          command=lambda: lancer_le_jeu(frame_menu))
    btn_jouer.pack(pady=30)

    # 5. Le Lien GitHub (URL mise à jour)
    lien_github = tk.Label(frame_menu, text="https://github.com/Raph81212/bataille-navale", 
                           font=("Helvetica", 10, "underline"), bg="white", fg="blue", cursor="hand2")
    lien_github.pack(pady=5)
    lien_github.bind("<Button-1>", ouvrir_lien)

    # 6. La Licence + Ton NOM en bas
    texte_footer = "Raphaël CHAILLIÉ - Licence libre copyleft (ɔ)"
    tk.Label(frame_menu, text=texte_footer, font=("Helvetica", 9), 
             bg="white", fg="#999999").pack(side=tk.BOTTOM, pady=10)

# ==============================================================================
# 4. LANCEMENT DU PROGRAMME
# ==============================================================================

init_jeu()
fenetre_principale = tk.Tk()
fenetre_principale.title("Bataille Navale Relative")
fenetre_principale.geometry("650x650") 
afficher_menu()
fenetre_principale.mainloop()