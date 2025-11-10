import numpy as np

def Affichage (grid,coords):
    print("Bataille Navale :\n\n\n")
    print("    1   2   3   4   5   6   7   8   9   10")
    for i in range (21) :
        if i%2 == 0 :
            print ("   ---------------------------------------  ")
        if i%2 == 1 :
            print(f"{coords[i//2]} | {grid[i//2][0]} | {grid[i//2][1]} | {grid[i//2][2]} | {grid[i//2][3]} | {grid[i//2][4]} | {grid[i//2][5]} | {grid[i//2][6]} | {grid[i//2][7]} | {grid[i//2][8]} | {grid[i//2][9]} |")


def attack (x, y, boat_grid, attack_grid) :

    x = coord_list.index(x)
    y -= 1

    if boat_grid[x][y] == " " :
        attack_grid[x][y] = "*"

    return 

def place_boats () :
    # Cindy
    return 
#def placer_bateau_aleatoire(grille):
#     dict_bateau = {}
#     for symbole in bateaux.keys():
#         placer=False
#         taille = bateaux[symbole]
#         liste = []
#         while placer==False:    
#             ligne = random.randint(0,9)
#             colonne = random.randint(0,9)
#             orientation = random.choice(["H","V"])
#             if orientation=="H":
#                 if(colonne+taille)<=10 and all(grille[ligne][colonne+i]==" " for i in range(taille)):
#                     for i in range(taille):
#                         grid_act[ligne][colonne+i] = symbole
#                         liste.append((ligne,colonne+i))
#                     placer=True
#             if orientation=="V":
#                 if(ligne+taille)<=10 and all(grille[ligne+i][colonne]==" " for i in range(taille)):
#                     for i in range(taille):
#                         grid_act[ligne+i][colonne] = symbole
#                         liste.append((ligne+i,colonne))
#                     placer=True
#         dict_bateau[symbole] = liste
#     return dict_bateau
        
# print(placer_bateau_aleatoire(grid_act))
#{'P': [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5)], 'C': [(1, 8), (2, 8), (3, 8), (4, 8)], 'S': [(6, 7), (7, 7), (8, 7)], 'T': [(8, 3), (8, 4)], 'B': [(5, 0)]}

if  __name__ == "__main__" :
    grid_act = np.full(shape= [10,10], fill_value= " ")
    coord_list = ["A","B","C","D","E","F","G","H","I","J"]
    Affichage(gird= grid_act, coords= coord_list)
    x = input("Enter the row to attack : ")
    y = input("Enter the column to attack : ")
    attack(x,y)

