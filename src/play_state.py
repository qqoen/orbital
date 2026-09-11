import pyxel as px
from src.enemy import Enemy
from src.player import Player
from src.common import *


blue = Sprite(48, 0)
red = Sprite(32, 0)
yellow = Sprite(16, 0)


ENEMIES = [
    {
        "health": 1,
        "sprite": blue,
        "is_shooting": False,
        "score": 30,
    },
    {
        "health": 2,
        "sprite": red,
        "is_shooting": False,
        "score": 60,
    },
    {
        "health": 1,
        "sprite": yellow,
        "is_shooting": True,
        "score": 60,
    },
]


class PlayState(State):
    def __init__(self, app):
        self.app = app
        self.player = Player(px.width // 2, px.height - 16)
        self.enemies = []
        self.enemy_bullets = []
        self.victory_frames = -1
        self.score = 0
        self.wave = 0
        self.max_wave = 3

    def update(self):
        if len(self.enemies) == 0:
            self.wave += 1

            if self.wave <= self.max_wave:
                self._setup_wave()
            elif self.victory_frames == -1:
                self.victory_frames = px.frame_count
            elif px.frame_count - self.victory_frames >= 60:
                self.app.switch("end", {
                    "is_win": True,
                    "score": self.score * self.player.health,
                })
                px.play(1, 5)
                return

        self.player.update()

        for enemy in self.enemies:
            for bullet in self.player.bullets:
                if bullet.intersects(enemy):
                    bullet.is_destroyed = True
                    enemy.hit()

                    if enemy.is_destroyed:
                        self.score += enemy.score
                    break

            if enemy.is_destroyed:
                continue

        for bullet in self.enemy_bullets:
            if bullet.intersects(self.player):
                self.player.hit()
                bullet.is_destroyed = True
                break

        if self.player.is_destroyed:
            self.app.switch("end", {
                    "is_win": False,
                    "score": self.score,
                })
            px.play(1, 4)
            return

        update_list(self.enemies)
        update_list(self.enemy_bullets)

    def draw(self):
        print_center(0, f"SCORE: {self.score}", px.COLOR_WHITE, self.app.font)
        px.text(0, 0, "@" * self.player.health, px.COLOR_WHITE, self.app.font)
        self.player.draw()
        draw_list(self.enemies)
        draw_list(self.enemy_bullets)

    def _setup_wave(self):
        match self.wave:
            case 1:
                for i in range(10):
                    self.enemies.append(Enemy(16 + i * 16, 16, self.enemy_bullets, ENEMIES[0]))
            case 2:
                for i in range(10):
                    self.enemies.append(Enemy(16 + i * 16, 16, self.enemy_bullets, ENEMIES[1]))
                    self.enemies.append(Enemy(16 + i * 16, 32, self.enemy_bullets, ENEMIES[0]))
            case 3:
                for i in range(10):
                    self.enemies.append(Enemy(16 + i * 16, 16, self.enemy_bullets, ENEMIES[2]))
                    self.enemies.append(Enemy(16 + i * 16, 32, self.enemy_bullets, ENEMIES[0]))
                    self.enemies.append(Enemy(16 + i * 16, 48, self.enemy_bullets, ENEMIES[1]))
