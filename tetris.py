import pygame
import random
from settings import settings
from utils import draw_text, load_image, FONT

# Define the shapes of the blocks
SHAPES = [
    [[1, 1, 1, 1]],          # I shape
    [[1, 1], [1, 1]],        # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 1, 1], [1, 0, 0]],  # J shape
    [[1, 1, 1], [0, 0, 1]]   # L shape
]

class Tetris:
    def __init__(self, screen, player_controls, start_x, start_y, next_block_x, next_block_y, player_text=None):
        self.screen = screen
        self.player_controls = player_controls
        self.start_x = start_x
        self.start_y = start_y
        self.next_block_x = next_block_x
        self.next_block_y = next_block_y
        self.player_text = player_text
        self.grid_width = 10
        self.grid_height = 20
        self.grid = self.create_grid()
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.score = 0
        self.level = 1
        self.fall_speed = 0.5
        self.fall_time = 0
        self.game_over = False
        self.update_theme()

    def update_theme(self):
        self.block_image = load_image(settings.get_block_image_path())
        self.shadow_color = (128, 128, 128)  # Set the shadow color

    def create_grid(self):
        return [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def get_new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(settings.get_theme()['block_colors'])
        return {'shape': shape, 'color': color, 'x': self.grid_width // 2 - len(shape[0]) // 2, 'y': 0}

    def rotate_piece(self):
        shape = self.current_piece['shape']
        self.current_piece['shape'] = [list(row) for row in zip(*shape[::-1])]
        if self.check_collision():
            self.current_piece['shape'] = shape  # revert rotation if collision

    def lock_piece(self):
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        if self.check_collision():
            self.game_over = True  # Game over

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0 for _ in range(self.grid_width)])
        self.score += len(lines_to_clear) * 10
        if len(lines_to_clear) > 0:
            self.level += 1
            self.fall_speed *= 0.9

    def drop_piece(self):
        while self.move_piece(0, 1):
            pass
        self.lock_piece()

    def calculate_shadow_position(self):
        original_y = self.current_piece['y']
        while not self.check_collision():
            self.current_piece['y'] += 1
        self.current_piece['y'] -= 1
        shadow_y = self.current_piece['y']
        self.current_piece['y'] = original_y
        return shadow_y

    def update(self, dt):
        self.fall_time += dt
        if self.fall_time > self.fall_speed:
            self.fall_time = 0
            if not self.move_piece(0, 1):
                self.lock_piece()

    def draw_grid(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                rect = pygame.Rect(self.start_x + x * 30, self.start_y + y * 30, 30, 30)
                pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)

    def draw_next_piece(self):
        shape = self.next_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.screen.blit(self.block_image, (self.next_block_x + x * 30, self.next_block_y + y * 30))

    def draw(self):
        shadow_y = self.calculate_shadow_position()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    self.screen.blit(self.block_image, (self.start_x + x * 30, self.start_y + y * 30))
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    # Draw the shadow
                    shadow_rect = pygame.Rect(self.start_x + (self.current_piece['x'] + x) * 30, self.start_y + (shadow_y + y) * 30, 30, 30)
                    pygame.draw.rect(self.screen, self.shadow_color, shadow_rect)
                    # Draw the current piece
                    self.screen.blit(self.block_image, (self.start_x + (self.current_piece['x'] + x) * 30, self.start_y + (self.current_piece['y'] + y) * 30))
        
        self.draw_grid()
        self.draw_next_piece()
        font = pygame.font.SysFont(FONT, 24)
        draw_text(self.screen, 'Next piece:', font, settings.get_theme()['text_color'], (self.start_x + 300, self.start_y-1))
        
        draw_text(self.screen, f'Score: {self.score}', font, settings.get_theme()['text_color'], (self.start_x + 300, self.start_y + 100))
        draw_text(self.screen, f'Level: {self.level}', font, settings.get_theme()['text_color'], (self.start_x + 300, self.start_y + 125))