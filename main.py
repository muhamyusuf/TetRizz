import pygame
import sys
from tetris import Tetris
from settings import settings
from utils import load_music, play_music, stop_music, draw_text, FONT

def reset_game():
    global solo_tetris, dual_tetris1, dual_tetris2, mode, winner

    solo_tetris = Tetris(
                    screen,
                    player_controls={'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP},
                    start_x=350,
                    start_y=25,
                    next_block_x=650,
                    next_block_y=50)
    
    dual_tetris1 = Tetris(
                    screen,
                    player_controls={'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'rotate': pygame.K_w},
                    start_x=50,
                    start_y=25,
                    next_block_x=350,
                    next_block_y=50)
    
    dual_tetris2 = Tetris(
                    screen,
                    player_controls={'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP},
                    start_x=500,
                    start_y=25,
                    next_block_x=800,
                    next_block_y=50)
    mode = 'menu'
    winner = None

def main():
    pygame.init()
    global screen, mode, winner
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Tetrizz")
    clock = pygame.time.Clock()

    if settings.music_on:
        load_music()
        play_music()

    # Initialize game modes
    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if mode == 'menu':
                    if event.key == pygame.K_1:
                        mode = 'solo'
                    elif event.key == pygame.K_2:
                        mode = 'dual'
                    elif event.key == pygame.K_s:
                        mode = 'settings'
                elif mode == 'settings':
                    if event.key == pygame.K_m:
                        settings.toggle_music()
                        if settings.music_on:
                            play_music()
                        else:
                            stop_music()
                    elif event.key == pygame.K_t:
                        settings.set_theme('light' if settings.theme == 'default' else 'default')
                        solo_tetris.update_theme()
                        dual_tetris1.update_theme()
                        dual_tetris2.update_theme()
                    elif event.key == pygame.K_ESCAPE:
                        mode = 'menu'
                elif mode == 'solo':
                    if event.key in solo_tetris.player_controls.values():
                        if event.key == solo_tetris.player_controls['left']:
                            solo_tetris.move_piece(-1, 0)
                        elif event.key == solo_tetris.player_controls['right']:
                            solo_tetris.move_piece(1, 0)
                        elif event.key == solo_tetris.player_controls['down']:
                            solo_tetris.move_piece(0, 1)
                        elif event.key == solo_tetris.player_controls['rotate']:
                            solo_tetris.rotate_piece()
                    if event.key == pygame.K_SPACE:
                        solo_tetris.drop_piece()
                elif mode == 'dual':
                    if event.key in dual_tetris1.player_controls.values():
                        if event.key == dual_tetris1.player_controls['left']:
                            dual_tetris1.move_piece(-1, 0)
                        elif event.key == dual_tetris1.player_controls['right']:
                            dual_tetris1.move_piece(1, 0)
                        elif event.key == dual_tetris1.player_controls['down']:
                            dual_tetris1.move_piece(0, 1)
                        elif event.key == dual_tetris1.player_controls['rotate']:
                            dual_tetris1.rotate_piece()
                    if event.key == pygame.K_RETURN:
                        dual_tetris1.drop_piece()

                    if event.key in dual_tetris2.player_controls.values():
                        if event.key == dual_tetris2.player_controls['left']:
                            dual_tetris2.move_piece(-1, 0)
                        elif event.key == dual_tetris2.player_controls['right']:
                            dual_tetris2.move_piece(1, 0)
                        elif event.key == dual_tetris2.player_controls['down']:
                            dual_tetris2.move_piece(0, 1)
                        elif event.key == dual_tetris2.player_controls['rotate']:
                            dual_tetris2.rotate_piece()
                    if event.key == pygame.K_SPACE:
                        dual_tetris2.drop_piece()
                elif mode in ['gameover', 'player1_win', 'player2_win']:
                    if event.key == pygame.K_r:
                        reset_game()

        dt = clock.tick(144) / 1000.0

        if mode == 'solo':
            solo_tetris.update(dt)
            screen.fill(settings.get_theme()['background_color'])
            solo_tetris.draw()
            if solo_tetris.game_over:
                mode = 'gameover'
        elif mode == 'dual':
            dual_tetris1.update(dt)
            dual_tetris2.update(dt)
            screen.fill(settings.get_theme()['background_color'])
            dual_tetris1.draw()
            dual_tetris2.draw()
            if dual_tetris1.game_over:
                winner = 'Player 2'
                mode = 'player2_win'
            if dual_tetris2.game_over:
                winner = 'Player 1'
                mode = 'player1_win'
        elif mode == 'settings':
            screen.fill(settings.get_theme()['background_color'])
            font = pygame.font.SysFont(FONT, 40)
            font_title = pygame.font.SysFont(FONT, 50)

            text_lines = [
                f"Music: {'On' if settings.music_on else 'Off'} (Press M to toggle)",
                f"Theme: {settings.theme} (Press T to toggle)",
                "Press ESC to return to menu"
            ]
            text_color = settings.get_theme()['text_color']

            draw_text(screen, "Settings", font_title, settings.get_theme()['text_color'], (screen.get_width()//2-65, 50))

            for i, line in enumerate(text_lines):
                text_surface = font.render(line, True, text_color)
                text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 200 + i * 40))
                draw_text(screen, line, font, text_color, text_rect.topleft)
            
            font_copyright = pygame.font.SysFont(FONT, 24)
            draw_text(screen, "Made by RizzGang.", font_copyright, settings.get_theme()['text_color'], (screen.get_width()//2-65, 650))
        elif mode == 'menu':
            screen.fill(settings.get_theme()['background_color'])
            font = pygame.font.SysFont(FONT, 40)
            font_title = pygame.font.SysFont(FONT, 50)
            font_copyright = pygame.font.SysFont(FONT, 24)

            text_lines = ["Solo Mode (Press 1)", "Dual Mode (Press 2)", "Settings (Press S)"]
            text_color = settings.get_theme()['text_color']

            draw_text(screen, "TetRizz", font_title, settings.get_theme()['text_color'], (screen.get_width()//2-65, 50))
            
            font_copyright = pygame.font.SysFont(FONT, 24)
            draw_text(screen, "Made by RizzGang.", font_copyright, settings.get_theme()['text_color'], (screen.get_width()//2-65, 650))

            for i, line in enumerate(text_lines):
                text_surface = font.render(line, True, text_color)
                text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 200 + i * 40))
                draw_text(screen, line, font, text_color, text_rect.topleft)

        elif mode == 'gameover':
            screen.fill(settings.get_theme()['background_color'])
            font = pygame.font.SysFont(FONT, 48)
            text_surface = font.render("Game Over", True, settings.get_theme()['text_color'])
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 250))
            screen.blit(text_surface, text_rect.topleft)
            font = pygame.font.SysFont(FONT, 24)
            text_surface = font.render("Press R to return to menu", True, settings.get_theme()['text_color'])
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 320))
            screen.blit(text_surface, text_rect.topleft)

        elif mode == 'player1_win':
            screen.fill(settings.get_theme()['background_color'])
            font = pygame.font.SysFont(FONT, 48)
            text_surface = font.render("Player 1 Wins!", True, settings.get_theme()['text_color'])
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 250))
            screen.blit(text_surface, text_rect.topleft)
            font = pygame.font.SysFont(FONT, 24)
            text_surface = font.render("Press R to return to menu", True, settings.get_theme()['text_color'])
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 320))
            screen.blit(text_surface, text_rect.topleft)

        elif mode == 'player2_win':
            screen.fill(settings.get_theme()['background_color'])
            font = pygame.font.SysFont(FONT, 48)
            text_surface = font.render("Player 2 Wins!", True, settings.get_theme()['text_color'])
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 250))
            screen.blit(text_surface, text_rect.topleft)
            font = pygame.font.SysFont(FONT, 24)
            text_surface = font.render("Press R to return to menu", True, settings.get_theme()['text_color'])
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 320))
            screen.blit(text_surface, text_rect.topleft)


        pygame.display.flip()

if __name__ == "__main__":
    main()
