import pyxel as px
from src.common import *
from src.bullet import Bullet


class Enemy(Rect):
    def __init__(self, x, y, bullets, enemy_type):
        super().__init__(x, y, 16, 16)
        self._bullets = bullets
        self.health = enemy_type["health"]
        self.sprite = enemy_type["sprite"]
        self.is_shooting = enemy_type["is_shooting"]
        self.score = enemy_type["score"]

        self.speed = 1
        self.is_destroyed = False
        self.start_x = x
        self._shoot_frame = -200

    def update(self):
        if px.frame_count % 2 == 0:
            self.x += self.speed

        if self.x - self.start_x >= 112:
            self.speed = -1

        if self.x < self.start_x:
            self.speed = 1

        if self.is_shooting and px.frame_count - self._shoot_frame >= 240 and px.rndi(1, 100) <= 1:
            bullet = Bullet(self.x + self.w // 2 - 1, self.y + self.h, -2, px.COLOR_YELLOW)
            self._bullets.append(bullet)
            self._shoot_frame = px.frame_count

    def draw(self):
        self.sprite.draw(self.x, self.y)

    def hit(self):
        self.health -= 1
        px.play(2, 2)

        if self.health <= 0:
            self.is_destroyed = True
            px.play(2, 1)
