import pygame
import sys
from settings import settings
from utils import load_music, play_music
from game import SoloTetrisGame, DualTetrisGame, Menu, SettingsScreen, GameOverScreen, PlayerWinScreen

def initialize_game_modes(screen):
    return {
        'menu': Menu(screen),
        'settings': SettingsScreen(screen),
        'solo': SoloTetrisGame(screen),
        'dual': DualTetrisGame(screen),
        'gameover': GameOverScreen(screen),
        'player1_win': PlayerWinScreen(screen, "Player 1 Wins!"),
        'player2_win': PlayerWinScreen(screen, "Player 2 Wins!")
    }

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Tetrizz")
    clock = pygame.time.Clock()

    if settings.music_on:
        load_music()
        play_music()

    game_modes = initialize_game_modes(screen)
    mode = 'menu'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                new_mode = game_modes[mode].handle_event(event)
                if new_mode != mode:
                    if new_mode in ['menu', 'gameover', 'player1_win', 'player2_win']:
                        game_modes = initialize_game_modes(screen)
                    mode = new_mode

        dt = clock.tick(144) / 1000.0

        if mode == 'solo' and game_modes[mode].tetris.game_over:
            mode = 'gameover'
        elif mode == 'dual':
            if game_modes[mode].tetris1.game_over:
                mode = 'player2_win'
            elif game_modes[mode].tetris2.game_over:
                mode = 'player1_win'

        screen.fill(settings.get_theme()['background_color'])
        game_modes[mode].update(dt)
        game_modes[mode].draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()
