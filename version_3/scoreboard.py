import pygame
import csv
from pathlib import Path

# Couleurs style naval/métallique
RUST_ORANGE = (184, 115, 51)
RUST_RED = (139, 69, 19)
METAL_GRAY = (105, 105, 105)
DARK_METAL = (45, 52, 54)
WHITE = (220, 220, 220)
DARK_GRAY = (80, 90, 100)
HIGHLIGHT = (255, 140, 0)
GOLD_METAL = (218, 165, 32)

def load_scores(csv_path):
    """Charge les scores depuis le CSV et les trie (ordre croissant = meilleur)"""
    scores = []
    if not Path(csv_path).exists():
        return []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                scores.append({
                    'username': row['Username'],
                    'score': int(row['Score'])
                })
    except Exception as e:
        print(f"Erreur chargement scores: {e}")
        return []
    
    scores.sort(key=lambda x: x['score'])
    return scores

def save_score(csv_path, username, score):
    """Ajoute un nouveau score au CSV"""
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    
    file_exists = Path(csv_path).exists()
    
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Username', 'Score'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Username': username, 'Score': score})

def draw_metal_panel(screen, rect):
    """Dessine un panneau métallique avec effet rouillé"""
    pygame.draw.rect(screen, DARK_METAL, rect, border_radius=8)
    pygame.draw.rect(screen, RUST_ORANGE, rect, 3, border_radius=8)
    
    rivet_positions = [
        (rect.left + 15, rect.top + 15),
        (rect.right - 15, rect.top + 15),
        (rect.left + 15, rect.bottom - 15),
        (rect.right - 15, rect.bottom - 15)
    ]
    for pos in rivet_positions:
        pygame.draw.circle(screen, METAL_GRAY, pos, 5)
        pygame.draw.circle(screen, RUST_RED, pos, 5, 1)

def draw_podium_entry(screen, rank, username, score, y_pos, is_new=False, get_font=None):
    """Dessine une entrée du scoreboard"""
    if rank == 1:
        color = GOLD_METAL
        rank_symbol = "#1"
    elif rank == 2:
        color = METAL_GRAY
        rank_symbol = "#2"
    elif rank == 3:
        color = RUST_ORANGE
        rank_symbol = "#3"
    else:
        color = DARK_GRAY
        rank_symbol = f"#{rank}"
    
    card_rect = pygame.Rect(150, y_pos, 500, 70)
    if is_new:
        pygame.draw.rect(screen, HIGHLIGHT, card_rect, border_radius=8)
        draw_metal_panel(screen, card_rect)
        pygame.draw.rect(screen, HIGHLIGHT, card_rect, 4, border_radius=8)
    else:
        draw_metal_panel(screen, card_rect)
    
    font_large = get_font(48) if get_font else pygame.font.Font(None, 48)
    font_medium = get_font(36) if get_font else pygame.font.Font(None, 36)
    
    rank_text = font_large.render(rank_symbol, True, color)
    screen.blit(rank_text, (170, y_pos + 15))
    
    username_text = font_medium.render(username, True, WHITE)
    screen.blit(username_text, (290, y_pos + 20))
    
    score_text = font_large.render(str(score), True, color)
    score_rect = score_text.get_rect(right=620, centery=y_pos + 35)
    screen.blit(score_text, score_rect)

def draw_dots(screen, y_pos):
    """Dessine les petits points de séparation"""
    for i in range(3):
        pygame.draw.circle(screen, RUST_ORANGE, (400, y_pos + i * 15), 4)


def show_game_over_scoreboard(screen, get_font, frames, username, score, csv_path="ressources/scoreboard_battleship.csv"):
    """
    Affiche le scoreboard après la partie avec le nouveau score en évidence
    """
    # Sauvegarder le score
    save_score(csv_path, username, score)
    
    # Charger tous les scores
    scores = load_scores(csv_path)
    
    # Trouver la position du nouveau score
    new_entry = {'username': username, 'score': score}
    new_rank = next((i + 1 for i, s in enumerate(scores) if s == new_entry or 
                     (s['username'] == username and s['score'] == score)), len(scores))
    
    is_podium = new_rank <= 3
    
    clock = pygame.time.Clock()
    running = True
    frame_index = 0
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        
        # Fond GIF
        screen.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % len(frames)
        
        # Titre
        title = get_font(72).render("SCOREBOARD", True, RUST_ORANGE)
        title_rect = title.get_rect(center=(screen.get_width() // 2, 60))
        screen.blit(title, title_rect)
        
        # Ligne décorative
        pygame.draw.line(screen, RUST_ORANGE, (200, 120), (screen.get_width() - 200, 120), 4)
        pygame.draw.line(screen, RUST_RED, (200, 125), (screen.get_width() - 200, 125), 2)
        
        y_offset = 180
        
        if is_podium:
            for i in range(min(3, len(scores))):
                entry = scores[i]
                is_new = (entry['username'] == username and entry['score'] == score and i + 1 == new_rank)
                draw_podium_entry(screen, i + 1, entry['username'], 
                                entry['score'], y_offset, is_new, get_font)
                y_offset += 90
        else:
            for i in range(min(3, len(scores))):
                entry = scores[i]
                draw_podium_entry(screen, i + 1, entry['username'], 
                                entry['score'], y_offset, False, get_font)
                y_offset += 90
            
            y_offset += 20
            draw_dots(screen, y_offset)
            y_offset += 60
            
            draw_podium_entry(screen, new_rank, username, 
                            score, y_offset, True, get_font)
        
        # Instructions
        info_text = get_font(30).render("Press any key to return to menu", True, WHITE)
        info_rect = info_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 30))
        screen.blit(info_text, info_rect)
        
        pygame.display.update()
        clock.tick(10)


