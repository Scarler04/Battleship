import pygame, sys
from button import Button
from boutontranspa import TransparentButton
from PIL import Image
from username import get_user_name
import pygame_gui

from colors import Colors
from position import Position
from grid import Grid
import random


pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Tobu  Candyland.mp3")
pygame.mixer.music.play(-1)
water_sound = pygame.mixer.Sound("water-splash-199583.mp3")
explosion_sound = pygame.mixer.Sound("large-underwater-explosion-sfx-450455.mp3")



SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
MANAGER = pygame_gui.UIManager(SCREEN.get_size())
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
clock = pygame.time.Clock()
score_image = pygame.image.load("Designer (1).png")
score_image = pygame.transform.scale(score_image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT))


# Charger GIF   #Vu sur internet
gif = Image.open("ocean waves GIF by weinventyou.gif")
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
menu_image = pygame.image.load("Copilot_20251128_101845-removebg-preview.png")
menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

def place_enemy_ships(enemy_grid, ships_info):
    for ship in ships_info:
        placed = False
        while not placed:
            row = random.randint(0, enemy_grid.num_rows - 1)
            col = random.randint(0, enemy_grid.num_cols - 1)
            orientation = random.choice(["H", "V"])
            placed = enemy_grid.place_ship(
                row, col,
                ship["size"],
                orientation,
                ship["id"]
            )

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
                                place_enemy_ships(enemy_grid, ships_info)

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


        texts = [
            ("Eau", Colors.water),
            ("Bateau 1", Colors.green),
            ("Bateau 2", Colors.orange),
            ("Bateau 3", Colors.purple),
            ("Bateau 4", Colors.cyan),
            ("Bateau 5", Colors.blue),
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
                "Press any key or click to return to menu",
                True, (255, 255, 255)
            )
            SCREEN.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2,
                            SCREEN_HEIGHT // 2 + 100))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return 


        pygame.display.update()
        clock.tick(60)

def score():
    while True:
        mouse_pos = pygame.mouse.get_pos()

        for frame in frames:
            SCREEN.blit(frame, (0, 0))
        img_width = int(SCREEN_WIDTH * 0.6)
        img_height = int(SCREEN_HEIGHT * 0.6)

        center_image = pygame.transform.scale(score_image, (img_width, img_height))
        x = (SCREEN_WIDTH - img_width) // 2
        y = (SCREEN_HEIGHT - img_height) // 2

        SCREEN.blit(center_image, (x, y))

        back_button = Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80),
                             "BACK", get_font(30), "white", "red")
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(mouse_pos):
                    return

        pygame.display.update()
        clock.tick(10)

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

        pygame.display.update()
        clock.tick(10)

main_menu()
