class Settings:
    def __init__(self):
        self.theme = 'default'
        self.music_on = True

    def set_theme(self, theme_name):
        self.theme = theme_name

    def toggle_music(self):
        self.music_on = not self.music_on

    def get_theme(self):
        from themes import themes
        return themes[self.theme]

    def get_block_image_path(self):
        return self.get_theme()['block_image']

settings = Settings()
