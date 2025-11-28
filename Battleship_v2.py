import numpy as np

def Affichage (grid,coords):
    print("Bataille Navale :\n\n\n")
    print("    1   2   3   4   5   6   7   8   9   10")
    for i in range (21) :
        if i%2 == 0 :
            print ("   ---------------------------------------  ")
        if i%2 == 1 :
            print(f"{coords[i//2]} | {grid[i//2][0]} | {grid[i//2][1]} | {grid[i//2][2]} | {grid[i//2][3]} | {grid[i//2][4]} | {grid[i//2][5]} | {grid[i//2][6]} | {grid[i//2][7]} | {grid[i//2][8]} | {grid[i//2][9]} |")


class Joueur :

    def __init__ (self):
        self.score = 0

    def attack (self, x, y) :
        self.score += 1
        return 
    
    def place_boats() :
        return


def show_boat(grid, coords, message):
    print("\nBataille Navale :\n")
    print("    " + "   ".join(str(i) for i in range(1, 11)))
    sep = "   " + "-" * 39

    for i, row in enumerate(grid):
        print(sep)
        if i == 7:
            print(f"{coords[i]} | " + " | ".join(row) + f" |   {message}")
        else:
            print(f"{coords[i]} | " + " | ".join(row) + " |")
    print(sep)


def positions(x, y, orientation, taille):
    pos = []
    if orientation == "H":
        if y + taille > 10:
            return False
        for i in range(taille):
            pos.append((x, y + i))
    else:
        if x + taille > 10:
            return False
        for i in range(taille):
            pos.append((x + i, y))
    return pos


def chevauchement(pos, cases_occup):
    return any(p in cases_occup for p in pos)


def placer_bateau(symbole, pos, attack_grid, cases_occup):
    for (l, c) in pos:
        attack_grid[l][c] = symbole
        cases_occup.append((l, c))


def placement(symbole, nom, taille, x, y, orientation, attack_grid, cases_occup, coord_list):

    if x.upper() not in coord_list or not y.isdigit():
        return None, "Coordonnées invalides."

    ligne = coord_list.index(x.upper())
    col = int(y) - 1

    if col < 0 or col >= 10:
        return None, "Colonne invalide."

    pos = positions(ligne, col, orientation, taille)
    if pos is False:
        return None, "Le bateau dépasse de la grille."

    if chevauchement(pos, cases_occup):
        return None, "Le bateau chevauche un autre."

    placer_bateau(symbole, pos, attack_grid, cases_occup)
    return pos, f"{nom} placé !"


def placer_un_bateau(symbole, nom, taille, attack_grid, cases_occup, coord_list):
    valide = False
    while not valide:
        print(f"Nouvelles coordonnées pour {nom} ({taille} cases)")
        x = input("Ligne (A-J) : ")
        y = input("Colonne (1-10) : ")

        orientation = "H"
        if taille > 1:
            orientation = input("Orientation H/V : ").upper()

        pos, message = placement(symbole, nom, taille, x, y, orientation,attack_grid, cases_occup, coord_list)

        show_boat(attack_grid, coord_list, message)

        if pos is not None:
            return pos


def grille_joueur():
    attack_grid = np.full((10, 10), " ")
    cases_occup = []
    dict_bateaux = {}
    return attack_grid, cases_occup, dict_bateaux


if __name__ == "__main__":

    coord_list = ["A","B","C","D","E","F","G","H","I","J"]
    boat_names = {
        "P": ("Porte-Avion", 5),
        "C": ("Croiseur", 4),
        "S": ("Sous-marin", 3),
        "T": ("Torpilleur", 2),
        "B": ("Barque", 1)
    }

    attack_grid, cases_occup, dict_bateaux = grille_joueur()

    message = "Placement des bateaux"
    show_boat(attack_grid, coord_list, message)

    for symbole, (nom, taille) in boat_names.items():
        valide = False
        while not valide:
            print(f"Où placer {nom} ({taille} cases) ?")
            x = input("Ligne (A-J) : ")
            y = input("Colonne (1-10) : ")

            orientation = "H"
            if taille > 1:
                orientation = input("Orientation H/V : ").upper()

            pos, message = placement(symbole, nom, taille, x, y, orientation,attack_grid, cases_occup, coord_list)

            show_boat(attack_grid, coord_list, message)

            if pos is not None:
                dict_bateaux[symbole] = pos
                valide = True
    OK = True
    while OK:
        o = input("Voulez-vous changer la place d'un bateau ? (O/N) : ").upper().strip()
        if o == "N":
            OK = False
        elif o == "O":
            s = input("Quel bateau ? (P/C/S/T/B) : ").upper().strip()
            if s in boat_names:
                nom, taille = boat_names[s]
                anciennes = dict_bateaux[s]
                for (l, c) in anciennes:
                    attack_grid[l][c] = " "
                    cases_occup.remove((l, c))

                show_boat(attack_grid, coord_list, "Bateau retiré")
                nouvelles = placer_un_bateau(s, nom, taille, attack_grid, cases_occup, coord_list)
                dict_bateaux[s] = nouvelles
            else:
                print("Symbole invalide.")
        else:
            print("Choix invalide.")
    print(dict_bateaux)


if  __name__ == "__main__" :
    grid_act = np.full(shape= [10,10], fill_value= " ")
    coord_list = ["A","B","C","D","E","F","G","H","I","J"]
    Affichage(gird= grid_act, coords= coord_list)



