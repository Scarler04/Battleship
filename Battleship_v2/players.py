import numpy as np
import random
from interface import placing_boats_grid

class BasePlayer :
    """
    Base class for all Battleship players.

    Parameters
    ----------
        name : str
            Name of the player.

    Attributes
    ----------
        name : str
            Player's display name.
        boats_left : int
            Number of boats still afloat.
        grid : ndarray
            10x10 grid representing the player's board.
        boat_coords : dict[str, list[tuple[int, int]]]
            Dictionary mapping boat symbols to lists of occupied coordinates.
    """

    def __init__ (self, name) :
        self.name = name 
        self.boats_left = 5
        self.grid = np.full(shape= [10,10], fill_value= " ")
        self.boat_coords = {}

    def register_attack (self, x : str, y : int, boat_coord : dict[str, list[tuple[int, int]]], attack_grid : np.ndarray, score : int, coord_list : list[str], player : bool) :
        """
        Process an attack on the battleship grid

        Parameters
        ----------
            x : str
                Row coordinate of attack
            y : int
                Column coordinate of attack
            boat_coord : dict
                Dictionnary containing all boat coordinates of attacked player
            attack_grid : array
                Current grid of attacked player
            score : int
                Current number of human player attempts
            coord_list : list
                Names of rows (x)
            player : bool
                True if player attack, False if bot attack
        
        Returns
        ----------
            tuple: A tuple containing:
                - str : "Fail" if coordinates already attacked, "Miss" if missed, or boat name if hit
                - bool : True if a boat was sunk, False otherwise
                - int : Updated player score
        """
        if player :
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
                    if player :
                        score += 1
                    sunk = self.check_sink(boat_hit= boat,boat_coord= boat_coord, attack_grid= attack_grid)
                    hit = boat # Store boat key
            if hit == None :
                attack_grid[x][y] = "*" # "*" = Attack missed
                if player :
                    score += 1
                sunk = False
                hit = "Miss"
        return hit, sunk, score

    def check_sink (self, boat_hit : str, boat_coord : dict[str, list[tuple[int, int]]], attack_grid : np.ndarray):
        """
        Check if attack sinks a boat

        Parameters
        ----------
            boat_hit : str
                Symbol of the boat hit by the attack
            boat_coord : dict
                Dictionnary containing all boat coordinates of attacked player
            attack_grid : array
                Current grid of attacked player
        
        Returns
        ----------
            bool : 
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




class Player (BasePlayer) :
    """
    Class representing a human Battleship player.

    Parameters
    ----------
        name : str
            Username of the player

    Attributes
    ----------
        score : int
            Number of valid attack attempts made by the player
    """

    def __init__(self, name):
        super().__init__(name)
        self.score = 0

    def place_boat (self, symbole, nom, taille, x, y, orientation, cases_occup, coord_list):
        """
        Place a boat on the player's grid.

        Parameters
        ----------
            symbole : str
                Boat symbol used on the grid
            nom : str
                Full name of the boat
            taille : int
                Length of the boat
            x : str
                Row coordinate of the boat (A-J)
            y : str
                Column coordinate of the boat (1-10).
            orientation : str
                Orientation of the boat: "H" for horizontal or "V" for vertical.
            cases_occup : list
                List of already occupied grid coordinates.
            coord_list : list
                List of allowed row labels ("A"-"J").

        Returns
        ----------
            tuple :
                - list | None : List of coordinates if the placement succeeds, else None.
                - str : Status message describing the result of placement.
        """
        
        if x.upper() not in coord_list or not y.isdigit():
            return None, "Coordonnées invalides."

        ligne = coord_list.index(x.upper())
        col = int(y) - 1

        if col < 0 or col >= 10:
            return None, "Coordonnées invalides."
        poss = True
        pos = [] #position
        if orientation == "H":
            if col + taille > 10:
                poss = False
            else :
                for i in range(taille):
                    pos.append((ligne, col + i))
        else:
            if ligne + taille > 10:
                poss = False
            else :
                for i in range(taille):
                    pos.append((ligne + i, col))

        if poss is False:
            return None, "Le bateau dépasse de la grille."

        if any(p in cases_occup for p in pos) : # Chevauchement
            return None, "Le bateau chevauche un autre."

        for (l, c) in pos: # placer bateau
            self.grid[l][c] = symbole
            cases_occup.append((l, c))
        return pos, f"{nom} placé !"





class Bot (BasePlayer) :

    def __init__(self, name, diff = 0):
        super().__init__(name)
        self.difficulty = diff

    def place_boats (self) :
        """
        Generates random boat coordinates
        
        Returns
        ----------
            dict :
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

    def attack (self, grid : np.ndarray, boat_coord) :
        """
        Perform an attack, depending on the bot's difficulty level.

        Parameters:
            grid : ndarray
                Grid to attack
            boat_coord : dict
                Dictionnary containing all boat coordinates of attacked player

        Returns:
            tuple:
                - str: "Miss", "Fail", or the boat symbol if a boat was hit.
                - bool: True if the targeted boat was sunk, False otherwise.
        """
        if self.difficulty == 0 :
            indexes = np.where(~np.isin(grid, ["*", "+", "X"]))
            L = [(i,j) for i, j in zip(indexes[0],indexes[1])]
            attack_coords = random.choice(L)
            boat_hit, sunk, score = self.register_attack(x= attack_coords[0], y= attack_coords[1],boat_coord= boat_coord, attack_grid= grid, score= None, coord_list= None, player= False)
            return boat_hit, sunk
        elif self.difficulty == 1 :
            pass
