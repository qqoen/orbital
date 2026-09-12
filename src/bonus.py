import pyxel as px
from src.common import *


class Bonus(Rect):
    def __init__(self, x, y, score):
        super().__init__(x, y, 7, 7)
        self.score = score
        self.speed = 1
        self.is_destroyed = False

    def update(self):
        self.y += self.speed

        if self.y >= px.height:
            self.is_destroyed = True

    def draw(self):
        color = px.COLOR_WHITE if px.frame_count % 6 == 0 else px.COLOR_DARK_BLUE
        px.rect(self.x, self.y, self.w, self.h, color)
        px.text(self.x + 2, self.y + 1, "B", px.COLOR_WHITE)

    def pick(self):
        px.play(1, 3)
        self.is_destroyed = True
