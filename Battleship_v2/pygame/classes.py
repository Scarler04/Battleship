import pygame
class TransparentButton:
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input

        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

        screen.blit(self.text, self.rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position) 
class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color, width=700, height=80):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.width = width
        self.height = height

        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.x_pos, self.y_pos)

    def update(self, screen):
        # couleur du fond 
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = self.hovering_color
        else:
            color = (50, 50, 50)  # gris foncé pour fond
        pygame.draw.rect(screen, color, self.rect, border_radius=12)  # rectangle arrondi
        pygame.draw.rect(screen, self.base_color, self.rect, width=4, border_radius=12)  # bordure
        # texte
        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

