from Database import create_database, update_scoreboard

if __name__ == "__main__" :

    # Scoreboard Init and upadte
    scoreboard_path = create_database()
    update_scoreboard("Test",50,scoreboard_path)

    pass