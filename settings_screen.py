import sys
import pygame as pg
from settings import *
from theming import SetTheme  # Jika Anda ingin menggunakan kelas SetTheme

class SettingsScreen:
    def __init__(self, app):
        self.app = app
        self.theme_buttons = self.create_theme_buttons()
        self.music_button = self.create_music_button()
        self.back_button = self.create_back_button()

    def create_theme_buttons(self):
        light_button = self.app.draw_button("Light Theme", (WIN_RES[0] // 2, WIN_RES[1] // 2 - 100))
        dark_button = self.app.draw_button("Dark Theme", (WIN_RES[0] // 2, WIN_RES[1] // 2 - 50))
        return light_button, dark_button

    def create_music_button(self):
        music_button_text = "Music: On" if CURRENT_MUSIC else "Music: Off"
        return self.app.draw_button(music_button_text, (WIN_RES[0] // 2, WIN_RES[1] // 2))

    def create_back_button(self):
        return self.app.draw_button("Back", (WIN_RES[0] // 2, WIN_RES[1] // 2 + 50))

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in self.theme_buttons:
                    if button.collidepoint(mouse_pos):
                        self.set_theme(button.text)  # Atur tema sesuai tombol yang ditekan
                if self.music_button.collidepoint(mouse_pos):
                    self.toggle_music()  # Toggle status musik
                if self.back_button.collidepoint(mouse_pos):
                    self.app.current_screen = "menu"  # Kembali ke main menu

    def set_theme(self, theme_text):
        if theme_text == "Light Theme":
            CURRENT_THEME = THEME_LIGHT
        elif theme_text == "Dark Theme":
            CURRENT_THEME = THEME_DARK
        # Terapkan tema ke seluruh tampilan game
        SetTheme.apply_theme(CURRENT_THEME)

    def toggle_music(self):
        global CURRENT_MUSIC
        CURRENT_MUSIC = not CURRENT_MUSIC
        music_button_text = "Music: On" if CURRENT_MUSIC else "Music: Off"
        self.music_button = self.app.draw_button(music_button_text, (WIN_RES[0] // 2, WIN_RES[1] // 2))

    def update(self):
        self.handle_events()
        self.app.screen.fill(color=BG_COLOR)
        # Gambar komponen-komponen UI ke layar
        self.app.screen.blit(self.back_button)
        self.app.screen.blit(self.music_button)
        for button in self.theme_buttons:
            self.app.screen.blit(button)
        pg.display.update()
