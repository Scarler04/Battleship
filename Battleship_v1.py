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


if  __name__ == "__main__" :
    grid_act = np.full(shape= [10,10], fill_value= " ")
    coord_list = ["A","B","C","D","E","F","G","H","I","J"]
    Affichage(gird= grid_act, coords= coord_list)
    x = input("Enter the row to attack : ")
    y = input("Enter the column to attack : ")
    attack(x,y)
