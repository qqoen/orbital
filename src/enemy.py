import pyxel as px
from src.common import *
from src.bullet import Bullet
from src.bonus import Bonus


class BulletEmitter:
    def __init__(self, bullets, cooldown):
        self._bullets = bullets
        self._shoot_cooldown = Timer(cooldown)
        self._is_shooting = cooldown > 0

    def update(self, x, y):
        if self._is_shooting and self._shoot_cooldown.done:
            bullet = Bullet(x, y, -2, px.COLOR_YELLOW)
            self._bullets.append(bullet)
            self._shoot_cooldown.start()

        self._shoot_cooldown.update()


class Enemy(Rect):
    def __init__(self, x, y, enemy_type, emitter):
        super().__init__(x, y, 16, 16)
        self._spawn_x = x
        self._spawn_y = y
        self.x = x
        self.y = y - 32
    
        self._health = enemy_type["health"]
        self._sprite = enemy_type["sprite"]
        self._score = enemy_type["score"]
        self._xspeed = enemy_type["xspeed"]
        self._yspeed = enemy_type["yspeed"]
        self._can_approach = enemy_type["can_approach"]
        self._bonus_chance = enemy_type["bonus_chance"]
        self._emitter = emitter

        self._xdir = 1
        self._start_x = x
        self._approach_timer = Timer(px.rndi(250, 2000)) 
        self._approach_timer.start()
        self._is_spawned = False

        self.is_destroyed = False

    @property
    def score(self):
        if self._can_approach and self._approach_timer.done:
            return self._score * 2

        return self._score

    def update(self):
        # spawn phase
        if not self._is_spawned:
            self.x = approach(self.x, self._spawn_x)
            self.y = approach(self.y, self._spawn_y)
            if self.x == self._spawn_x and self.y == self._spawn_y:
                self._is_spawned = True
            return
        self._is_spawned = True

        if px.frame_count % 2 == 0:
            self.x += self._xspeed * self._xdir

        if self.x - self._start_x >= 112:
            self._xdir = -1
        elif self.x < self._start_x:
            self._xdir = 1

        if px.frame_count % 2 == 0:
            self.y += self._yspeed

        self._emitter.update(self.x + self.w // 2 - 1, self.y + self.h)

        if self._can_approach and self._approach_timer.done:
            self._yspeed = 1

        if self.y >= px.height:
            self.is_destroyed = True

        self._approach_timer.update()

    def draw(self):
        self._sprite.draw(self.x, self.y)

    def hit(self):
        self._health -= 1
        drops = []

        if self._health <= 0:
            self.is_destroyed = True
            px.play(2, 1)

            if px.rndi(1, 100) <= self._bonus_chance:
                drops.append(Bonus(self.x + self.w // 2 - 3, self.y + self.h // 2, self._score))
        else:
            px.play(2, 2)

        return drops

