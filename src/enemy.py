import pyxel as px
from src.common import *
from src.bullet import Bullet


class Enemy(Rect):
    def __init__(self, x, y, bullets, enemy_type):
        super().__init__(x, y, 16, 16)
        self._bullets = bullets
        self._health = enemy_type["health"]
        self._sprite = enemy_type["sprite"]
        self._is_shooting = enemy_type["is_shooting"]
        self.score = enemy_type["score"]
        self._xspeed = enemy_type["xspeed"]
        self._yspeed = enemy_type["yspeed"]

        self._xdir = 1
        self._start_x = x
        self._shoot_frame = -200

        self.is_destroyed = False

    def update(self):
        if px.frame_count % 2 == 0:
            self.x += self._xspeed * self._xdir

        if self.x - self._start_x >= 112:
            self._xdir = -1
        elif self.x < self._start_x:
            self._xdir = 1

        self.y += self._yspeed

        if self._is_shooting and px.frame_count - self._shoot_frame >= 240 and px.rndi(1, 100) <= 1:
            bullet = Bullet(self.x + self.w // 2 - 1, self.y + self.h, -2, px.COLOR_YELLOW)
            self._bullets.append(bullet)
            self._shoot_frame = px.frame_count

        if self.y >= px.height:
            self.is_destroyed = True

    def draw(self):
        self._sprite.draw(self.x, self.y)

    def hit(self):
        self._health -= 1

        if self._health <= 0:
            self.is_destroyed = True
            px.play(2, 1)
        else:
            px.play(2, 2)
