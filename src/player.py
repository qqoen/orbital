import pyxel as px
from src.bullet import Bullet
from src.common import *


class Player(Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.sprite = Sprite(0, 0)
        self.speed = 2
        self.bullets = []

    def update(self):
        if px.btn(px.KEY_LEFT):
            self.x -= self.speed
        elif px.btn(px.KEY_RIGHT):
            self.x += self.speed

        if px.btnp(px.KEY_SPACE):
            bullet = Bullet(self.x + self.w // 2 - 1, self.y, 3, px.COLOR_WHITE)
            self.bullets.append(bullet)
            px.play(0, 0)

        self.x = px.clamp(self.x, 0, px.width - self.w)
        update_list(self.bullets)

    def draw(self):
        self.sprite.draw(self.x, self.y)
        draw_list(self.bullets)
