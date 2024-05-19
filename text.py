import math
import pygame as pg
import pygame.freetype as ft
from settings import *

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw(self):
        self.render_text((WIN_W * 0.595, WIN_H * 0.02), 'TETRIZZ', self.get_color(), TILE_SIZE * 1.65, 'black')
        self.render_text((WIN_W * 0.65, WIN_H * 0.22), 'next', 'orange', TILE_SIZE * 1.4, 'black')
        self.render_text((WIN_W * 0.64, WIN_H * 0.67), 'score', 'orange', TILE_SIZE * 1.4, 'black')
        self.render_text((WIN_W * 0.64, WIN_H * 0.8), f'{self.app.tetris.score}', 'white', TILE_SIZE * 1.8)
        
        level = self.app.level_manager.get_level()
        self.render_text((WIN_W * 0.64, WIN_H * 0.57), f'Level: {level}', 'orange', TILE_SIZE * 1.4, 'black')

    def draw_main_menu(self):
        self.render_text((WIDTH * 0.430, HEIGHT * 0.05), 'TetRizz', 'white', TILE_SIZE * 1.65)

    def render_text(self, position, text, color, size, bgcolor=None):
        self.font.render_to(self.app.screen, position, text=text, fgcolor=color, size=size, bgcolor=bgcolor)
