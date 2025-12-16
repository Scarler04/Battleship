import pygame,sys
from grid import Grid


pygame.init()
SCREEN = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

grid = Grid()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill((0, 0, 0))     # fond noir
    grid.draw(SCREEN, 50, 50) # dessine la grille
    pygame.display.update()
    clock.tick(60)

pygame.quit()
