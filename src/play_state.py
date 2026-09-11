from src.common import draw_list
import pyxel as px
from src.enemy import Enemy
from src.player import Player
from src.common import *


yellow = Sprite(16, 0)
red = Sprite(32, 0)
blue = Sprite(48, 0)
green = Sprite(64, 0)


ENEMIES = [
    {
        "health": 1,
        "sprite": blue,
        "is_shooting": False,
        "score": 30,
        "xspeed": 1,
        "yspeed": 0,
    },
    {
        "health": 2,
        "sprite": red,
        "is_shooting": False,
        "score": 60,
        "xspeed": 1,
        "yspeed": 0,
    },
    {
        "health": 1,
        "sprite": yellow,
        "is_shooting": True,
        "score": 60,
        "xspeed": 1,
        "yspeed": 0,
    },
    {
        "health": 1,
        "sprite": green,
        "is_shooting": False,
        "score": 40,
        "xspeed": 2,
        "yspeed": 0,
    },
    {
        "health": 1,
        "sprite": green,
        "is_shooting": False,
        "score": 40,
        "xspeed": 1,
        "yspeed": 1,
    },
]


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
        px.text(self.x + 2, self.y + 1, "T", px.COLOR_WHITE)

    def pick(self):
        px.play(1, 3)
        self.is_destroyed = True


class Blast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1
        self.max_radius = 8
        self.is_destroyed = False

    def update(self):
        self.radius += 1
        if self.radius > self.max_radius:
            self.is_destroyed = True

    def draw(self):
        px.circ(self.x, self.y, self.radius, px.COLOR_YELLOW)
        px.circb(self.x, self.y, self.radius, px.COLOR_RED)


class PlayState(State):
    def __init__(self, app):
        self.app = app
        self.player = Player(px.width // 2, px.height - 16)
        self.enemies = []
        self.enemy_bullets = []
        self.bonuses = []
        self.blasts = []
        self.victory_frames = -1
        self.score = 0
        self.wave = 0
        self.max_wave = 5

    def update(self):
        if len(self.enemies) == 0:
            self.wave += 1

            if self.wave <= self.max_wave:
                self._setup_wave()
            elif self.victory_frames == -1:
                self.victory_frames = px.frame_count
            elif px.frame_count - self.victory_frames >= 60:
                self.app.switch("end", is_win=True, score=self.score * self.player.health)
                px.play(1, 5)
                return

        self.player.update()

        for enemy in self.enemies:
            for bullet in self.player.bullets:
                if bullet.intersects(enemy):
                    bullet.is_destroyed = True
                    self._hit_enemy(enemy)
                    break

            if enemy.intersects(self.player):
                self.player.hit()
                self._hit_enemy(enemy)

            if enemy.is_destroyed:
                continue

        for bullet in self.enemy_bullets:
            if bullet.intersects(self.player):
                self.player.hit()
                bullet.is_destroyed = True
                break

        for bonus in self.bonuses:
            if bonus.intersects(self.player):
                bonus.pick()
                self.score += bonus.score

        if self.player.is_destroyed:
            self.app.switch("end", is_win=False, score=self.score)
            px.play(1, 4)
            return

        update_list(self.enemies)
        update_list(self.enemy_bullets)
        update_list(self.bonuses)
        update_list(self.blasts)

    def _hit_enemy(self, enemy):
        enemy.hit()

        if enemy.is_destroyed:
            self.score += enemy.score
            self.blasts.append(Blast(enemy.x + enemy.w // 2, enemy.y + enemy.h // 2))

            if px.rndi(1, 100) <= 25:
                self.bonuses.append(Bonus(enemy.x + enemy.w // 2 - 3, enemy.y + enemy.h // 2, enemy.score))

    def draw(self):
        print_center(0, f"SCORE: {self.score:5}", px.COLOR_WHITE, self.app.font)
        
        hs_text = f"HIGH: {self.app.highscore:5}"
        hs_width = self.app.font.text_width(hs_text)
        px.text(px.width - hs_width, 0, hs_text, px.COLOR_WHITE, self.app.font)
        
        px.text(0, 0, "@" * self.player.health, px.COLOR_WHITE, self.app.font)
        self.player.draw()
        draw_list(self.enemies)
        draw_list(self.enemy_bullets)
        draw_list(self.bonuses)
        draw_list(self.blasts)

    def _setup_wave(self):
        match self.wave:
            case 1:
                for i in range(10):
                    self.enemies.append(Enemy(16 + i * 16, 16, self.enemy_bullets, ENEMIES[0]))
                    self.enemies.append(Enemy(16 + i * 16, 32, self.enemy_bullets, ENEMIES[0]))
            case 2:
                for i in range(10):
                    self.enemies.append(Enemy(16 + i * 16, 16, self.enemy_bullets, ENEMIES[0]))
                    self.enemies.append(Enemy(16 + i * 16, 32, self.enemy_bullets, ENEMIES[3]))
                    self.enemies.append(Enemy(16 + i * 16, 48, self.enemy_bullets, ENEMIES[0]))
            case 3:
                for i in range(8):
                    self.enemies.append(Enemy(16 + i * 16, 16, self.enemy_bullets, ENEMIES[3]))
                    self.enemies.append(Enemy(16 + i * 16, 32, self.enemy_bullets, ENEMIES[0]))
                    self.enemies.append(Enemy(16 + i * 16, 48, self.enemy_bullets, ENEMIES[3]))
                    self.enemies.append(Enemy(16 + i * 16, 64, self.enemy_bullets, ENEMIES[1]))
            case 4:
                for i in range(8):
                    self.enemies.append(Enemy(16 + i * 16, 16, self.enemy_bullets, ENEMIES[2]))
                    self.enemies.append(Enemy(16 + i * 16, 32, self.enemy_bullets, ENEMIES[0]))
                    self.enemies.append(Enemy(16 + i * 16, 48, self.enemy_bullets, ENEMIES[1]))
            case 5:
                for i in range(10):
                    self.enemies.append(Enemy(16 + i * 16, 16, self.enemy_bullets, ENEMIES[2]))
                    self.enemies.append(Enemy(16 + i * 16, 32, self.enemy_bullets, ENEMIES[0]))
                    self.enemies.append(Enemy(16 + i * 16, 48, self.enemy_bullets, ENEMIES[3]))
                    self.enemies.append(Enemy(16 + i * 16, 64, self.enemy_bullets, ENEMIES[4]))
