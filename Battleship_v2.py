# def place_boats():  
#     """
#     Generates random boat coordinates
    
#     Returns:
#         dict:
#             A dictionnary with boat names as keys and lists of boat coordinates as tuples of two integers as items
#     """
#     bateaux = {"P":5,"C":4,"S":3,"T":2,"B":1}       # Dictionary of boat lengths
#     dict_bateau = {}                                
#     case_occupe = []
#     for symbole,taille in bateaux.items():          # Browse the dictionary that we introduce at the begining
#         invalid = False                             # Booleen to see if we can put the boat or no (if the boat exceeds the grid or if the boat overlap another boat )
#         while invalid==False:    
#             ligne = random.randint(0,9)             # Stock the random coordonate in the variable "ligne" and the variable "colonne"
#             colonne = random.randint(0,9)
#             orientation = random.choice(["H","V"])  # Choose boat direction (H : horizontal, V : vertical)
#             pos = []
#             if orientation=="H":
#                 if colonne+taille<=10:              # Check if the boat fits on the grid using generated coordinates and direction
#                     for i in range(taille):
#                         p = (ligne,colonne+i)        
#                         pos.append(p)
#                                                      # List of boat's coordinates
#                 else:
#                     col = colonne-taille 
#                     for i in range(taille):
#                         p = (ligne,col+i)
#                         pos.append(p)                                                   #if the boat don't fits on the grid
                                           
#             else:                                    # Same for vertical
#                 if ligne+taille<=10:
#                     for i in range(taille):
#                         p = (ligne+i,colonne)
#                         pos.append(p)
#                 else:
#                     li = ligne-taille
#                     for i in range(taille):
#                         p = (li+i,colonne)
#                         pos.append(p)

#             if pos!=[]:
#                 chevauchement = False
#                 for k in pos:
#                     if k in case_occupe:
#                         chevauchement=True
#                 if chevauchement==False:
#                     dict_bateau[symbole] = pos 
#                     for x in pos:
#                         case_occupe.append(x)       # We add the coordinates in the list to make sure that we have no duplicates
#                     invalid=True
#     return dict_bateau


# print(place_boats())

