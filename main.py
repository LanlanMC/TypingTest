"""Typing test"""

import sys
import pygame
from random import shuffle

from settings import Settings
from timer import Timer
from cursor import Cursor


class Test:
    """The typing test main class"""
    
    def __init__(self, game_window):
        pygame.init()
        self.settings = Settings(name='main')
        self.words = self.load()
        self.wrong_letters = ''
        self.typed = False
        self.typed_words = ''
        
        # initialize the keys
        self.keys_dict = {eval("pygame.K_"+e): key
                          for e, key in [('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'), ('e', 'e'), ('f', 'f'),
                                         ('g', 'g'), ('h', 'h'), ('i', 'i'), ('j', 'j'), ('k', 'k'), ('l', 'l'),
                                         ('m', 'm'), ('n', 'n'), ('o', 'o'), ('p', 'p'), ('q', 'q'), ('r', 'r'),
                                         ('s', 's'), ('t', 't'), ('u', 'u'), ('v', 'v'), ('w', 'w'), ('x', 'x'),
                                         ('y', 'y'), ('z', 'z'),
                                         ('SPACE', ' '), ('PERIOD', '.'), ('COMMA', ',')]}
        self.shift = False
        
        # initialize the window
        pygame.display.set_caption("Typing Test")
        icon = pygame.font.SysFont("Arial", 32).render("Test", True, (0, 144, 0))
        pygame.display.set_icon(icon)
        self.window = game_window
        
        # initialize the font
        self.word_font = pygame.font.SysFont('Consolas', 32)
        self.fps_font = pygame.font.SysFont('Consolas', 12)
        
        self.string = ' '.join(self.words)
        
        # initialize the frame rate
        self.clock = pygame.time.Clock()
        self.fps = self.clock.get_fps()
        
        # initialize the cursor
        self.cursor = Cursor()
        
        # initialize the timer
        self.timer = None
    
    @staticmethod
    def load():
        """Load the words needed"""
        with open(file='resources/words.txt', mode='r', encoding='ASCII') as f:
            words = f.read().split(sep='\n')
            shuffle(words)
            return words
    
    def get_keys(self, event) -> str:
        try:
            return self.keys_dict[event]
        except KeyError:
            return ''
    
    def check_keys(self):
        key_pressed = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                elif event.key == pygame.K_BACKSPACE:
                    self.delete()
                elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    self.shift = True
                else:
                    key = self.get_keys(event=event.key)
                    if key:
                        if key == ' ' and self.typed_words.endswith(' '):
                            pass
                        elif self.shift:
                            key_pressed.append(key.upper())
                        else:
                            key_pressed.append(key)
                    self.shift = False
        
        if len(key_pressed) != 1:
            return ''
        else:
            self.typed = True
            return key_pressed[0]
    
    def delete(self):
        """response your deleting action"""
        self.wrong_letters = self.wrong_letters[:-1]
    
    def typing(self, key):
        """response your typing action"""
        if self.typed:
            if not self.wrong_letters and self.string.startswith(key):
                self.typed_words += key
                self.string = self.string[1:]
            elif key == ' ' and self.typed_words.endswith(' ') or not self.typed_words:
                pass
            elif self.string.startswith(' ') and key == ' ':
                self.wrong_letters = ''
            elif key == ' ':
                self.string = ' '.join(self.string.split()[1:])
                self.wrong_letters = ''
            else:
                self.wrong_letters += key
            self.typed = False
    
    def render(self):
        """render everything on the screen"""
        '''get the images ready'''
        # font
        fps_img = self.fps_font.render('FPS:'+str(int(self.fps))+'/240', True, self.settings.fps_color)
        words_img = self.word_font.render(self.string, True, self.settings.string_color)
        typed_words_img = self.word_font.render(self.typed_words, True, self.settings.typed_words_color)
        wrong_letters_img = self.word_font.render(self.wrong_letters, True, self.settings.wrong_words_color)
        
        # wrong letter rect
        width = wrong_letters_img.get_width()
        height = 2
        wrong_rect = pygame.Rect(self.settings.center[0]-wrong_letters_img.get_width(),
                                 self.settings.center[1]+0.45*wrong_letters_img.get_height(),
                                 width, height)
        
        '''render the images on the screen'''
        # background
        self.window.fill(self.settings.window_color)
        
        # font
        self.window.blit(fps_img, (0, 0))
        self.window.blit(words_img, self.settings.center)
        self.window.blit(typed_words_img, (self.settings.center[0]-wrong_letters_img.get_width()
                                           - typed_words_img.get_width(),
                                           self.settings.center[1]))
        self.window.blit(wrong_letters_img, (self.settings.center[0]-wrong_letters_img.get_width(),
                                             self.settings.center[1]))
        
        # cross out wrong letter
        pygame.draw.rect(self.window, self.settings.wrong_rect_color, wrong_rect)
        
        # cursor
        if self.cursor.light:
            pygame.draw.rect(self.window, self.settings.cursor_color, self.cursor.rect)
    
    def main(self):
        while True:
            self.cursor.check_light()
            
            key = self.check_keys()
            self.typing(key)

            self.render()
            
            pygame.display.flip()
            self.clock.tick(240)
            self.fps = self.clock.get_fps()


if __name__ == '__main__':
    window = pygame.display.set_mode(Settings().bg_size)
    test = Test(window)
    test.main()
