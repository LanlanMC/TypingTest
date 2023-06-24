class Settings:
    def __init__(self, name='main'):
        self.bg_size = (800, 480)
        self.center = tuple(int(value/2) for value in self.bg_size)
        
        if name == 'cursor':
            self.width = 2
            self.height = 35
        
        # colors
        self.window_color = (255, 255, 255)
        self.fps_color = self.string_color = (0, 0, 0)
        self.typed_words_color = self.wrong_words_color = (110, 93, 187)
        self.wrong_rect_color = (110, 93, 187)
        self.cursor_color = (212, 215, 255)
