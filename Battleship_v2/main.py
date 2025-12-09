import random

from exceptions import BotLoopError
from database import create_database, update_scoreboard
from players import Player, Bot
from interface import game_init, placing_boats_grid, show_grids, ascii_art

def main ():
    """
    Starts Battleship game
    """
    # Initialising
    player_name ,diff ,bot_name = game_init()
    players = [player_name, bot_name]

    P = Player (player_name)
    B = Bot (bot_name,diff)
    # Scoreboard Init and upadte
    scoreboard_path = create_database()
    if not scoreboard_path :
        print("Scoreboard not found")
    # update_scoreboard("Test",50,scoreboard_path)
    
    coord_list = ["A","B","C","D","E","F","G","H","I","J"]
    boat_names = {
        "P": ("Porte-Avion", 5),
        "C": ("Croiseur", 4),
        "S": ("Sous-marin", 3),
        "T": ("Torpilleur", 2),
        "B": ("Barque", 1)
    }

    # Placing player bots
    cases_occup = []
    P.boat_coords.clear()

    message = "Placing boats"
    placing_boats_grid(P.grid, coord_list, message)

    for symbole, (nom, taille) in boat_names.items():
        valide = False
        while not valide:
            print(f"Where do you want to place the {nom} (length {taille}) ?")
            x = input("Row (A-J) : ")
            y = input("Column (1-10) : ")

            orientation = "H"
            if taille > 1:
                orientation = input("Orientation H/V : ").upper()

            pos, message = P.place_boat(symbole, nom, taille, x, y, orientation, cases_occup, coord_list)

            placing_boats_grid(grid= P.grid, coords= coord_list, message= message)

            if pos is not None:
                P.boat_coords[symbole] = pos
                valide = True

    OK = True
    while OK:
        o = input("Do you want to change a boat's position ? (Y/N) : ").upper().strip()
        if o == "N":
            OK = False
        elif o == "Y":
            s = input("Which boat ? (P/C/S/T/B) : ").upper().strip()
            if s in boat_names:
                nom, taille = boat_names[s]
                anciennes = P.boat_coords[s]
                for (l, c) in anciennes:
                    P.grid[l][c] = " "
                    cases_occup.remove((l, c))

                placing_boats_grid(grid= P.grid, coords= coord_list, message= "Boat deleted")

                valide = False

                while not valide:
                    print(f"New coordinates for {nom} (length {taille})")
                    x = input("Row (A-J) : ")
                    y = input("Column (1-10) : ")

                    orientation = "H"
                    if taille > 1:
                        orientation = input("Orientation H/V : ").upper()

                    nouvelles, message = P.place_boat(symbole= s, nom= nom, taille= taille, x= x, y= y, orientation= orientation, cases_occup= cases_occup, coord_list= coord_list)

                    placing_boats_grid(grid= P.grid, coords= coord_list, message= message)

                    if nouvelles is not None :
                        valide = True

                P.boat_coords[s] = nouvelles
            else:
                print("Invalid symbol")
        else:
            print("Invalid choice")

    B.boat_coords = B.place_boats()

    bot_won = False
    player_won = False
    boat_hit = ""
    
    turn = random.randint(0,1)
    starter = turn
    player_message = f'{players[turn]} is starting !'
    bot_message = f"{bot_name} is your opponent this game !"
    bot_tries = 0

    while not bot_won and not player_won :

        if turn == starter :
            show_grids (boat_grid= P.grid, attack_grid= B.grid, coords= coord_list, score= P.score, player_message= player_message, bot_message= bot_message)

        if turn == 0 :
            x = input("Enter the row to attack (A-J) : ")
            y = input("Enter the column to attack (1-10) : ")
            # Check if input is valid
            if (x.upper().strip() in coord_list) & (y.isnumeric()) :
                if 1<=int(y)<=10 :
                    boat_hit, sunk, P.score = P.register_attack(x= x, y= int(y), boat_coord= B.boat_coords, attack_grid= B.grid, score= P.score, coord_list= coord_list, player= True)
                    if sunk :
                        player_message = f'You sunk {boat_names[boat_hit][0]} !'
                        P.boats_left -= 1
                        if P.boats_left == 0 :
                            player_won = True
                    elif (boat_hit != "Miss") & (boat_hit != "Fail") :
                       player_message = "Hit !"
                    elif boat_hit == "Miss" :
                        player_message = 'Miss !'
                    elif (boat_hit == "Fail") :
                        player_message = "You already tried here... Try again !"
                else : 
                    boat_hit = "Fail"
                    player_message = "Invalid coordinates... Try again !"
            else : 
                boat_hit = "Fail"
                player_message = "Invalid coordinates... Try again !"

        elif turn == 1 :
            boat_hit, sunk = B.attack(grid= P.grid, boat_coord= P.boat_coords)
            bot_tries += 1
            if sunk :
                bot_message = f"{bot_name} sunk {boat_names[boat_hit][0]}"
                B.boats_left -= 1
                if B.boats_left == 0 :
                    bot_won = True
            elif (boat_hit != "Miss") & (boat_hit != "Fail") :
                bot_message = f"{bot_name} hit {boat_names[boat_hit][0]}"
            elif boat_hit == "Miss" :
                bot_message = f'{bot_name} missed !'
            elif (boat_hit == "Fail") :
                bot_message = f"{bot_name} entered invalid coordinates"

            if bot_tries >= 100 :
                raise BotLoopError ("Bot exceeded 100 failed attempts")
                
        if boat_hit != "Fail" :
            bot_tries = 0
            turn = (turn + 1) % 2
    
    show_grids (boat_grid= P.grid, attack_grid= B.grid, coords= coord_list, score= P.score, player_message= player_message, bot_message= bot_message)

    ascii_art(player_won= player_won)

    if scoreboard_path and player_won :
        update_scoreboard(username= P.name, score= P.score, path= scoreboard_path)


if __name__ == "__main__" :
    try :
        play = True
        while play :
            main()
            play_again = input("Do you want to play again ? (Y/N)\n")
            if play_again.upper().strip() == "N" :
                play = False
    except Exception as e :
        print(f"An error has occured : {e}")
        print("Please check you satisfy all requirements to launch the game")
