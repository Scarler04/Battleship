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
                - str: "Fail" if coordinates already attacked, "Miss" if missed, or boat name if hit
                - bool: True if a boat was sunk, False otherwise
                - int: Updated player score
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
                - list | None: List of coordinates if the placement succeeds, else None.
                - str: Status message describing the result of placement.
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
    """
    Class representing the AI Battleship player

    Parameters
    ----------
        name : str
            Name of the bot
        diff : int, optional
            Difficulty level (0 = random attacks, 1 = smarter bot)
        hit_coords : list
            Coordinates of previously hit boat segments that belong to boats not yet sunk
    """

    def __init__(self, name, diff = 0):
        super().__init__(name)
        self.difficulty = diff
        self.hit_coords = []

    def random_func(self, weights=None):
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

    def place_boats(self, weights=None):  
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
                weights_dynamiques = self.calculer_poids_uniformite(case_occupe, weights)
                
                ligne, colonne = self.random_func(weights_dynamiques)
                orientation = random.choice(["H","V"])
                
                pos = self.tenter_placement_uniform(ligne, colonne, taille, orientation)
                
                if pos == []:
                    orientation_alt = "V" if orientation == "H" else "H"
                    pos = self.tenter_placement_uniform(ligne, colonne, taille, orientation_alt)
                
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
                pos = self.placement_force(taille, case_occupe)
                if pos:
                    dict_bateau[symbole] = pos
                    case_occupe.extend(pos)
        
        return dict_bateau


    def calculer_poids_uniformite(self, case_occupe:list, weights_base=None):
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


    def tenter_placement_uniform(self, ligne : int, colonne : int, taille : int, orientation : str):
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


    def placement_force(self, taille : int, case_occupe : list):
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
                    pos = self.tenter_placement_uniform(ligne, colonne, taille, orientation)
                    
                    if pos:
                        valide = True
                        for k in pos:
                            if k in case_occupe:
                                valide = False
                                break
                        
                        if valide:
                            return pos
        
        return []

    def attack (self, grid : np.ndarray, boat_coord : dict[str, list[tuple[int, int]]]) :
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
            # Identifier toutes les cases non attaquées
            indexes = np.where(~np.isin(grid, ["*", "+", "X"]))
            L = [(i,j) for i, j in zip(indexes[0],indexes[1])]

            # Choisir et attaquer une case aléatoirement
            attack_coords = random.choice(L)
            boat_hit, sunk, _ = self.register_attack(x= attack_coords[0], y= attack_coords[1],boat_coord= boat_coord, attack_grid= grid, score= None, coord_list= None, player= False)
            return boat_hit, sunk
        elif self.difficulty == 1 :
            invalids = ["*", "+", "X"]
            if len(self.hit_coords) == 0 :
                indexes = np.where(~np.isin(grid, invalids))
                L = [(i,j) for i, j in zip(indexes[0],indexes[1])]
                attack_coords = random.choice(L)
                boat_hit, sunk, _ = self.register_attack(x= attack_coords[0], y= attack_coords[1],boat_coord= boat_coord, attack_grid= grid, score= None, coord_list= None, player= False)

                if (boat_hit != "Miss") & (boat_hit != "Fail") & (not sunk):
                    self.hit_coords.append((attack_coords[0] , attack_coords[1]))
                elif sunk :
                    self.hit_coords = [ coords for coords in self.hit_coords if grid[coords[0]][coords[1]] != "X"]
                return boat_hit, sunk
            
            else :
                (x,y) = self.hit_coords[0]
                if ((x,y-1) in self.hit_coords[:1]) | ((x,y+1) in self.hit_coords[:1]) :
                    orient = 0 # Horizontal
                elif ((x-1,y) in self.hit_coords[:1]) | ((x+1,y) in self.hit_coords[:1]) :
                    orient = 1 # Vertical
                else :
                    if x in [0,9] :
                        orient = 0
                    elif y in [0,9] :
                        orient = 1
                    else :
                        orient = int(int(grid[x][y-1] not in invalids) + int(grid[x][y+1] not in invalids) > int(grid[x-1][y] not in invalids) + int(grid[x+1][y] not in invalids)) # 1 s'il y a plus de cases disponibles à l'horizontal, 0 sinon
                
                attempts = 1
                fire = False
                while (attempts <= 2) & (not fire):
                    lineup = [(x,y)]

                    if orient is not None :
                        dx, dy = (1,0) if orient == 1 else (0,1)

                        i = 1
                        while (x + i*dx, y + i*dy) in self.hit_coords :
                            lineup.append ((x + i*dx, y + i*dy))
                            i+= 1

                        j = 1
                        while (x - j*dx, y - j*dy) in self.hit_coords :
                            lineup.insert (0, (x - j*dx, y - j*dy))
                            j+= 1
                        
                        (a_up, b_up) = (x + i*dx, y + i*dy)
                        (a_down, b_down) = (x - j*dx, y - j*dy)

                        # Check if grid border reached
                        end_up = False
                        end_down = False
                        if -1 in (a_down, b_down) :
                            end_down = True
                        if 10 in (a_up, b_up) :
                            end_up = True
    
                        if not end_down :
                            if grid[a_down][b_down] not in invalids :
                                boat_hit, sunk, _ = self.register_attack(x= a_down, y= b_down, boat_coord= boat_coord, attack_grid= grid, score= None, coord_list= None, player= False)
                                fire = True

                                if (boat_hit != "Miss") & (boat_hit != "Fail") & (not sunk) :
                                    self.hit_coords.append((a_down , b_down))
                            
                        if (not end_up) & (not fire):
                            if grid[a_up][b_up] not in invalids :
                                boat_hit, sunk, _ = self.register_attack(x= a_up, y= b_up, boat_coord= boat_coord, attack_grid= grid, score= None, coord_list= None, player= False)
                                fire = True

                                if (boat_hit != "Miss") & (boat_hit != "Fail") & (not sunk):
                                    self.hit_coords.append((a_up , b_up))                                    
                    
                    if not fire :
                        attempts +=1
                        orient = (orient + 1) % 2 # Change orientation
                
                if fire :
                    if sunk :
                        self.hit_coords = [ coords for coords in self.hit_coords if grid[coords[0]][coords[1]] != "X"]
                    return boat_hit, sunk
                else :
                    indexes = np.where(~np.isin(grid, ["*", "+", "X"]))
                    L = [(i,j) for i, j in zip(indexes[0],indexes[1])]
                    attack_coords = random.choice(L)
                    boat_hit, sunk, _ = self.register_attack(x= attack_coords[0], y= attack_coords[1],boat_coord= boat_coord, attack_grid= grid, score= None, coord_list= None, player= False)

                    if (boat_hit != "Miss") & (boat_hit != "Fail") & (not sunk):
                        self.hit_coords.append((attack_coords[0] , attack_coords[1]))
                    return boat_hit, sunk
