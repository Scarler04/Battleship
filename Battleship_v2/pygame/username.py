import pygame
import pygame_gui
import sys

def get_user_name(screen, manager):
    clock = pygame.time.Clock()
    
    width, height = screen.get_size()
    
    text_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((width//2 - 200, height//2), (400, 50)),
        manager=manager,
        object_id="#main_text_entry"
    )

    font = pygame.font.SysFont("bahnschrift", 40)
    label_text = font.render("Veuillez saisir votre prénom :", True, "black")
    label_rect = label_text.get_rect(center=(width//2, height//2 - 50))
    
    user_name = None
    while user_name is None:
        time_delta = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                user_name = event.text
            manager.process_events(event)

        manager.update(time_delta)
        screen.fill((255,255,255))
        screen.blit(label_text, label_rect)
        manager.draw_ui(screen)
        pygame.display.update()
    
    return user_name
