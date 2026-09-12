import pyxel as px
from src.enemy import Enemy
from src.player import Player
from src.common import *
from src.background import Background
from src.bonus import Bonus
from src.blast import Blast


yellow = Sprite(16, 0)
red = Sprite(32, 0)
blue = Sprite(48, 0)
green = Sprite(64, 0)


ENEMIES = [
    {
        "health": 1,
        "sprite": blue,
        "is_shooting": False,
        "score": 10,
        "xspeed": 1,
        "yspeed": 0,
    },
    {
        "health": 2,
        "sprite": red,
        "is_shooting": False,
        "score": 20,
        "xspeed": 1,
        "yspeed": 0,
    },
    {
        "health": 1,
        "sprite": yellow,
        "is_shooting": True,
        "score": 20,
        "xspeed": 1,
        "yspeed": 0,
    },
    {
        "health": 1,
        "sprite": green,
        "is_shooting": False,
        "score": 15,
        "xspeed": 2,
        "yspeed": 0,
    },
    {
        "health": 1,
        "sprite": green,
        "is_shooting": False,
        "score": 15,
        "xspeed": 1,
        "yspeed": 1,
    },
]


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
        self.chain_timer = Timer(60)
        self.chain_count = 0
        self._bg = Background()

    def update(self):
        self._bg.update()

        if len(self.enemies) == 0:
            self.wave += 1
            self.chain_timer.stop()
            self.chain_count = 0

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
                self._hit_player()
                self._hit_enemy(enemy)

            if enemy.is_destroyed:
                continue

        for bullet in self.enemy_bullets:
            if bullet.intersects(self.player):
                self._hit_player()
                bullet.is_destroyed = True
                break

        for bonus in self.bonuses:
            if bonus.intersects(self.player):
                bonus.pick()
                self._add_score(bonus.score)

        if self.player.is_destroyed:
            self.app.switch("end", is_win=False, score=self.score)
            px.play(1, 4)
            return

        update_list(self.enemies)
        update_list(self.enemy_bullets)
        update_list(self.bonuses)
        update_list(self.blasts)
        self.chain_timer.update()

        if self.chain_timer.done:
            self.chain_count = 0

    def _hit_player(self):
        self.player.hit()
        self.chain_timer.stop()
        self.chain_count = 0

    def _hit_enemy(self, enemy):
        enemy.hit()

        if enemy.is_destroyed:
            self._add_score(enemy.score * max(1, self.chain_count))
            self.blasts.append(Blast(enemy.x + enemy.w // 2, enemy.y + enemy.h // 2))

            if px.rndi(1, 100) <= 25:
                self.bonuses.append(Bonus(enemy.x + enemy.w // 2 - 3, enemy.y + enemy.h // 2, enemy.score))

            self.chain_timer.start()
            self.chain_count = min(5, self.chain_count + 1)

    def _add_score(self, amount):
        self.score += amount

    def draw(self):
        px.cls(px.COLOR_BLACK)
        self._bg.draw()

        s_text = f"SCORE: {self.score:5}"
        s_width = self.app.font.text_width(s_text)
        print_center(0, s_text, px.COLOR_WHITE, self.app.font)

        if not self.chain_timer.done and self.chain_count > 1:
            ratio = self.chain_timer.left / self.chain_timer.max
            line_w = s_width * ratio
            hline(px.width // 2 - s_width // 2, 10, line_w)
            px.text(px.width // 2 + s_width // 2 + 2, 8, f"x{self.chain_count}", px.COLOR_WHITE)

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
