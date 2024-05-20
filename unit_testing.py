import unittest
import pygame
from game import Menu, SettingsScreen, SoloTetrisGame, DualTetrisGame, GameOverScreen, PlayerWinScreen
from settings import settings

class TestMenu(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.menu = Menu(self.screen)

    def test_handle_event(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
        self.assertEqual(self.menu.handle_event(event), 'solo')
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2)
        self.assertEqual(self.menu.handle_event(event), 'dual')
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s)
        self.assertEqual(self.menu.handle_event(event), 'settings')
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x)
        self.assertEqual(self.menu.handle_event(event), 'menu')

    def tearDown(self):
        pygame.quit()

class TestSettingsScreen(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.settings_screen = SettingsScreen(self.screen)

    def test_handle_event(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)
        initial_music_on = settings.music_on
        self.settings_screen.handle_event(event)
        self.assertNotEqual(settings.music_on, initial_music_on)

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_t)
        initial_theme = settings.theme
        self.settings_screen.handle_event(event)
        self.assertNotEqual(settings.theme, initial_theme)

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        self.assertEqual(self.settings_screen.handle_event(event), 'menu')

    def tearDown(self):
        pygame.quit()

class TestSoloTetrisGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.solo_game = SoloTetrisGame(self.screen)

    def test_handle_event(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        self.solo_game.handle_event(event)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        self.solo_game.handle_event(event)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        self.solo_game.handle_event(event)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        self.solo_game.handle_event(event)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.solo_game.handle_event(event)

    def tearDown(self):
        pygame.quit()

class TestDualTetrisGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.dual_game = DualTetrisGame(self.screen)

    def test_handle_event(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)
        self.dual_game.handle_event(event)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d)
        self.dual_game.handle_event(event)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s)
        self.dual_game.handle_event(event)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
        self.dual_game.handle_event(event)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LSHIFT)
        self.dual_game.handle_event(event)
        
    def tearDown(self):
        pygame.quit()

class TestGameOverScreen(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.gameover_screen = GameOverScreen(self.screen)

    def test_handle_event(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
        self.assertEqual(self.gameover_screen.handle_event(event), 'menu')

    def tearDown(self):
        pygame.quit()

class TestPlayerWinScreen(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.player1_win_screen = PlayerWinScreen(self.screen, "Player 1 Wins!")
        self.player2_win_screen = PlayerWinScreen(self.screen, "Player 2 Wins!")

    def test_handle_event(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
        self.assertEqual(self.player1_win_screen.handle_event(event), 'menu')
        self.assertEqual(self.player2_win_screen.handle_event(event), 'menu')

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
