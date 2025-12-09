import random
import numpy as np


def game_init () :
    """
    Initialize player classes variables

    Returns
    ----------
        tuple: A tuple containing:
            - str: Player's username
            - int: Bot level of difficulty
            - str: Bot name
    """

    username = input("Please enter your username :\n")
    if not username :
        username = "Anonymous"
    difficulties = ["Easy", "Hard"]
    diff = None
    while diff == None :
        d = input("Choose difficulty (Easy/Hard):\n")
        try :
            diff = difficulties.index(d.lower().capitalize().strip()) # Get difficulty as integer 0-1
        except ValueError :
            print("Invalid Input")
    bot_name = random.choice(["Laurent Beaudou","François Bouchon","Terminator","Stephanie Leger"])
    return username, diff, bot_name


def placing_boats_grid (grid : np.ndarray, coords : list, message : str):
    """
    Displays current player grid

    Parameters
    ----------
        grid : array
            The boat grid to display
        coords : list
            List of column indexes de display
        message : str 
            Message to display
    """

    print("Bataille Navale :\n\n")
    print("    " + "   ".join(str(i) for i in range(1, 11)))
    
    sep = "   " + "-" * 39
    
    for i, row in enumerate(grid):
        print(sep)
        if i == 7 :
            print(f"{coords[i]} | " + " | ".join(row) + " |" + f"     {message}")
        else :
            print(f"{coords[i]} | " + " | ".join(row) + " |")
    
    print(sep)


def show_grids (boat_grid : np.ndarray, attack_grid : np.ndarray, coords : list, score : int, message : str) :
    """
    Displays current grid and score

    Parameters
    ----------
        boat_grid : array
            Player grid with boats
        attack_grid : array
            The attack grid with values to display
        coords : list
            List of column indexes de display
        score : int
            Current player score (number of tries)
        message : str
            Message to display
    """

    print("Bataille Navale :\n\n")
    print("    " + "   ".join(str(i) for i in range(1, 11))+ " "*20 + "   ".join(str(i) for i in range(1, 11))) # Print column index
    
    sep = "   " + "-" * 39 + " "*20 + "-" * 39 
    
    # Display grid
    for i, (row1, row2) in enumerate(zip(boat_grid, attack_grid)):
        print(sep)
        if i == 5 :
            print(f"{coords[i]} | " + " | ".join(row1) + " |" + " "*16 + f"{coords[i]} | " + " | ".join(row2) + " |" + f"            Nombre de tirs : {score}") # Display grid and current player score on row 5
        elif i == 7 : 
            print(f"{coords[i]} | " + " | ".join(row1) + " |" + " "*16 + f"{coords[i]} | " + " | ".join(row2) + " |" + f"            {message}") # Display grid and message on row 7
        else :
            print(f"{coords[i]} | " + " | ".join(row1) + " |" + " "*16 + f"{coords[i]} | " + " | ".join(row2) + " |" )
    
    print(sep)


def ascii_art (player_won : bool) :
    """
    Show ascii art depending on game outcome
    
    Parameters
    ----------
        player_won : bool
            True if player won, False otherwise
    """
    if player_won :
        print(r" /$$     /$$ /$$$$$$  /$$   /$$       /$$      /$$  /$$$$$$  /$$   /$$")
        print(r"|  $$   /$$//$$__  $$| $$  | $$      | $$  /$ | $$ /$$__  $$| $$$ | $$")
        print(r" \  $$ /$$/| $$  \ $$| $$  | $$      | $$ /$$$| $$| $$  \ $$| $$$$| $$")
        print(r"  \  $$$$/ | $$  | $$| $$  | $$      | $$/$$ $$ $$| $$  | $$| $$ $$ $$")
        print(r"   \  $$/  | $$  | $$| $$  | $$      | $$$$_  $$$$| $$  | $$| $$  $$$$")
        print(r"    | $$   | $$  | $$| $$  | $$      | $$$/ \  $$$| $$  | $$| $$\  $$$")
        print(r"    | $$   |  $$$$$$/|  $$$$$$/      | $$/   \  $$|  $$$$$$/| $$ \  $$")
        print(r"    |__/    \______/  \______/       |__/     \__/ \______/ |__/  \__/")
    else :
        print(r"  /$$$$$$   /$$$$$$  /$$      /$$ /$$$$$$$$        /$$$$$$  /$$    /$$ /$$$$$$$$ /$$$$$$$ ")
        print(r" /$$__  $$ /$$__  $$| $$$    /$$$| $$_____/       /$$__  $$| $$   | $$| $$_____/| $$__  $$")
        print(r"| $$  \__/| $$  \ $$| $$$$  /$$$$| $$            | $$  \ $$| $$   | $$| $$      | $$  \ $$")
        print(r"| $$ /$$$$| $$$$$$$$| $$ $$/$$ $$| $$$$$         | $$  | $$|  $$ / $$/| $$$$$   | $$$$$$$/")
        print(r"| $$|_  $$| $$__  $$| $$  $$$| $$| $$__/         | $$  | $$ \  $$ $$/ | $$__/   | $$__  $$")
        print(r"| $$  \ $$| $$  | $$| $$\  $ | $$| $$            | $$  | $$  \  $$$/  | $$      | $$  \ $$")
        print(r"|  $$$$$$/| $$  | $$| $$ \/  | $$| $$$$$$$$      |  $$$$$$/   \  $/   | $$$$$$$$| $$  | $$")
        print(r" \______/ |__/  |__/|__/     |__/|________/       \______/     \_/    |________/|__/  |__/")


if __name__ == "__main__" :
    print(game_init())
    show_grids(np.full([10,10],"P"),np.full([10,10],"*"),["A","B","C","D","E","F","G","H","I","J"],3,"Nope")
