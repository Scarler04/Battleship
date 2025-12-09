import os
import csv


def find_file(filename : str, search_path = ".") :
    """
    Search for a file in a directory tree.

    This function walks through all subdirectories starting from
    `search_path` and returns the full path to `filename` as soon
    as it is found.

    Parameters
    ----------
        filename : str
            Name of the file to search for
        search_path : str, optional
            Directory path from which the search begins (default is current directory)

    Returns
    -------
        str or None
            Full path to the file if found, otherwise None
    """
    for root, dirs, files in os.walk(search_path) :
        if filename in files :
            return os.path.join(root, filename)
    return None


def find_directory (dirname : str, search_path = ".") :
    """
    Search for a folder in a directory tree
    
    Parameters
    -------
        dirname : str 
            Name of the folder to search for
        search_path : str, optional
            Directory path from which the search begins (default is current directory) 
        
    Returns
    -------
        str or None : Full path to the folder if found, otherwise None
    """
    for root, dirs, files in os.walk(search_path) :
        if dirname in dirs :
            return os.path.join(root, dirname)
    return None


def create_database () :
    """
    Find or create scoreboard data file

    Returns
    -------
        str : Full path to the file if found or created file, otherwise None.
    """
    path = find_file(filename= "scoreboard_battleship.csv")

    if path :
        return path    
    else :
        path = find_directory(dirname= "Battleship_v2")

        # Adding default scoreboard
        if path :
            path += "/scoreboard_battleship.csv"
            default_scores = [
                ["Username", "Score"],
                ["vanRossum", 60],
                ["Scarler", 50],
                ["36", 70]
            ]

            with open(path, "w", newline= "") as f :
                writer = csv.writer(f)
                writer.writerows(default_scores)

            return path 
        else :
            return path


def update_scoreboard (username : str, score : int, path : str) :
    """
    Update scoreboard data file after winning a game

    Parameters
    -------
        username : str
            Player username
        score : int
            Player score
        path : str
            Path to the scoreboard data file
    """
    with open(path, "a", newline= "\n") as f :
        writer = csv.writer(f)
        writer.writerow([username,score])


if __name__ == "__main__" :
    path = create_database()
    update_scoreboard("cici",50,path)
