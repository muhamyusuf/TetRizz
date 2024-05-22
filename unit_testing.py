import unittest
import pygame
from game import Menu, SettingsScreen, SoloTetrisGame, DualTetrisGame, GameOverScreen, PlayerWinScreen
from settings import settings
from utils import load_music, play_music, stop_music, draw_text, FONT
from tetris import Tetris

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
        print("TestMenu test_handle_event passed")

    def tearDown(self):
        pygame.quit()

class TestSettingsScreen(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.settings_screen = SettingsScreen(self.screen)
        load_music()  # Ensure music is loaded before tests

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
        print("TestSettingsScreen test_handle_event passed")

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
        print("TestSoloTetrisGame test_handle_event passed")

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
        print("TestDualTetrisGame test_handle_event passed")

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
        print("TestGameOverScreen test_handle_event passed")

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
        print("TestPlayerWinScreen test_handle_event passed")

    def tearDown(self):
        pygame.quit()

class TestSettings(unittest.TestCase):
    def test_toggle_music(self):
        initial_music_on = settings.music_on
        settings.toggle_music()
        self.assertNotEqual(settings.music_on, initial_music_on)
        print("TestSettings test_toggle_music passed")

    def test_set_theme(self):
        initial_theme = settings.theme
        new_theme = 'light' if initial_theme == 'default' else 'default'
        settings.set_theme(new_theme)
        self.assertEqual(settings.theme, new_theme)
        print("TestSettings test_set_theme passed")

class TestTetris(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.tetris = Tetris(self.screen, {}, 0, 0, 0, 0)
        self.tetris.current_piece = self.tetris.get_new_piece()
        while self.tetris.current_piece['shape'] == [[1, 1], [1, 1]]:  # Ensure the piece is not O-shape
            self.tetris.current_piece = self.tetris.get_new_piece()

    def test_create_grid(self):
        grid = self.tetris.create_grid()
        self.assertEqual(len(grid), 20)
        self.assertEqual(len(grid[0]), 10)
        print("TestTetris test_create_grid passed")

    def test_clear_lines(self):
        self.tetris.grid = [[1]*10] + [[0]*10]*19
        self.tetris.clear_lines()
        self.assertEqual(self.tetris.grid, [[0]*10]*20)
        print("TestTetris test_clear_lines passed")

    def test_move_piece(self):
        piece = self.tetris.current_piece
        original_x = piece['x']
        original_y = piece['y']
        self.tetris.move_piece(1, 1)
        self.assertEqual(piece['x'], original_x + 1)
        self.assertEqual(piece['y'], original_y + 1)
        print("TestTetris test_move_piece passed")

    def test_rotate_piece(self):
        original_shape = self.tetris.current_piece['shape']
        self.tetris.rotate_piece()
        rotated_shape = self.tetris.current_piece['shape']
        self.assertNotEqual(original_shape, rotated_shape)
        print("TestTetris test_rotate_piece passed")

    def test_check_collision(self):
        # Ubah grid menjadi satu baris penuh di bagian bawah agar terdeteksi collision
        self.tetris.grid = [[0]*10 for _ in range(self.tetris.grid_height - 1)] + [[1]*10]
        self.tetris.current_piece['y'] = self.tetris.grid_height - len(self.tetris.current_piece['shape'])
        self.assertTrue(self.tetris.check_collision())
        print("TestTetris test_check_collision passed")

    def tearDown(self):
        pygame.quit()

class TestUtils(unittest.TestCase):
    def test_draw_text(self):
        pygame.init()
        screen = pygame.display.set_mode((1000, 700))
        font = pygame.font.SysFont(FONT, 24)
        draw_text(screen, "Test", font, (255, 255, 255), (50, 50))
        print("TestUtils test_draw_text passed")
        pygame.quit()

    def test_play_music(self):
        pygame.init()
        load_music()
        play_music()
        # No assertion needed; if no exception is raised, the test is considered passed.
        print("TestUtils test_play_music passed")

    def test_stop_music(self):
        pygame.init()
        stop_music()
        # No assertion needed; if no exception is raised, the test is considered passed.
        print("TestUtils test_stop_music passed")
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
