# 🚢 Bataille Navale Relative

> Un jeu de stratégie éducatif pour maîtriser le repère cartésien.

![Version](https://img.shields.io/badge/version-1.1-blue)
![License](https://img.shields.io/badge/license-Copyleft-red)
![Aperçu du jeu](screenshot.png)

## 🎮 Jouer en ligne (Recommandé)

Pas besoin d'installation ! Le jeu est disponible directement dans votre navigateur (PC, Tablette, Mobile).

👉 **[CLIQUEZ ICI POUR JOUER](https://raph81212.github.io/bataille-navalle/)**

---

## 🧐 À propos du projet

**Bataille Navale Relative** revisite le célèbre jeu de société en y intégrant une dimension mathématique. Au lieu des classiques "A1, B2", le joueur doit utiliser des **coordonnées relatives (x, y)** comprises entre **-4 et 4**.

L'objectif est pédagogique et ludique : aider à visualiser et comprendre le fonctionnement d'un repère orthonormé (abscisses et ordonnées) tout en s'amusant.

### ✨ Fonctionnalités
* **Repère Cartésien :** Grille centrée sur (0,0) avec axes x et y visibles.
* **Interface Responsive :** S'adapte parfaitement aux ordinateurs et aux téléphones portables.
* **Contrôles Tactiles :** Boutons `+` et `-` pour une saisie facile sur mobile.
* **Retour Visuel :**
    * 🔴 Rouge : Touché (avec lignes pointillées pour repérer les coordonnées).
    * 🔘 Gris : Dans l'eau.
* **Suivi de la Flotte :** Liste des navires ennemis qui se raye automatiquement.
* **Système de Score :** Calcul de l'efficacité et attribution d'un grade militaire en fin de partie.

---

## 🏆 Système de Score

Le jeu récompense votre efficacité. Plus il vous reste de munitions à la fin de la partie, plus votre grade est élevé ! Sur un total de **60 munitions**, visez la performance maximale.

| Munitions restantes | Grade obtenu |
| :--- | :--- |
| **40 ou +** | 🌟 LÉGENDE VIVANTE |
| **30 à 39** | 🏆 GRAND AMIRAL |
| **20 à 29** | 🎖️ LIEUTENANT TACTICIEN |
| **5 à 19** | ⚓ MATELOT DÉBROUILLARD |
| **0 à 4** | 🛟 MOUSSAILLON DU DIMANCHE |

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
    git clone [https://github.com/Raph81212/bataille-navale.git](https://github.com/Raph81212/bataille-navale.git)
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
    * JavaScript (Canvas API)
2.  **Version Desktop (Originale) :**
    * Python 3
    * Tkinter (GUI)

---

## 👤 Auteur

**Raphaël CHAILLIÉ**

* Ce projet est **Open Source**.
* Licence : Copyleft (ɔ) - Vous êtes libre de partager et modifier ce code.

---
*Fait avec ❤️ et des maths.*