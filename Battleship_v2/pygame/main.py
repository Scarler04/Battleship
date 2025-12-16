import pygame, sys
from button import Button
from boutontranspa import TransparentButton
from PIL import Image
from username import get_user_name
import pygame_gui

from colors import Colors
from position import Position
from grid import Grid

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Tobu  Candyland.mp3")
pygame.mixer.music.play(-1)



SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
MANAGER = pygame_gui.UIManager(SCREEN.get_size())
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
clock = pygame.time.Clock()
score_image = pygame.image.load("Designer (1).png")
score_image = pygame.transform.scale(score_image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT))


# Charger GIF
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

            if event.type == pygame.MOUSEBUTTONDOWN:       #ça veut dire que l'utilisateur à cliquer
                if easy_button.check_for_input(mouse_pos):
                    return player_name, "Easy"
                if hard_button.check_for_input(mouse_pos):
                    return player_name, "Hard"

        pygame.display.update()
        clock.tick(10)
import random

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

def bot_attack(player_grid, bot_shots):
    while True:
        row = random.randint(0, player_grid.num_rows - 1)
        col = random.randint(0, player_grid.num_cols - 1)

        if (row, col) not in bot_shots:
            bot_shots.add((row, col))
            result = player_grid.hit_cell(row, col)
            print(f"Tir bot ({row},{col}) : {result}")
            break



def play(player_name, difficulty):
    player_grid = Grid()
    enemy_grid = Grid()

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
    bot_shots = set()   # mémorise les cases déjà tirées par l'ordi


    ships_info = [
        {"id": 1, "size": 5, "orientation": "H"},
        {"id": 2, "size": 4, "orientation": "V"},
        {"id": 3, "size": 3, "orientation": "H"},
        {"id": 4, "size": 2, "orientation": "V"},
        {"id": 5, "size": 1, "orientation": "H"}
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(frames[0], (0, 0))

        info_text = get_font(40).render(
            f"Player: {player_name.upper()}   Difficulty: {difficulty.upper()}",
            True, (255, 255, 255)
        )
        SCREEN.blit(info_text, (30, 30))

        # === TITRES DES GRILLES ===
        title_font = get_font(30)
        SCREEN.blit(title_font.render("YOUR GRID", True, (255, 255, 255)),
                    (player_offset_x, offset_y - 40))
        SCREEN.blit(title_font.render("ENEMY GRID", True, (255, 255, 255)),
                    (enemy_offset_x, offset_y - 40))

        # === BOUTON BACK ===
        back_button = Button(
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80),
            "BACK", get_font(30), "white", "red"
        )
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if back_button.check_for_input(mouse_pos):
                    return

                # --- GRILLE JOUEUR ---
                row = (y - offset_y) // player_grid.cell_size
                col = (x - player_offset_x) // player_grid.cell_size

                if 0 <= row < player_grid.num_rows and 0 <= col < player_grid.num_cols:
                    if placing_phase:
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
                                place_enemy_ships(enemy_grid, ships_info)
                                player_turn = True   
                                print("Tous les bateaux placés ! Combat lancé !")



                # --- GRILLE ENNEMIE ---
                # --- GRILLE ENNEMIE ---
                row_e = (y - offset_y) // enemy_grid.cell_size
                col_e = (x - enemy_offset_x) // enemy_grid.cell_size

                if 0 <= row_e < enemy_grid.num_rows and 0 <= col_e < enemy_grid.num_cols:
                    if not placing_phase and player_turn:
                        # le joueur tire sur la grille ennemie
                        result = enemy_grid.hit_cell(row_e, col_e)
                        print(f"Tir joueur ({row_e},{col_e}) : {result}")
                        player_turn = False  # ensuite c'est au bot
                if not player_turn and not placing_phase:
                    pygame.time.delay(500)
                    bot_attack(player_grid, bot_shots)
                    player_turn = True



            elif event.type == pygame.KEYDOWN:
                if placing_phase and event.key == pygame.K_r:
                    ship = ships_info[current_ship_index]
                    ship["orientation"] = "V" if ship["orientation"] == "H" else "H"

        player_grid.draw(SCREEN, player_offset_x, offset_y, hide_ships=False)
        enemy_grid.draw(SCREEN, enemy_offset_x, offset_y, hide_ships=True)


        # === LÉGENDE ===
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
