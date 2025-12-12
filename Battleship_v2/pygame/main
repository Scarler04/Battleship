import pygame, sys
from button import Button
from boutontranspa import TransparentButton
from PIL import Image
from username import get_user_name
import pygame_gui

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

        SCREEN.blit(frames[0], (0, 0))

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.check_for_input(mouse_pos):
                    return player_name, "Easy"
                if hard_button.check_for_input(mouse_pos):
                    return player_name, "Hard"

        pygame.display.update()
        clock.tick(10)


def play(player_name, difficulty):
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.blit(frames[0], (0, 0))

        info_text = get_font(40).render(
            f"Player: {player_name.upper()}   Difficulty: {difficulty.upper()}",
            True, (255, 255, 255)
        )
        SCREEN.blit(info_text, (30, 30))

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
