import pygame
import random

# Constants
GAME_SIZE = 3
TILE_SIZE = 100
WINDOW_SIZE = GAME_SIZE * TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sliding Puzzle")


# Game Class
class Game:
    def __init__(self):
        self.tiles = []
        self.tiles_grid = []
        self.empty_tile = None
        self.running = True

    def generate_tiles(self):
        numbers = list(range(1, GAME_SIZE ** 2))
        random.shuffle(numbers)

        for row in range(GAME_SIZE):
            tile_row = []
            grid_row = []
            for col in range(GAME_SIZE):
                if row == GAME_SIZE - 1 and col == GAME_SIZE - 1:
                    tile_row.append(None)
                    grid_row.append(0)
                    self.empty_tile = (row, col)
                else:
                    number = numbers.pop()
                    tile_row.append(number)
                    grid_row.append(number)
            self.tiles.append(tile_row)
            self.tiles_grid.append(grid_row)

    def draw_tiles(self):
        window.fill(WHITE)
        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                if self.tiles[row][col]:
                    pygame.draw.rect(window, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    font = pygame.font.SysFont(None, 48)
                    text = font.render(str(self.tiles[row][col]), True, WHITE)
                    text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE / 2, row * TILE_SIZE + TILE_SIZE / 2))
                    window.blit(text, text_rect)

    def move_tile(self, row, col):
        if (row, col) == self.empty_tile:
            return

        if row == self.empty_tile[0]:
            direction = -1 if col < self.empty_tile[1] else 1
            for c in range(col, self.empty_tile[1], direction):
                self.tiles[row][c], self.tiles[row][c + direction] = self.tiles[row][c + direction], self.tiles[row][c]
        elif col == self.empty_tile[1]:
            direction = -1 if row < self.empty_tile[0] else 1
            for r in range(row, self.empty_tile[0], direction):
                self.tiles[r][col], self.tiles[r + direction][col] = self.tiles[r + direction][col], self.tiles[r][col]
        else:
            return

        self.empty_tile = (row, col)

    def is_solved(self):
        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                if self.tiles[row][col] != row * GAME_SIZE + col + 1:
                    return False
        return True

    def handle_click(self, pos):
        col = pos[0] // TILE_SIZE
        row = pos[1] // TILE_SIZE

        if (row, col) == self.empty_tile:
            return

        if row == self.empty_tile[0] and abs(col - self.empty_tile[1]) == 1:
            self.move_tile(row, col)
        elif col == self.empty_tile[1] and abs(row - self.empty_tile[0]) == 1:
            self.move_tile(row, col)

    def solve(self):
        # A* Search Algorithm
        def manhattan_distance(start, end):
            return abs(start[0] - end[0]) + abs(start[1] - end[1])

        def find_empty_tile(grid):
            for row in range(GAME_SIZE):
                for col in range(GAME_SIZE):
                    if grid[row][col] == 0:
                        return (row, col)

        class Node:
            def __init__(self, grid, parent, move, g, h):
                self.grid = grid
                self.parent = parent
                self.move = move
                self.g = g
                self.h = h
                self.f = g + h

            def __eq__(self, other):
                return self.grid == other.grid

        start_node = Node(self.tiles_grid, None, None, 0, 0)
        open_list = [start_node]
        closed_list = []

        while open_list:
            current_node = open_list[0]
            current_index = 0

            for index, node in enumerate(open_list):
                if node.f < current_node.f:
                    current_node = node
                    current_index = index

            open_list.pop(current_index)


game = Game()
while True:
    game.new()
    game.run()
