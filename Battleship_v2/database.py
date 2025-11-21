import os
import csv

def find_file(filename, search_path="."):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def find_directory(dirname, search_path="."):
    for root, dirs, files in os.walk(search_path):
        if dirname in dirs:
            return os.path.join(root, dirname)
    return None

def create_database () :
    path = find_file("scoreboard_battleship.csv")

    if path:
        return path
        
    else:
        path = find_directory("Battleship_v2")
        if path :
            path += "/scoreboard_battleship.csv"
            default_scores = [
                ["Username", "Score"],
                ["vanRossum", 25],
                ["Scarler", 35],
                ["36", 50]
            ]

            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(default_scores)

            return path 
        else :
            return path

def update_scoreboard (username : str, score : int, path : str) :
    with open(path,"a",newline="\n") as f:
        writer = csv.writer(f)
        writer.writerow([username,score])
    pass 

if __name__ == "__main__" :
    path = create_database()
    print(path)