def show_full_scoreboard(screen, get_font, frames, csv_path="ressources/scoreboard_battleship.csv"):
    """
    Affiche le scoreboard complet accessible depuis le menu principal
    Avec scrolling pour voir tous les scores
    """
    scores = load_scores(csv_path)
    
    clock = pygame.time.Clock()
    running = True
    frame_index = 0
    scroll_offset = 0
    max_visible = 10
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            
            # Scrolling avec molette
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * 30
                scroll_offset = max(0, min(scroll_offset, max(0, (len(scores) - max_visible) * 80)))
            
            # Scrolling avec flèches
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + 80, max(0, (len(scores) - max_visible) * 80))
                elif event.key == pygame.K_UP:
                    scroll_offset = max(0, scroll_offset - 80)
                elif event.key == pygame.K_ESCAPE:
                    running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check bouton back
                back_button_rect = pygame.Rect(screen.get_width() // 2 - 100, 
                                              screen.get_height() - 80, 200, 50)
                if back_button_rect.collidepoint(mouse_pos):
                    running = False
        
        # Fond GIF
        screen.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % len(frames)
        
        # Titre
        title = get_font(72).render("FULL SCOREBOARD", True, RUST_ORANGE)
        title_rect = title.get_rect(center=(screen.get_width() // 2, 60))
        screen.blit(title, title_rect)
        
        # Ligne décorative
        pygame.draw.line(screen, RUST_ORANGE, (150, 120), (screen.get_width() - 150, 120), 4)
        
        # Zone de scoreboard avec clipping
        scoreboard_rect = pygame.Rect(100, 150, screen.get_width() - 200, 
                                      screen.get_height() - 250)
        
        # Créer surface pour scrolling
        scroll_surface = pygame.Surface((scoreboard_rect.width, 
                                        max(scoreboard_rect.height, len(scores) * 80)))
        scroll_surface.fill((0, 0, 0, 0))
        scroll_surface.set_colorkey((0, 0, 0))
        
        # Dessiner toutes les entrées
        y_pos = 0
        for i, entry in enumerate(scores):
            if i < 20:  # Limiter affichage pour performance
                temp_rect = pygame.Rect(50, y_pos, 500, 70)
                
                # Couleur selon rang
                if i < 3:
                    colors = [GOLD_METAL, METAL_GRAY, RUST_ORANGE]
                    color = colors[i]
                else:
                    color = DARK_GRAY
                
                # Panneau
                draw_metal_panel(scroll_surface, temp_rect)
                
                # Rank
                rank_text = get_font(40).render(f"#{i+1}", True, color)
                scroll_surface.blit(rank_text, (70, y_pos + 18))
                
                # Username
                username_text = get_font(32).render(entry['username'], True, WHITE)
                scroll_surface.blit(username_text, (180, y_pos + 22))
                
                # Score
                score_text = get_font(40).render(str(entry['score']), True, color)
                score_rect = score_text.get_rect(right=520, centery=y_pos + 35)
                scroll_surface.blit(score_text, score_rect)
            
            y_pos += 80
        
        # Afficher la partie visible
        screen.blit(scroll_surface, scoreboard_rect.topleft, 
                   pygame.Rect(0, scroll_offset, scoreboard_rect.width, scoreboard_rect.height))
        
        # Indicateur de scroll
        if len(scores) > max_visible:
            # Barre de scroll
            scroll_bar_height = max(30, scoreboard_rect.height * max_visible / len(scores))
            scroll_bar_y = scoreboard_rect.top + (scroll_offset / ((len(scores) - max_visible) * 80)) * \
                          (scoreboard_rect.height - scroll_bar_height)
            
            pygame.draw.rect(screen, DARK_GRAY, 
                           (screen.get_width() - 120, scoreboard_rect.top, 
                            20, scoreboard_rect.height), border_radius=10)
            pygame.draw.rect(screen, RUST_ORANGE,
                           (screen.get_width() - 120, scroll_bar_y, 
                            20, scroll_bar_height), border_radius=10)
        
        # Bouton Back
        back_button_rect = pygame.Rect(screen.get_width() // 2 - 100, 
                                       screen.get_height() - 80, 200, 50)
        
        # Effet hover
        if back_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, RUST_ORANGE, back_button_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, DARK_METAL, back_button_rect, border_radius=10)
        
        pygame.draw.rect(screen, RUST_ORANGE, back_button_rect, 3, border_radius=10)
        
        back_text = get_font(30).render("BACK", True, WHITE)
        back_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_rect)
        
        # Instructions
        if len(scores) > max_visible:
            info = get_font(24).render("Use mouse wheel or arrows to scroll", True, DARK_GRAY)
            screen.blit(info, (screen.get_width() // 2 - info.get_width() // 2, 
                              screen.get_height() - 110))
        
        pygame.display.update()
        clock.tick(60)