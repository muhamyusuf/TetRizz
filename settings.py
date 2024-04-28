import pygame as pg

vec = pg.math.Vector2

FPS = 60
FIELD_COLOR = (0, 0, 0)
BG_COLOR = (0, 0, 0)

SPRITE_DIR_PATH = 'assets/rizz'
FONT_PATH = 'assets/font/helvetica-compressed.otf'

ANIM_TIME_INTERVAL = 500  # milliseconds 
# lvl 1 500
# lvl 2 400
# lvl 3 300
# lvl 4 200
# lvl 5 100
# lvl 6 80
# lvl 7 60
# lvl 8 40
# lvl 9 20
# lvl DEWA 10 10

FAST_ANIM_TIME_INTERVAL = 15

TILE_SIZE = 25
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

INIT_POS_OFFSET = vec(FIELD_W // 2 - 1, 0)
NEXT_POS_OFFSET = vec(FIELD_W * 1.3, FIELD_H * 0.45)
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}
