import pygame, sys
from button import Button
from bouton_transparent import TransparentButton
from PIL import Image
from username import get_user_name
from settings_menu import settings_menu
from scoreboard import show_game_over_scoreboard, show_full_scoreboard
import pygame_gui

from colors import Colors
from position import Position
from grid import Grid
import random
import numpy as np


pygame.init()
pygame.mixer.init()

# Variable globale pour le volume des effets sonores
SOUND_EFFECTS_VOLUME = 1.0  # Entre 0.0 et 1.0

def set_sound_effects_volume(volume):
    """Met à jour le volume de tous les sound effects"""
    global SOUND_EFFECTS_VOLUME
    SOUND_EFFECTS_VOLUME = volume
    water_sound.set_volume(volume)
    explosion_sound.set_volume(volume)

pygame.mixer.music.load("ressources/Tobu_Candyland.mp3")
pygame.mixer.music.play(-1)
water_sound = pygame.mixer.Sound("ressources/water-splash.mp3")
explosion_sound = pygame.mixer.Sound("ressources/large-underwater-explosion-sfx.mp3")



SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
MANAGER = pygame_gui.UIManager(SCREEN.get_size())
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
clock = pygame.time.Clock()

# Charger GIF   #Vu sur internet
gif = Image.open("ressources/ocean waves GIF by weinventyou.gif")
frames = []

try:
    while True:
        frame = gif.copy().convert("RGBA")
        frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frames.append(frame)
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

# Image par-dessus GIF
menu_image = pygame.image.load("ressources/Logo.png")
menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_settings_button(SCREEN, mouse_pos, get_font):
    """Dessine et gère le bouton settings universel"""
    from bouton_transparent import TransparentButton
    
    settings_font = get_font(30)
    setting_button = TransparentButton((SCREEN.get_width() - 100, 50),
                                       "SETTINGS", settings_font,
                                       (255, 255, 255), (255, 0, 0))
    setting_button.update(SCREEN)
    
    return setting_button

def get_font(size):
    return pygame.font.SysFont("Arial", size)


