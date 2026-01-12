import pygame
import pygame_gui

def settings_menu(SCREEN, MANAGER, SCREEN_WIDTH, SCREEN_HEIGHT, get_font, frames, 
                  water_sound=None, explosion_sound=None):
    """
    Menu de paramètres avec sliders de volume et bouton shutdown
    """
    clock = pygame.time.Clock()
    
    popup_width = 600
    popup_height = 600  # Augmenté pour le bouton shutdown
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2
    
    # Slider volume musique
    music_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((popup_x + 200, popup_y + 120), (300, 30)),
        start_value=pygame.mixer.music.get_volume() * 100,
        value_range=(0, 100),
        manager=MANAGER
    )
    
    # Slider volume effets sonores
    effects_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((popup_x + 200, popup_y + 220), (300, 30)),
        start_value=100,
        value_range=(0, 100),
        manager=MANAGER
    )
    
    language_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=['Français', 'English'],
        starting_option='Français',
        relative_rect=pygame.Rect((popup_x + 200, popup_y + 320), (300, 40)),
        manager=MANAGER
    )
    
    # Bouton Close
    close_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((popup_x + popup_width // 2 - 150, popup_y + popup_height - 70), (120, 50)),
        text='CLOSE',
        manager=MANAGER
    )
    
    # Bouton Shutdown
    shutdown_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((popup_x + popup_width // 2 + 30, popup_y + popup_height - 70), (120, 50)),
        text='QUIT',
        manager=MANAGER
    )
    
    # Variables pour confirmation
    confirmation_dialog = None
    
    running = True
    frame_index = 0
    
    while running:
        time_delta = clock.tick(60) / 1000.0
        
        SCREEN.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % len(frames)
        
        # Overlay semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        SCREEN.blit(overlay, (0, 0))
        
        # Popup
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((50, 50, 60))
        pygame.draw.rect(popup_surface, (100, 200, 255), (0, 0, popup_width, popup_height), 5, border_radius=15)
        
        shadow = pygame.Surface((popup_width + 10, popup_height + 10), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 100))
        SCREEN.blit(shadow, (popup_x + 5, popup_y + 5))
        SCREEN.blit(popup_surface, (popup_x, popup_y))
        
        # Titre
        title_font = get_font(50)
        title_text = title_font.render("SETTINGS", True, (255, 255, 255))
        title_x = popup_x + (popup_width - title_text.get_width()) // 2
        SCREEN.blit(title_text, (title_x, popup_y + 30))
        
        # Légende "Music Volume"
        music_font = get_font(30)
        music_text = music_font.render("Music:", True, (255, 255, 255))
        SCREEN.blit(music_text, (popup_x + 50, popup_y + 120))
        
        music_value = int(music_slider.get_current_value())
        music_value_text = get_font(25).render(f"{music_value}%", True, (100, 200, 255))
        SCREEN.blit(music_value_text, (popup_x + 520, popup_y + 122))
        
        # Légende "Effects Volume"
        effects_font = get_font(30)
        effects_text = effects_font.render("Effects:", True, (255, 255, 255))
        SCREEN.blit(effects_text, (popup_x + 50, popup_y + 220))
        
        effects_value = int(effects_slider.get_current_value())
        effects_value_text = get_font(25).render(f"{effects_value}%", True, (100, 200, 255))
        SCREEN.blit(effects_value_text, (popup_x + 520, popup_y + 222))
        
        # Légende "Language"
        language_font = get_font(30)
        language_text = language_font.render("Language:", True, (255, 255, 255))
        SCREEN.blit(language_text, (popup_x + 50, popup_y + 320))
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == close_button:
                    running = False
                
                elif event.ui_element == shutdown_button:
                    # Créer dialog de confirmation
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 75), (300, 150)),
                        manager=MANAGER,
                        window_title='Confirmation',
                        action_long_desc='Êtes-vous sûr de vouloir quitter le jeu ?',
                        action_short_name='OK',
                        blocking=True
                    )
            
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                # L'utilisateur a confirmé la fermeture
                pygame.quit()
                import sys
                sys.exit()
            
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == music_slider:
                    volume = music_slider.get_current_value() / 100
                    pygame.mixer.music.set_volume(volume)
                
                elif event.ui_element == effects_slider:
                    volume = effects_slider.get_current_value() / 100
                    if water_sound:
                        water_sound.set_volume(volume)
                    if explosion_sound:
                        explosion_sound.set_volume(volume)
            
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == language_dropdown:
                    selected_language = language_dropdown.selected_option
                    print(f"Langue sélectionnée: {selected_language}")
            
            MANAGER.process_events(event)
        
        MANAGER.update(time_delta)
        MANAGER.draw_ui(SCREEN)
        
        pygame.display.update()
    
    # Nettoyer
    music_slider.kill()
    effects_slider.kill()
    language_dropdown.kill()
    close_button.kill()
    shutdown_button.kill()