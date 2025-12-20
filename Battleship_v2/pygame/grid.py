import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 10
        self.num_cols = 10
        self.cell_size = 30 
        self.grid = [[0]*10 for _ in range(10)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in self.grid:
            print(" ".join(str(c) for c in row))
    def draw(self, screen, offset_x=0, offset_y=0, hide_ships=False):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                value = self.grid[row][col]

                # déterminer la couleur à dessiner
                if hide_ships and 1 <= value <= 5:
                    color = Colors.water  # cache les bateaux ennemis
                else:
                    color = self.colors[value]  # touche, coulé, eau ou tir raté

                rect = pygame.Rect(
                    col * self.cell_size + offset_x,
                    row * self.cell_size + offset_y,
                    self.cell_size - 1,
                    self.cell_size - 1
                )
                pygame.draw.rect(screen, color, rect)


    
    def place_ship(self, start_row, start_col, size, orientation, ship_id):
        positions = []
        for i in range(size):
            r = start_row + i if orientation == "V" else start_row
            c = start_col + i if orientation == "H" else start_col
            if r >= self.num_rows or c >= self.num_cols or self.grid[r][c] != 0:
                return False  
            positions.append((r,c))
        for r,c in positions:
            self.grid[r][c] = ship_id
        return True
    
    def hit_cell(self, row, col):
        value = self.grid[row][col]

        # --- Eau ---
        if value == 0:
            self.grid[row][col] = 30  # raté
            return "miss"

        # --- Bateau intact ---
        elif 1 <= value <= 5:
            ship_id = value
            self.grid[row][col] +=10

            for r in range(self.num_rows):
                for c in range(self.num_cols):
                    if self.grid[r][c] == ship_id:
                        return "hit"   

            for r in range(self.num_rows):
                for c in range(self.num_cols):
                    if self.grid[r][c] == ship_id + 10:
                        self.grid[r][c] += 10  

            return f"sunk_{ship_id}"

        elif value == 30:
            return "already miss"

        else:
            return "already hit"

        


    def all_ships_sunk(self):
        for row in self.grid:
            for cell in row:
                if 1 <= cell <= 5:
                    return False
        return True
