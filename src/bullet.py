import pyxel as px
from src.common import *


class Bullet(Rect):
    def __init__(self, x, y, xspeed, yspeed, color):
        super().__init__(x, y, 2, 8)
        self._xspeed = xspeed
        self._yspeed = yspeed
        self._color = color
        self.is_destroyed = False

    def update(self):
        self.x += self._xspeed
        self.y += self._yspeed

        if self.y <= 0 or self.y >= px.height or self.x <= 0 or self.x >= px.width:
            self.is_destroyed = True

    def draw(self):
        px.rect(self.x, self.y, self.w, self.h, self._color)
