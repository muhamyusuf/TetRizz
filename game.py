import pygame
from tetris import Tetris
from settings import settings
from utils import FONT, play_music, stop_music
from abc import ABC, abstractmethod

class GameMode(ABC):
    def __init__(self, screen):
        self.screen = screen

    @abstractmethod
    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    @abstractmethod
    def draw(self):
        pass

class SoloTetrisGame(GameMode):
    def __init__(self, screen):
        super().__init__(screen)
        self.tetris = Tetris(screen, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP}, 350, 25, 650, 50)

    def handle_event(self, event):
        if event.key in self.tetris.player_controls.values():
            if event.key == self.tetris.player_controls['left']:
                self.tetris.move_piece(-1, 0)
            elif event.key == self.tetris.player_controls['right']:
                self.tetris.move_piece(1, 0)
            elif event.key == self.tetris.player_controls['down']:
                self.tetris.move_piece(0, 1)
            elif event.key == self.tetris.player_controls['rotate']:
                self.tetris.rotate_piece()
        if event.key == pygame.K_SPACE:
            self.tetris.drop_piece()
        return 'solo' if not self.tetris.game_over else 'gameover'

    def update(self, dt):
        self.tetris.update(dt)

    def draw(self):
        self.tetris.draw()

class DualTetrisGame(GameMode):
    def __init__(self, screen):
        super().__init__(screen)
        self.tetris1 = Tetris(screen, {'left': pygame.K_a, 'right': pygame.K_d, 'down': pygame.K_s, 'rotate': pygame.K_w}, 50, 25, 350, 50)
        self.tetris2 = Tetris(screen, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'down': pygame.K_DOWN, 'rotate': pygame.K_UP}, 500, 25, 800, 50)

    def handle_event(self, event):
        if event.key in self.tetris1.player_controls.values():
            if event.key == self.tetris1.player_controls['left']:
                self.tetris1.move_piece(-1, 0)
            elif event.key == self.tetris1.player_controls['right']:
                self.tetris1.move_piece(1, 0)
            elif event.key == self.tetris1.player_controls['down']:
                self.tetris1.move_piece(0, 1)
            elif event.key == self.tetris1.player_controls['rotate']:
                self.tetris1.rotate_piece()
        if event.key == pygame.K_LSHIFT:
            self.tetris1.drop_piece()

        if event.key in self.tetris2.player_controls.values():
            if event.key == self.tetris2.player_controls['left']:
                self.tetris2.move_piece(-1, 0)
            elif event.key == self.tetris2.player_controls['right']:
                self.tetris2.move_piece(1, 0)
            elif event.key == self.tetris2.player_controls['down']:
                self.tetris2.move_piece(0, 1)
            elif event.key == self.tetris2.player_controls['rotate']:
                self.tetris2.rotate_piece()
        if event.key == pygame.K_SPACE:
            self.tetris2.drop_piece()
        
        if self.tetris1.game_over:
            return 'player2_win'
        elif self.tetris2.game_over:
            return 'player1_win'
        return 'dual'

    def update(self, dt):
        self.tetris1.update(dt)
        self.tetris2.update(dt)

    def draw(self):
        self.tetris1.draw()
        self.tetris2.draw()

class GameOverScreen(GameMode):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.SysFont(FONT, 48)
        self.font_small = pygame.font.SysFont(FONT, 24)

    def handle_event(self, event):
        if event.key == pygame.K_r:
            return 'menu'
        return 'gameover'

    def draw(self):
        screen_center_x = self.screen.get_width() // 2

        game_over_text_surface = self.font.render("Game Over", True, settings.get_theme()['text_color'])
        game_over_text_rect = game_over_text_surface.get_rect(center=(screen_center_x, 250))
        self.screen.blit(game_over_text_surface, game_over_text_rect.topleft)
        
        title_text_surface = self.font_small.render("Made by RizzGang", True, settings.get_theme()['text_color'])
        title_text_rect = title_text_surface.get_rect(center=(screen_center_x, 650))
        self.screen.blit(title_text_surface, title_text_rect.topleft)

        return_text_surface = self.font_small.render("Press R to return to menu", True, settings.get_theme()['text_color'])
        return_text_rect = return_text_surface.get_rect(center=(screen_center_x, 320))
        self.screen.blit(return_text_surface, return_text_rect.topleft)

class PlayerWinScreen(GameMode):
    def __init__(self, screen, message):
        super().__init__(screen)
        self.message = message
        self.font = pygame.font.SysFont(FONT, 48)
        self.font_small = pygame.font.SysFont(FONT, 24)

    def handle_event(self, event):
        if event.key == pygame.K_r:
            return 'menu'
        return 'player1_win' if '1' in self.message else 'player2_win'

    def draw(self):
        screen_center_x = self.screen.get_width() // 2

        message_text_surface = self.font.render(self.message, True, settings.get_theme()['text_color'])
        message_text_rect = message_text_surface.get_rect(center=(screen_center_x, 250))
        self.screen.blit(message_text_surface, message_text_rect.topleft)
        
        title_text_surface = self.font_small.render("Made by RizzGang", True, settings.get_theme()['text_color'])
        title_text_rect = title_text_surface.get_rect(center=(screen_center_x, 650))
        self.screen.blit(title_text_surface, title_text_rect.topleft)

        return_text_surface = self.font_small.render("Press R to return to menu", True, settings.get_theme()['text_color'])
        return_text_rect = return_text_surface.get_rect(center=(screen_center_x, 320))
        self.screen.blit(return_text_surface, return_text_rect.topleft)

