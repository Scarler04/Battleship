import numpy as np
import random

def show_grid(grid : np.ndarray, coords : list, score : int, message : str):
    """
    Displays current grid and score

    Parameters
    -------
        grid : array
            The grid with values to display
        coords : list
            List of column indexes de display
        score : int
            Current player score (number of tries)
        message : str 
            Message to display
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

    Parameters
    -------
        x : str
            Row coordinate of player attack
        y : int
            Column coordinate of player attack
        boat_coord : dict
            Dictionnary with boat coordinates
        attack_grid : array
            Current grid with player hits and misses
        score : int
            Current number of player attempts
        coord_list : list 
            Names of rows (x)
    
    Returns
    -------
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


def check_sink (boat_hit : str, boat_coord : dict[str, list[tuple[int, int]]], attack_grid : np.ndarray):
    """
    Check if player attack sinks a boat

    Parameters
    -------
        boat_hit : str
            Name of the boat hit by the attack
        boat_coord : dict
            Dictionnary with boat coordinates
        attack_grid : array 
            Current grid with player hits and misses
    
    Returns
    -------
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

def random_func(weights=None):
    """
    Generate random coordinates on the grid
    
    Parameters
    ----------
        weights : array, optional
            2D array (10x10) of probability weights for each cell
            
    Returns
    -------
        tuple: A tuple containing:
            - int: Row coordinate (0-9)
            - int: Column coordinate (0-9)
    """
    if weights is None:
        return random.randint(0,9), random.randint(0,9)
    else:
        # Flatten weights and create probability distribution
        flat_weights = weights.flatten()
        flat_weights = flat_weights / flat_weights.sum()  # Normalize
        
        # Choose a cell index based on weights
        cell_idx = np.random.choice(100, p=flat_weights)
        ligne = cell_idx // 10
        colonne = cell_idx % 10
        return ligne, colonne

def place_boats(weights=None):  
    """
    Generate boat coordinates with maximum uniform distribution
    Uses repulsion strategy to spread boats evenly across the grid
    
    Parameters
    ----------
        weights : array, optional
            2D array (10x10) of base probability weights for initial placement
            
    Returns
    -------
        dict: A dictionary with boat names as keys and lists of boat coordinates as tuples of two integers as values
    """
    bateaux = {"P":5,"C":4,"S":3,"T":2,"B":1}
    dict_bateau = {}
    case_occupe = []
    
    for symbole, taille in bateaux.items():
        invalid = False
        tentatives = 0
        max_tentatives = 1000
        
        while invalid == False and tentatives < max_tentatives:
            tentatives += 1
            
            # Générer poids dynamiques basés sur la densité actuelle
            weights_dynamiques = calculer_poids_uniformite(case_occupe, weights)
            
            ligne, colonne = random_func(weights_dynamiques)
            orientation = random.choice(["H","V"])
            
            pos = tenter_placement_uniform(ligne, colonne, taille, orientation)
            
            if pos == []:
                orientation_alt = "V" if orientation == "H" else "H"
                pos = tenter_placement_uniform(ligne, colonne, taille, orientation_alt)
            
            if pos != []:
                chevauchement = False
                for k in pos:
                    if k in case_occupe:
                        chevauchement = True
                        break
                
                if chevauchement == False:
                    dict_bateau[symbole] = pos
                    case_occupe.extend(pos)
                    invalid = True
        
        # Fallback si max_tentatives atteint
        if not invalid:
            pos = placement_force(taille, case_occupe)
            if pos:
                dict_bateau[symbole] = pos
                case_occupe.extend(pos)
    
    return dict_bateau


