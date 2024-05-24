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

class Menu(GameMode):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.SysFont(FONT, 40)
        self.font_title = pygame.font.SysFont(FONT, 50)
        self.font_small = pygame.font.SysFont(FONT, 24)

    def handle_event(self, event):
        if event.key == pygame.K_1:
            return 'solo'
        elif event.key == pygame.K_2:
            return 'dual'
        elif event.key == pygame.K_s:
            return 'settings'
        return 'menu'

    def draw(self):
        screen_center_x = self.screen.get_width() // 2

        title_text_surface = self.font_title.render("TetRizz", True, settings.get_theme()['text_color'])
        title_text_rect = title_text_surface.get_rect(center=(screen_center_x, 50))
        self.screen.blit(title_text_surface, title_text_rect.topleft)
        
        title_text_surface = self.font_small.render("Made by RizzGang", True, settings.get_theme()['text_color'])
        title_text_rect = title_text_surface.get_rect(center=(screen_center_x, 650))
        self.screen.blit(title_text_surface, title_text_rect.topleft)

        text_lines = ["Solo Mode (Press 1)", "Dual Mode (Press 2)", "Settings (Press S)"]
        for i, line in enumerate(text_lines):
            text_surface = self.font.render(line, True, settings.get_theme()['text_color'])
            text_rect = text_surface.get_rect(center=(screen_center_x, 200 + i * 40))
            self.screen.blit(text_surface, text_rect.topleft)

class SettingsScreen(GameMode):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.SysFont(FONT, 40)
        self.font_title = pygame.font.SysFont(FONT, 50)
        self.font_small = pygame.font.SysFont(FONT, 24)

    def handle_event(self, event):
        if event.key == pygame.K_m:
            settings.toggle_music()
            if settings.music_on:
                play_music()
            else:
                stop_music()
        elif event.key == pygame.K_t:
            settings.set_theme('light' if settings.theme == 'default' else 'default')
        elif event.key == pygame.K_ESCAPE:
            return 'menu'
        return 'settings'

    def draw(self):
        screen_center_x = self.screen.get_width() // 2

        title_text_surface = self.font_title.render("Settings", True, settings.get_theme()['text_color'])
        title_text_rect = title_text_surface.get_rect(center=(screen_center_x, 50))
        self.screen.blit(title_text_surface, title_text_rect.topleft)
        
        title_text_surface = self.font_small.render("Made by RizzGang", True, settings.get_theme()['text_color'])
        title_text_rect = title_text_surface.get_rect(center=(screen_center_x, 650))
        self.screen.blit(title_text_surface, title_text_rect.topleft)

        text_lines = [
            f"Music: {'On' if settings.music_on else 'Off'} (Press M to toggle)",
            f"Theme: {settings.theme} (Press T to toggle)",
            "Press ESC to return to menu"
        ]
        
        for i, line in enumerate(text_lines):
            text_surface = self.font.render(line, True, settings.get_theme()['text_color'])
            text_rect = text_surface.get_rect(center=(screen_center_x, 200 + i * 40))
            self.screen.blit(text_surface, text_rect.topleft)

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

