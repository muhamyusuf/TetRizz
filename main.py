import sys
import pathlib
import pygame as pg

from settings import *
from tetris import Tetris
from text import Text
from level import LevelManager
# from settings_screen import SettingsScreen
# from theming import SetTheme

pg.init()
pg.mixer.init()

pg.mixer.music.load('assets/song/tetris-remix.ogg')
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(loops=-1)

# Memberhentikan lagu (opsional)
# pg.mixer.music.stop()


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetrizz')
        self.screen = pg.display.set_mode(GAME_SCREEN)
        self.clock = pg.time.Clock()
        self.current_screen = "menu"
        self.theme = "light"
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.level_manager = LevelManager(0)

    def draw_button(self, text, position, button_size=(200, 60)):
        font = pg.font.Font(FONT_PATH, 36)
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=position)

        button_width, button_height = button_size
        button_rect = pg.Rect(0, 0, button_width, button_height)
        button_rect.center = position

        button_surface = pg.Surface((button_width, button_height), pg.SRCALPHA)
        button_surface.fill((0, 0, 0, 0))  # Make the surface transparent

        # Draw filled rounded rectangle
        border_radius = 15
        pg.draw.rect(button_surface, (0, 0, 0, 0), button_surface.get_rect(), border_radius=border_radius)

        # Draw the outline
        pg.draw.rect(button_surface, (255, 255, 255), button_surface.get_rect(), width=2, border_radius=border_radius)

        # Adjust the position of the text to be centered within the button
        text_rect.center = button_rect.center

        # Blit the button surface onto the main screen
        self.screen.blit(button_surface, button_rect.topleft)
        self.screen.blit(text_surf, text_rect)

        return button_rect
    
    def handle_menu_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.solo_button.collidepoint(mouse_pos):
                    self.run()
                elif self.dual_button.collidepoint(mouse_pos):
                    print("Dual Player mode selected")
                elif self.settings_button.collidepoint(mouse_pos):
                    print("Settings selected")

    def main_menu(self):
        while True:
            self.handle_menu_events()

            # self.screen.blit(background_dark, (0, 0))
            if self.theme == "light":
                self.screen.blit(background_light, (0, 0))
            if self.theme == "dark":
                self.screen.blit(background_dark, (0, 0))

            self.text.draw_main_menu()
            
            self.solo_button = self.draw_button("Solo Player", (GAME_SCREEN[0] // 2, GAME_SCREEN[1] // 2 - 75))
            self.dual_button = self.draw_button("Dual Player", (GAME_SCREEN[0] // 2, GAME_SCREEN[1] // 2))
            self.settings_button = self.draw_button("Settings", (GAME_SCREEN[0] // 2, GAME_SCREEN[1] // 2 + 75))

            pg.display.update()
            self.clock.tick(FPS)

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    
    app.main_menu()
    