def calculer_poids_uniformite(case_occupe, weights_base=None):
    """
    Calculate weights that favor less occupied zones
    Creates a density map and inverts weights to promote uniform distribution
    
    Parameters
    ----------
        case_occupe : list
            List of tuples representing already occupied cells
        weights_base : array, optional
            2D array (10x10) of base weights to combine with density weights
            
    Returns
    -------
        array: Normalized 2D array (10x10) of probability weights
    """
    grille_densite = np.zeros((10, 10))
    
    # Calculer densité autour de chaque case occupée
    for ligne, colonne in case_occupe:
        for dl in range(-2, 3):
            for dc in range(-2, 3):
                nl, nc = ligne + dl, colonne + dc
                if 0 <= nl < 10 and 0 <= nc < 10:
                    distance = max(abs(dl), abs(dc))
                    grille_densite[nl, nc] += 1.0 / (distance + 1)
    
    # Inverser les poids: zones denses = poids faibles
    poids = 1.0 / (grille_densite + 1.0)
    
    # Combiner avec weights_base si fourni
    if weights_base is not None:
        poids = poids * weights_base
    
    # Normaliser
    poids = poids / poids.sum()
    
    return poids


def tenter_placement_uniform(ligne, colonne, taille, orientation):
    """
    Attempt to place a boat at given coordinates
    Uses adaptive logic to try alternative placements if initial position is invalid
    
    Parameters
    ----------
        ligne : int
            Row coordinate for boat placement
        colonne : int
            Column coordinate for boat placement
        taille : int
            Length of the boat to place
        orientation : str
            Orientation of the boat ("H" for horizontal, "V" for vertical)
            
    Returns
    -------
        list: List of tuples representing boat coordinates if placement is valid,
              empty list otherwise
    """
    pos = []
    
    if orientation == "H":
        if colonne + taille <= 10:
            pos = [(ligne, colonne + i) for i in range(taille)]
        elif colonne - taille + 1 >= 0:
            pos = [(ligne, colonne - i) for i in range(taille)]
    else:
        if ligne + taille <= 10:
            pos = [(ligne + i, colonne) for i in range(taille)]
        elif ligne - taille + 1 >= 0:
            pos = [(ligne - i, colonne) for i in range(taille)]
    
    return pos


def placement_force(taille, case_occupe):
    """
    Force boat placement as last resort
    Systematically searches for a valid position on the grid
    
    Parameters
    ----------
        taille : int
            Length of the boat to place
        case_occupe : list
            List of tuples representing already occupied cells
            
    Returns
    -------
        list: List of tuples representing boat coordinates if valid position found,
              empty list if no valid position exists
    """
    for ligne in range(10):
        for colonne in range(10):
            for orientation in ["H", "V"]:
                pos = tenter_placement_uniform(ligne, colonne, taille, orientation)
                
                if pos:
                    valide = True
                    for k in pos:
                        if k in case_occupe:
                            valide = False
                            break
                    
                    if valide:
                        return pos
    
    return []


def main () :
    """
    Starts Battleship game
    """
    coord_list = ["A","B","C","D","E","F","G","H","I","J"] # List of row indexes
    boat_names = {"P":"le Porte-Avion", "C": "le Croiseur", "S" : "le Sous-marin", "T" : "le Torpilleur", "B" : "la Barque"} # Boat names (for boat sunk message)
    play = True
    try :
        weights = np.load('weightmap_boats.npy')
    except :
        weights = None
    # Loop while player wants to play
    while play :
        message = ""
        boats_left = 5
        won = False
        score = 0
        attack_grid = np.full(shape= [10,10], fill_value= " ")
        boat_coords = place_boats(weights)
        # Start new game
        while won == False :
            show_grid (grid= attack_grid, coords= coord_list, score= score, message= message)
            x = input("Enter the row to attack (A-J) : ")
            y = input("Enter the column to attack (1-10) : ")
            # Check if input is valid
            if (x.upper().strip() in coord_list) & (y.isnumeric()) :
                if 1<=int(y)<=10 :
                    boat_hit, sunk, score = attack(x,int(y),boat_coords,attack_grid,score,coord_list)
                    if sunk :
                        message = f'Vous avez coulé {boat_names[boat_hit]} !'
                        boats_left -= 1
                        if boats_left == 0 :
                            won = True
                    elif (boat_hit != "Miss") & (boat_hit != "Fail") :
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


if  __name__ == "__main__" :
    try :
        main()
    except :
        print("An error has occured, please check game requirements")
