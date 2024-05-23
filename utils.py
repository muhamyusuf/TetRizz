FONT = 'assets/fonts/helvetica-reguler.otf'

import pygame

def load_music():
    pygame.mixer.music.load('assets/music/tetris-remix.ogg')

def play_music():
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def draw_text(surface, text, font, color, position):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, position)

def load_image(path):
    return pygame.image.load(path).convert_alpha()