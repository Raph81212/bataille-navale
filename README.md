# 🚢 Bataille Navale Relative

> Un jeu de stratégie éducatif pour maîtriser le repère cartésien.

![Version](https://img.shields.io/badge/version-1.0-blue)
![License](https://img.shields.io/badge/license-Copyleft-red)
![Aperçu du jeu](screenshot.png)

## 🎮 Jouer en ligne (Recommandé)

Pas besoin d'installation ! Le jeu est disponible directement dans votre navigateur (PC, Tablette, Mobile).

👉 **[CLIQUEZ ICI POUR JOUER](https://raph81212.github.io/bataille-navalle/)**

---

## 🧐 À propos du projet

**Bataille Navale Relative** revisite le célèbre jeu de société en y intégrant une dimension mathématique. Au lieu des classiques "A1, B2", le joueur doit utiliser des **coordonnées relatives (x, y)** comprises entre **-4 et 4**.

L'objectif est de travaillé la compétence "se repérer sur une droite graduée, dans le plan muni d'un repère orthogonal".

### ✨ Fonctionnalités
* **Repère Cartésien :** Grille centrée sur (0,0) avec axes x et y visibles.
* **Interface :** S'adapte parfaitement aux ordinateurs et aux téléphones portables.
* **Contrôles Tactiles :** Boutons `+` et `-` pour une saisie facile sur mobile.
* **Retour Visuel :**
    * 🔴 Rouge : Touché (avec lignes pointillées pour repérer les coordonnées).
    * 🔘 Gris : Dans l'eau.
* **Suivi de la Flotte :** Liste des navires ennemis qui se raye automatiquement lorsqu'un bateau est coulé.

---

## 🛠️ Installation (Version Python / Windows)

Si vous préférez la version logicielle native (fichier `.exe`) ou si vous souhaitez modifier le code Python.

### Option 1 : L'exécutable (Windows uniquement)
1.  Allez dans le dossier `dist` de ce dépôt.
2.  Téléchargez le fichier `BatailleNavale.exe`.
3.  Lancez-le (acceptez l'avertissement de sécurité Windows lors du premier lancement).

### Option 2 : Le Code Source (Python)
Pré-requis : Avoir Python 3 installé.

1.  Clonez le dépôt :
    ```bash
    git clone [https://github.com/Raph81212/bataille-navalle.git](https://github.com/Raph81212/bataille-navalle.git)
    ```
2.  Lancez le jeu :
    ```bash
    python main.py
    ```

---

## 💻 Technologies utilisées

Ce projet contient deux versions du jeu :

1.  **Version Web (Actuelle) :**
    * HTML5 / CSS3 (Design responsive Flexbox)
    * JavaScript (Canvas API pour le dessin)
2.  **Version Desktop (Originale) :**
    * Python 3
    * Tkinter (GUI)

---

## 📏 Règles du jeu

1.  La flotte ennemie est cachée quelque part dans la grille de **-4 à 4**.
2.  Entrez une coordonnée **x** (horizontale) et **y** (verticale).
3.  Appuyez sur **FEU !**.
4.  Si vous touchez un navire, un point rouge apparaît. Si vous coulez un navire entier, son nom est rayé de la liste.
5.  Gagnez en coulant les 4 navires :
    * 1 Porte-Avions (5 cases)
    * 1 Croiseur (4 cases)
    * 1 Contre-Torpilleur (3 cases)
    * 1 Torpilleur (2 cases)

---

## 👤 Auteur

**Raphaël CHAILLIÉ**

* Ce projet est **Open Source**.
* Licence : Copyleft (ɔ) - Vous êtes libre de partager et modifier ce code.

---