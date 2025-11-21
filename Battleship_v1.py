import numpy as np
import random

def show_grid(grid, coords,score, message):
    """
    Displays current grid and score

    Parameters:
        grid (array): The grid with values to display
        coords (list): List of column indexes de display
        score (int): Current player score (number of tries)
        message (str): Message to display
    """

    print("Bataille Navale :\n\n")
    print("    " + "   ".join(str(i) for i in range(1, 11))) # Print column index
    
    sep = "   " + "-" * 39 
    
    # Display grid
    for i, row in enumerate(grid):
        print(sep)
        if i == 5 :
            print(f"{coords[i]} | " + " | ".join(row) + " |" + f"            Nombre de tirs : {score}") # Display grid and current player score on row 5
        elif i == 7 : 
            print(f"{coords[i]} | " + " | ".join(row) + " |" + f"            {message}") # Display grid and message on row 7
        else :
            print(f"{coords[i]} | " + " | ".join(row) + " |")
    
    print(sep)

def attack (x : str, y : int, boat_coord : dict[str, list[tuple[int, int]]], attack_grid : np.ndarray, score : int, coord_list : list[str]) :
    """
    Process an attack on the battleship grid

    Parameters:
        x (str): Row coordinate of player attack
        y (int): Column coordinate of player attack
        boat_coord (dict): Dictionnary with boat coordinates
        attack_grid (array): Current grid with player hits and misses
        coord_list (list): Names of rows (x)
    
    Returns:
        tuple: A tuple containing:
            - str: "Fail" if coordinates already attacked, "Miss" if missed, or boat name if hit
            - bool: True if a boat was sunk, False otherwise
            - int: Updated player score
    """
    x = coord_list.index(x.upper().strip()) # Get row index from letter input (A-J => 0-9)
    y -= 1 # Get column index : array index is 0-9, player index/input is 1-10

    hit = None # No boats hit by default

    # Check if player already attacked these coordinates
    if attack_grid[x][y] in ["*","+","X"] :
        hit = "Fail"
        sunk = False
    else :
        # Check each boat to see if attack hit it
        for boat, all_coords in boat_coord.items() :
            if (x,y) in all_coords :
                attack_grid[x][y] = "+" # "+" = Boat hit
                score += 1
                sunk = check_sink(boat_hit= boat,boat_coord= boat_coord, attack_grid= attack_grid)
                hit = boat # Store boat key
        if hit == None :
            attack_grid[x][y] = "*" # "*" = Attack missed
            score += 1
            sunk = False
            hit = "Miss"
    return hit, sunk, score


def check_sink (boat_hit, boat_coord, attack_grid):
    """
    Check if player attack sinks a boat

    Parameters:
        boat_hit (str): Name of the boat hit by the attack
        boat_coord (dict): Dictionnary with boat coordinates
        attack_grid (array): Current grid with player hits and misses
    
    Returns:
        bool: 
            True if boat is sunk, False otherwise
    """

    hits = 0

    # Go through coordinates of designated boat
    for coords in boat_coord[boat_hit] :
        # Check how many of the boat's coordinates were hit
        if attack_grid[coords[0]][coords[1]] == "+" :
            hits += 1
        elif attack_grid[coords[0]][coords[1]] == " " :
            return False # Boat is not sunk as soon as we find a coordinate not attacked
    # Check if boat was hit on all coordinates
    if hits == len(boat_coord[boat_hit]) :
        for coords in boat_coord[boat_hit] :
            attack_grid[coords[0]][coords[1]] = "X" # "X" = Boat sunk
        return True 
    else :
        return False

def place_boats():  
    """
    Generates random boat coordinates
    
    Returns:
        dict:
            A dictionnary with boat names as keys and lists of boat coordinates as tuples of two integers as items
    """
    bateaux = {"P":5,"C":4,"S":3,"T":2,"B":1}       # Dictionary of boat lengths
    dict_bateau = {}                                
    case_occupe = []
    for symbole,taille in bateaux.items():          # Browse the dictionary that we introduce at the begining
        invalid = False                             # Booleen to see if we can put the boat or no (if the boat exceeds the grid or if the boat overlap another boat )
        while invalid==False:    
            ligne = random.randint(0,9)             # Stock the random coordonate in the variable "ligne" and the variable "colonne"
            colonne = random.randint(0,9)
            orientation = random.choice(["H","V"])  # Choose boat direction (H : horizontal, V : vertical)
            pos = []
            if orientation=="H":
                if colonne+taille<=10:              # Check if the boat fits on the grid using generated coordinates and direction
                    for i in range(taille):
                        p = (ligne,colonne+i)        
                        pos.append(p)               # List of boat's coordinates
                else:
                    pos = []                        
            else:                                    # Same for vertical
                if ligne+taille<=10:
                    for i in range(taille):
                        p = (ligne+i,colonne)
                        pos.append(p)
                else:
                    pos = []
            if pos!=[]:
                chevauchement = False
                for k in pos:
                    if k in case_occupe:
                        chevauchement=True
                if chevauchement==False:
                    dict_bateau[symbole] = pos 
                    for x in pos:
                        case_occupe.append(x)       # We add the coordinates in the list to make sure that we have no duplicates
                    invalid=True
    return dict_bateau



if  __name__ == "__main__" :   
    coord_list = ["A","B","C","D","E","F","G","H","I","J"] # List of row indexes
    boat_names = {"P":"le Porte-Avion", "C": "le Croiseur", "S" : "le Sous-marin", "T" : " le Torpilleur", "B" : "la Barque"} # Boat names (for boat sunk message)
    play = True 
    # Loop while player wants to play
    while play :
        message = ""
        boats_left = 5
        won = False
        score = 0
        attack_grid = np.full(shape= [10,10], fill_value= " ")
        boat_coords = place_boats()
        # Start new game
        while won == False :
            show_grid (grid= attack_grid, coords= coord_list, score= score, message= message)
            x = input("Enter the row to attack (A-J) : ")
            y = input("Enter the column to attack (1-10) : ")
            # Check if input is valid
            if (x.upper().strip() in coord_list) & (y.strip().isnumeric()) :
                if 1<=int(y)<=10 :
                    boat_hit, sunk, score = attack(x,int(y),boat_coords,attack_grid,score,coord_list)
                    if sunk :
                        message = f'Vous avez coulé {boat_names[boat_hit]} !'
                        boats_left -= 1
                        if boats_left == 0 :
                            won = True
                    elif (boat_hit != "Miss") & (boat_hit != "Fail") :
                        print(boat_hit)
                        message = "Touché !"
                    elif boat_hit == "Miss" :
                        message = 'Raté !'
                    elif (boat_hit == "Fail") :
                        message = "Vous avez déjà essayer à cet endroit... Réessayez !"
                else : 
                    message = "Coordonnées invalides... Réessayez !"
            else : 
                message = "Coordonnées invalides... Réessayez !"
        
        show_grid (grid= attack_grid, coords= coord_list, score= score, message= message)
        print ("Vous avez gagné !!")
        print (f'Il vous aura fallu {score} tirs !')
        play_again = ""
        while play_again.upper().strip() not in ["O","N"] :
            play_again = input("Voulez vous rejouer ? (O/N)\n")
        if play_again.upper().strip() == "N" :
            play = False

