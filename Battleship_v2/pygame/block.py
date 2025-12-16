from colors import Colors
from position import Position
import pygame

class Block:
    def __init__(self, id, positions, cell_size=30):
        self.id = id
        self.cells = [Position(r,c) for r,c in positions]
        self.cell_size = cell_size
        self.colors = Colors.get_cell_colors()
    
    def draw(self, screen):
        for pos in self.cells:
            rect = pygame.Rect(pos.column*self.cell_size, pos.row*self.cell_size, self.cell_size-1, self.cell_size-1)
            pygame.draw.rect(screen, self.colors[self.id], rect)