def choose_difficulty():

    player_name = get_user_name(SCREEN, MANAGER)
    choosing = True
    
    while choosing:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.blit(frames[0], (0, 0))   #blit c'est pour dessiner

        title = get_font(70).render("Choose Difficulty", True, (255, 255, 255))
        SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        easy_button = Button((SCREEN_WIDTH // 2, 300), "EASY",
                             get_font(60), "white", "green")
        hard_button = Button((SCREEN_WIDTH // 2, 450), "HARD",
                             get_font(60), "white", "red")

        easy_button.update(SCREEN)
        hard_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:       #ça veut dire que l'utilisateur a cliqué
                if easy_button.check_for_input(mouse_pos):
                    return player_name, "Easy"
                if hard_button.check_for_input(mouse_pos):
                    return player_name, "Hard"

        pygame.display.update()
        clock.tick(10)

def calculer_poids_uniformite_pygame(case_occupe, weights_base=None):
    """Calcule poids pour distribution uniforme avec weights_base optionnel"""
    grille_densite = np.zeros((10, 10))
    
    for ligne, colonne in case_occupe:
        for dl in range(-2, 3):
            for dc in range(-2, 3):
                nl, nc = ligne + dl, colonne + dc
                if 0 <= nl < 10 and 0 <= nc < 10:
                    distance = max(abs(dl), abs(dc))
                    grille_densite[nl, nc] += 1.0 / (distance + 1)
    
    poids = 1.0 / (grille_densite + 1.0)
    
    # Combiner avec weights_base si fourni
    if weights_base is not None:
        poids = poids * weights_base
    
    poids = poids / poids.sum()
    
    return poids


def random_func_pygame(weights=None):
    """Génère coordonnées aléatoires avec poids optionnels"""
    if weights is None:
        return random.randint(0, 9), random.randint(0, 9)
    else:
        flat_weights = weights.flatten()
        flat_weights = flat_weights / flat_weights.sum()
        cell_idx = np.random.choice(100, p=flat_weights)
        ligne = cell_idx // 10
        colonne = cell_idx % 10
        return ligne, colonne


def tenter_placement_pygame(ligne, colonne, taille, orientation, enemy_grid):
    """
    Tente placement et retourne les positions si valide
    Vérifie que c'est dans la grille et pas de chevauchement
    """
    positions = []
    
    if orientation == "H":
        if colonne + taille <= 10:
            for i in range(taille):
                r, c = ligne, colonne + i
                if enemy_grid.grid[r][c] != 0:
                    return []
                positions.append((r, c))
        elif colonne - taille + 1 >= 0:
            for i in range(taille):
                r, c = ligne, colonne - i
                if enemy_grid.grid[r][c] != 0:
                    return []
                positions.append((r, c))
    else:
        if ligne + taille <= 10:
            for i in range(taille):
                r, c = ligne + i, colonne
                if enemy_grid.grid[r][c] != 0:
                    return []
                positions.append((r, c))
        elif ligne - taille + 1 >= 0:
            for i in range(taille):
                r, c = ligne - i, colonne
                if enemy_grid.grid[r][c] != 0:
                    return []
                positions.append((r, c))
    
    return positions

def place_enemy_ships(enemy_grid, ships_info, weight_map=None):
    """
    Place enemy ships avec distribution uniforme
    
    Parameters
    ----------
        enemy_grid : Grid
            La grille ennemie où placer les bateaux
        ships_info : list
            Liste de dictionnaires avec "size" et "id" pour chaque bateau
        weight_map : array, optional
            Matrice 10x10 de poids pour biaiser le placement initial
            Si None, utilise placement uniforme pur
    """
    case_occupe = []
    
    for ship in ships_info:
        placed = False
        tentatives = 0
        max_tentatives = 1000
        
        while not placed and tentatives < max_tentatives:
            tentatives += 1
            
            # Calculer poids dynamiques combinés avec weight_map
            weights = calculer_poids_uniformite_pygame(case_occupe, weight_map)
            
            # Générer position avec poids
            row, col = random_func_pygame(weights)
            orientation = random.choice(["H", "V"])
            
            # Tenter placement
            positions = tenter_placement_pygame(row, col, ship["size"], orientation, enemy_grid)
            
            # Si échec, essayer autre orientation
            if not positions:
                orientation_alt = "V" if orientation == "H" else "H"
                positions = tenter_placement_pygame(row, col, ship["size"], orientation_alt, enemy_grid)
            
            # Si positions valides, placer le bateau
            if positions:
                placed = enemy_grid.place_ship(
                    positions[0][0], 
                    positions[0][1],
                    ship["size"],
                    orientation if len(positions) == ship["size"] else orientation_alt,
                    ship["id"]
                )
                
                if placed:
                    case_occupe.extend(positions)
        
        # Fallback: placement forcé si max_tentatives atteint
        if not placed:
            for r in range(10):
                for c in range(10):
                    for ori in ["H", "V"]:
                        positions = tenter_placement_pygame(r, c, ship["size"], ori, enemy_grid)
                        if positions:
                            placed = enemy_grid.place_ship(r, c, ship["size"], ori, ship["id"])
                            if placed:
                                case_occupe.extend(positions)
                                break
                    if placed:
                        break
                if placed:
                    break

def load_weight_map(filepath=None):
    """
    Charge ou génère une weight_map
    
    Parameters
    ----------
        filepath : str, optional
            Chemin vers fichier .npy contenant la weight_map
            Si None, retourne None (placement uniforme pur)
    
    Returns
    -------
        array or None: Matrice 10x10 de poids ou None
    """
    if filepath is None:
        return None
    
    try:
        weight_map = np.load(filepath)
        if weight_map.shape != (10, 10):
            print(f"Warning: weight_map shape is {weight_map.shape}, expected (10, 10)")
            return None
        return weight_map
    except:
        print(f"Could not load weight_map from {filepath}")
        return None

def bot_attack_easy(player_grid, bot_shots):
    while True:
        row = random.randint(0, player_grid.num_rows - 1)
        col = random.randint(0, player_grid.num_cols - 1)

        if (row, col) not in bot_shots:
            bot_shots.add((row, col))
            result = player_grid.hit_cell(row, col)

            # SOUND EFFECTS
            if result not in ["already hit", "already miss"]:
                if result == "miss":
                    water_sound.play()
                elif result == "hit" or result.startswith("sunk_"):
                    explosion_sound.play()

            return result
def bot_attack_hard(player_grid, bot_shots, bot_targets):    
    if bot_targets:
        row, col = bot_targets.pop(0)

        if (row, col) in bot_shots:
            return "already hit"

    else:
        while True:
            row = random.randint(0, player_grid.num_rows - 1)
            col = random.randint(0, player_grid.num_cols - 1)
            if (row, col) not in bot_shots:
                break

    bot_shots.add((row, col))
    result = player_grid.hit_cell(row, col)

    if result == "hit":
        for x, y in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + x, col + y
            if 0 <= r < player_grid.num_rows and 0 <= c < player_grid.num_cols:
                if (r, c) not in bot_shots:
                    bot_targets.append((r, c))

    if result not in ["already hit", "already miss"]:
        if result == "miss":
            water_sound.play()
        else:
            explosion_sound.play()

    return result



def play(player_name, difficulty):
    player_grid = Grid()
    enemy_grid = Grid()
    bot_targets = []   # mémoire du bot HARD


    grid_width = player_grid.num_cols * player_grid.cell_size
    grid_height = player_grid.num_rows * player_grid.cell_size

    gap = 80
    total_width = grid_width * 2 + gap

    start_x = (SCREEN_WIDTH - total_width) // 2
    offset_y = (SCREEN_HEIGHT - grid_height) // 2

    player_offset_x = start_x
    enemy_offset_x = start_x + grid_width + gap

    placing_phase = True
    current_ship_index = 0
    player_turn = False

    bot_shots = set()
    player_shots = 0
    bot_shots_count = 0

    game_over = False
    result_text = ""

    last_message = ""
    message_timer = 0

    weightmap = load_weight_map("ressources/weightmap_boats.npy")

    ship_names = {
        "1": "Le Porte-avion",
        "2": "Le Croiseur",
        "3": "Le Sous-marin",
        "4": "Le Torpilleur",
        "5": "La Barque"
    }

    ships_info = [
        {"id": 1, "size": 5, "orientation": "H"},
        {"id": 2, "size": 4, "orientation": "V"},
        {"id": 3, "size": 3, "orientation": "H"},
        {"id": 4, "size": 2, "orientation": "V"},
        {"id": 5, "size": 1, "orientation": "H"}
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(frames[0], (0, 0))  # fond GIF

        # --- Affichage info ---
        info_text = get_font(40).render(
            f"Player: {player_name.upper()}   Difficulty: {difficulty.upper()}",
            True, (255, 255, 255)
        )
        SCREEN.blit(info_text, (30, 30))

        score_text = get_font(30).render(
            f"Player shots: {player_shots}   Bot shots: {bot_shots_count}",
            True, (255, 255, 255)
        )
        SCREEN.blit(score_text, (30, 80))

        if message_timer > 0:
            msg = get_font(30).render(last_message, True, (255, 200, 200))
            SCREEN.blit(msg, (30, 120))
            message_timer -= 1

        title_font = get_font(30)
        SCREEN.blit(title_font.render("YOUR GRID", True, (255, 255, 255)),
                    (player_offset_x, offset_y - 40))
        SCREEN.blit(title_font.render("ENEMY GRID", True, (255, 255, 255)),
                    (enemy_offset_x, offset_y - 40))

        # --- Événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Rotation bateau
            elif event.type == pygame.KEYDOWN:
                if placing_phase and event.key == pygame.K_r:
                    ship = ships_info[current_ship_index]
                    ship["orientation"] = "V" if ship["orientation"] == "H" else "H"

            # Clic souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if placing_phase:
                    # Placement bateau joueur
                    row = (y - offset_y) // player_grid.cell_size
                    col = (x - player_offset_x) // player_grid.cell_size

                    if 0 <= row < player_grid.num_rows and 0 <= col < player_grid.num_cols:
                        ship = ships_info[current_ship_index]
                        success = player_grid.place_ship(
                            row, col,
                            ship["size"],
                            ship["orientation"],
                            ship["id"]
                        )
                        if success:
                            current_ship_index += 1
                            if current_ship_index >= len(ships_info):
                                placing_phase = False
                                player_turn = True
                                place_enemy_ships(enemy_grid, ships_info, weightmap)

                else:
                    # Tir sur grille ennemie
                    row_e = (y - offset_y) // enemy_grid.cell_size
                    col_e = (x - enemy_offset_x) // enemy_grid.cell_size

                    if 0 <= row_e < enemy_grid.num_rows and 0 <= col_e < enemy_grid.num_cols:
                        if player_turn:
                            result = enemy_grid.hit_cell(row_e, col_e)

                            # Sound effects
                            if result not in ["already hit", "already miss"]:
                                if result == "miss":
                                    water_sound.play()
                                else:
                                    explosion_sound.play()

                            if result not in ["already hit", "already miss"]:
                                player_shots += 1
                                player_turn = False

                            # Message bateau coulé
                            if result.startswith("sunk_"):
                                ship_id = result.split("_")[1]
                                last_message = f"Tu as coulé {ship_names[ship_id]}"
                                message_timer = 180

                            if enemy_grid.all_ships_sunk():
                                game_over = True
                                result_text = "WINNER"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if setting_button.check_for_input(mouse_pos):
                    settings_menu(SCREEN, MANAGER, SCREEN_WIDTH, SCREEN_HEIGHT, get_font, frames,
                                water_sound, explosion_sound)
                    continue  # Évite de traiter le clic comme un tir

        # Tour du bot
        if not placing_phase and not player_turn and not game_over:
            pygame.time.delay(500)
            if difficulty == "Easy":
                result = bot_attack_easy(player_grid, bot_shots)
            else:
                result = bot_attack_hard(player_grid, bot_shots, bot_targets)

            bot_shots_count += 1
            player_turn = True


            if result.startswith("sunk_"):
                ship_id = result.split("_")[1]
                last_message = f"L’ordinateur a coulé {ship_names[ship_id]}"
                message_timer = 180

            if player_grid.all_ships_sunk():
                game_over = True
                result_text = "LOSER"


        player_grid.draw(SCREEN, player_offset_x, offset_y, hide_ships=False)
        enemy_grid.draw(SCREEN, enemy_offset_x, offset_y, hide_ships=True)

        # Bouton settings pendant le jeu
        setting_button = draw_settings_button(SCREEN, mouse_pos, get_font)

        texts = [
            ("Eau", Colors.water),
            ("Porte-Avion", Colors.green),
            ("Croiseur", Colors.orange),
            ("Torpilleur", Colors.purple),
            ("Sous-marin", Colors.cyan),
            ("Barque", Colors.blue),
            ("Touché", Colors.red),
            ("Coulé", Colors.dark_red)
        ]

        legend_x = 50
        legend_height = len(texts) * 30
        legend_y_start = (SCREEN_HEIGHT - legend_height) // 2

        for i, (name, color) in enumerate(texts):
            y = legend_y_start + i * 30
            pygame.draw.rect(SCREEN, color, (legend_x, y, 20, 20))
            text = pygame.font.SysFont("Arial", 24).render(name, True, (255, 255, 255))
            SCREEN.blit(text, (legend_x + 30, y))

        if game_over:
            big_font = get_font(120)
            text = big_font.render(result_text, True, (255, 0, 0))
            SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                            SCREEN_HEIGHT // 2 - text.get_height() // 2))
            info = get_font(30).render(
                "Press any key to see scoreboard",
                True, (255, 255, 255)
            )
            SCREEN.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2,
                            SCREEN_HEIGHT // 2 + 100))
            
            pygame.display.update()
            
            # Attendre input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
            
            # Afficher scoreboard
            show_game_over_scoreboard(SCREEN, get_font, frames, player_name, player_shots)
            return


        pygame.display.update()
        clock.tick(60)

def score():
    show_full_scoreboard(SCREEN, get_font, frames)

def main_menu():
    frame_index = 0

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # GIF
        SCREEN.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % len(frames)

        # Image par-dessus
        SCREEN.blit(menu_image, (0, -110))

        # Boutons
        image_height = menu_image.get_height()
        spacing = 30
        settings_font = get_font(30)

        play_button = Button((SCREEN_WIDTH // 2, image_height + spacing - 300),
                             "PLAY", get_font(75), "white", "red")
        scoreboard_button = Button((SCREEN_WIDTH // 2, image_height + spacing + 100 - 300),
                                   "SCOREBOARD", get_font(75), "white", "red")
        quit_button = Button((SCREEN_WIDTH // 2, image_height + spacing + 200 - 300),
                             "QUIT", get_font(75), "white", "red")

        setting_button = TransparentButton((SCREEN_WIDTH - 100, 50),
                                           "SETTINGS", settings_font,
                                           (255, 255, 255), (255, 0, 0))

        for button in [play_button, scoreboard_button, quit_button, setting_button]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(mouse_pos):
                    player_name, difficulty = choose_difficulty()
                    play(player_name, difficulty)

                if scoreboard_button.check_for_input(mouse_pos):
                    score()

                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()

                if setting_button.check_for_input(mouse_pos):
                    settings_menu(SCREEN, MANAGER, SCREEN_WIDTH, SCREEN_HEIGHT, get_font, frames, water_sound, explosion_sound)

        pygame.display.update()
        clock.tick(10)

main_menu()