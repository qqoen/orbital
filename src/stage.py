from src.common import print_center
import pyxel as px
from src.enemy import Enemy, BulletEmitter
from src.player import Player
from src.common import *
from src.blast import Blast
from src.data import ENEMIES


class Stage:
    def __init__(self, name, max_wave: int, player: Player):
        self.name = name
        self._max_wave = max_wave
        self.player = player
        self._wave = 0
        self._enemies = []
        self._enemy_bullets = []
        self._bonuses = []
        self._blasts = []
        self.score = 0
        self.chain_timer = Timer(60)
        self.chain_count = 0

    @property
    def current_wave(self):
        return self._wave

    @property
    def done(self):
        return self._wave > self._max_wave and len(self._enemies) == 0 and len(self._bonuses) == 0

    def update(self):
        for enemy in self._enemies:
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

        for bullet in self._enemy_bullets:
            if bullet.intersects(self.player):
                self._hit_player()
                bullet.is_destroyed = True
                break

        for bonus in self._bonuses:
            if bonus.intersects(self.player):
                bonus.pick()
                self._add_score(bonus.score)

        update_list(self._blasts)
        update_list(self._bonuses)
        self.player.update()
        update_list(self._enemies)
        update_list(self._enemy_bullets)

        self.chain_timer.update()

        if self.chain_timer.done:
            self.chain_count = 0

    def draw(self):
        draw_list(self._blasts)
        draw_list(self._bonuses)
        self.player.draw()
        draw_list(self._enemies)
        draw_list(self._enemy_bullets)

    def try_next_wave(self):
        if self._wave <= self._max_wave and len(self._enemies) == 0 and len(self._bonuses) == 0:
            self._wave += 1
            self._setup_wave()
            self.chain_timer.stop()
            self.chain_count = 0
            print(f"Wave: {self._wave}")
            return True

        return False

    def _hit_enemy(self, enemy):
        drops = enemy.hit()
        self._bonuses.extend(drops)

        if enemy.is_destroyed:
            self._blasts.append(Blast(enemy.x + enemy.w // 2, enemy.y + enemy.h // 2))
            self._add_score(enemy.score * max(1, self.chain_count))
            self.chain_timer.start()
            self.chain_count = min(5, self.chain_count + 1)

    def _setup_wave(self):
        pass

    def _spawn_row(self, x: int, y: int, count: int, enemy):
        for i in range(count):
            self._spawn(x + i * 16, y, enemy)

    def _spawn(self, x: int, y: int, enemy):
        emitter = BulletEmitter(self._enemy_bullets, enemy["shoot_cd"])
        self._enemies.append(Enemy(x, y, enemy, emitter))

    def _hit_player(self):
        self.player.hit()
        self.chain_timer.stop()
        self.chain_count = 0

    def _add_score(self, amount):
        self.score += amount


class Stage1(Stage):
    def __init__(self, player: Player):
        super().__init__("Stage 1", 6, player)

    def _setup_wave(self):
        match self._wave:
            case 1:
                self._spawn_row(16, 16, 10, ENEMIES["zako"])
                self._spawn_row(16, 32, 10, ENEMIES["zako"])
            case 2:
                self._spawn(16, 16, ENEMIES["shooter"])
                self._spawn_row(32, 16, 8, ENEMIES["zako"])
                self._spawn(32 + 8 * 16, 16, ENEMIES["shooter"])
                self._spawn_row(16, 32, 10, ENEMIES["zako"])
                self._spawn_row(32, 48, 8, ENEMIES["zako"])
            case 3:
                self._spawn_row(16, 16, 2, ENEMIES["shooter"])
                self._spawn_row(16 + 16 * 2, 16, 6, ENEMIES["zako"])
                self._spawn_row(16 + 16 * 8, 16, 2, ENEMIES["shooter"])
                self._spawn_row(16, 32, 10, ENEMIES["zako"])
                self._spawn_row(16, 48, 10, ENEMIES["shield"])
            case 4:
                self._spawn_row(16, 16, 2, ENEMIES["zako"])
                self._spawn_row(16 + 16 * 2, 16, 6, ENEMIES["shooter"])
                self._spawn_row(16 + 16 * 8, 16, 2, ENEMIES["zako"])
                self._spawn_row(16, 32, 10, ENEMIES["fast"])
                self._spawn_row(16, 48, 10, ENEMIES["fast"])
            case 5:
                self._spawn_row(16, 16, 2, ENEMIES["zako"])
                self._spawn_row(16 + 16 * 2, 16, 6, ENEMIES["shooter"])
                self._spawn_row(16 + 16 * 8, 16, 2, ENEMIES["zako"])
                self._spawn_row(16, 32, 10, ENEMIES["shield"])
                self._spawn_row(16, 48, 10, ENEMIES["fast"])
                self._spawn_row(16, 64, 10, ENEMIES["diver"])
            case 6:
                self._spawn(16, 32, ENEMIES["shooter"])
                self._spawn(48, 32, ENEMIES["boss"])
                self._spawn(80, 32, ENEMIES["shooter"])
                self._spawn_row(16, 48, 5, ENEMIES["shield"])