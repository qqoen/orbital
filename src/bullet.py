import pyxel as px
from src.common import *


class Bullet(Rect):
    def __init__(self, x, y, speed, color):
        super().__init__(x, y, 2, 8)
        self.speed = speed
        self.color = color
        self.is_destroyed = False

    def update(self):
        self.y -= self.speed

        if self.y <= 0 or self.y >= px.height:
            self.is_destroyed = True

    def draw(self):
        px.rect(self.x, self.y, self.w, self.h, self.color)
