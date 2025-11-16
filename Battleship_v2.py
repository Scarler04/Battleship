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


#def placer_bateau_joueur():
#     nombres_bateaux_places = 0
#     boat_names = {"P":("le Porte-Avion",5), "C": ("le Croiseur",4), "S" : ("le Sous-marin",3), "T" : (" le Torpilleur",2), "B" : ("la Barque",1)}
#     coord_list = ["A","B","C","D","E","F","G","H","I","J"]
#     cases_occup = [] 
#     dict_bateaux = {}
#     message = "Placement des bateaux"
#     attack_grid = np.full(shape= [10,10], fill_value= " ")
#     show_grid(grid=attack_grid, coords=coord_list, score=0, message=message)
#     for symbole,(nom,nombre) in boat_names.items():
#         placement_valide = False
#         while not placement_valide:
#             show_grid(grid=attack_grid, coords=coord_list, score=0, message=f"Placez : {nom}")
#             print(f'Où voulez-vous placer votre {nom} ({nombre} cases)?')
#             x = input("Ligne : ")
#             y = input("Colonne : ")
#             if nombre > 1:
#                 orientation = input("Horizontale(H) / Verticale(V) : ").upper()
#             else:
#                 orientation = "H"  
#             if (x.upper() in coord_list) & (y.isnumeric()) & (orientation.upper() in ["H","V"]):
#                 if 1<=int(y)<=10 :
#                     pos = []
#                     ligne = coord_list.index(x)
#                     col = int(y) - 1
#                     if orientation=="H":
#                         if col+nombre<=10:              
#                             for i in range(nombre):
#                                 p = (ligne,col+i)        
#                                 pos.append(p)               
#                         else:
#                             pos = []                        
#                     else:                                   
#                         if ligne+nombre<=10:
#                             for i in range(nombre):
#                                 p = (ligne+i,col)
#                                 pos.append(p)
#                         else:
#                             pos = []
#                 if pos!=[]:
#                     chevauchement = False
#                     for k in pos:
#                         if k in cases_occup:
#                             chevauchement=True
#                     if chevauchement==False:
#                         dict_bateaux[symbole] = pos 
#                         for x in pos:
#                             cases_occup.append(x)       
#                     for (l,c) in pos:
#                         attack_grid[l][c] = symbole
#                     placement_valide = True
#             else:
#                 message = "Coordonnées invalides... Réessayez !"
#         else:
#             message = "Coordonnées invalides... Réessayez !"

#         message = f"{nom} placé !"
#         show_grid(grid=attack_grid, coords=coord_list, score=0, message=message)

# placer_bateau_joueur()
    


if  __name__ == "__main__" :
    grid_act = np.full(shape= [10,10], fill_value= " ")
    coord_list = ["A","B","C","D","E","F","G","H","I","J"]
    Affichage(gird= grid_act, coords= coord_list)

