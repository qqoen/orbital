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
        self._score = enemy_type["score"]
        self._xspeed = enemy_type["xspeed"]
        self._yspeed = enemy_type["yspeed"]

        self._xdir = 1
        self._start_x = x
        self._shoot_cooldown = Timer(120)
        self._approach_timer = Timer(px.rndi(250, 2000)) 
        self._approach_timer.start()

        self.is_destroyed = False

    @property
    def score(self):
        if self._approach_timer.done:
            return self._score * 2

        return self._score

    def update(self):
        if px.frame_count % 2 == 0:
            self.x += self._xspeed * self._xdir

        if self.x - self._start_x >= 112:
            self._xdir = -1
        elif self.x < self._start_x:
            self._xdir = 1

        if px.frame_count % 2 == 0:
            self.y += self._yspeed

        if self._is_shooting and self._shoot_cooldown.done and px.rndf(1, 100) < 1.5:
            bullet = Bullet(self.x + self.w // 2 - 1, self.y + self.h, -2, px.COLOR_YELLOW)
            self._bullets.append(bullet)
            self._shoot_cooldown.start()

        if self._yspeed == 0 and self._approach_timer.done:
            self._yspeed = 1

        if self.y >= px.height:
            self.is_destroyed = True

        self._shoot_cooldown.update()
        self._approach_timer.update()

    def draw(self):
        self._sprite.draw(self.x, self.y)

    def hit(self):
        self._health -= 1

        if self._health <= 0:
            self.is_destroyed = True
            px.play(2, 1)
        else:
            px.play(2, 2)
