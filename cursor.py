import time
from pygame import Rect

from settings import Settings


class Cursor:
    """cursor class used in Typing Test"""
    
    def __init__(self):
        self.settings = Settings(name='cursor')
        
        self.light = None
        self.check_light()
        
        rect_dict = {
                'left': self.settings.center[0]-1.5*self.settings.width,
                'top': self.settings.center[1]-0.15*self.settings.height,
                'width': self.settings.width,
                'height': self.settings.height
        }
        self.rect = Rect(rect_dict['left'],
                         rect_dict['top'],
                         rect_dict['width'],
                         rect_dict['height'])
    
    def check_light(self):
        self.light = (int(time.time()*10) % 12) < 6


if __name__ == '__main__':
    pass