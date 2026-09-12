import pyxel as px
from src.enemy import Enemy, BulletEmitter
from src.player import Player
from src.common import *
from src.background import Background
from src.blast import Blast
from src.data import ENEMIES


class PlayState(State):
    def __init__(self, sm, assets, player_data):
        self._sm = sm
        self._font = assets["font"]
        self._highscore = player_data.highscore
        self.player = Player(px.width // 2, px.height - 16)
        self.enemies = []
        self.enemy_bullets = []
        self.bonuses = []
        self.blasts = []
        self.victory_frames = -1
        self.score = 0
        self.wave = 0
        self.max_wave = 6
        self.chain_timer = Timer(60)
        self.chain_count = 0
        self._bg = Background()

    def update(self):
        self._bg.update()

        if len(self.enemies) == 0 and len(self.bonuses) == 0:
            self.wave += 1
            self.chain_timer.stop()
            self.chain_count = 0

            if self.wave <= self.max_wave:
                self._setup_wave()
            elif self.victory_frames == -1:
                self.victory_frames = px.frame_count
            elif px.frame_count - self.victory_frames >= 60:
                self._sm.switch("end", is_win=True, score=self.score * self.player.health)
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
            self._sm.switch("end", is_win=False, score=self.score)
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
        drops = enemy.hit()
        self.bonuses.extend(drops)

        if enemy.is_destroyed:
            self._add_score(enemy.score * max(1, self.chain_count))
            self.blasts.append(Blast(enemy.x + enemy.w // 2, enemy.y + enemy.h // 2))
            self.chain_timer.start()
            self.chain_count = min(5, self.chain_count + 1)

    def _add_score(self, amount):
        self.score += amount

    def draw(self):
        px.cls(px.COLOR_BLACK)
        self._bg.draw()

        s_text = f"SCORE: {self.score:5}"
        s_width = self._font.text_width(s_text)
        print_center(0, s_text, px.COLOR_WHITE, self._font)

        if not self.chain_timer.done and self.chain_count > 1:
            ratio = self.chain_timer.left / self.chain_timer.max
            line_w = s_width * ratio
            hline(px.width // 2 - s_width // 2, 10, line_w)
            px.text(px.width // 2 + s_width // 2 + 2, 8, f"x{self.chain_count}", px.COLOR_WHITE)

        hs_text = f"HIGH: {self._highscore:5}"
        hs_width = self._font.text_width(hs_text)
        px.text(px.width - hs_width, 0, hs_text, px.COLOR_WHITE, self._font)
        
        px.text(0, 0, "@" * self.player.health, px.COLOR_WHITE, self._font)

        if self.wave <= self.max_wave:
            px.text(30, 0, f"WAVE: {self.wave}", px.COLOR_WHITE, self._font)

        self.player.draw()
        draw_list(self.enemies)
        draw_list(self.enemy_bullets)
        draw_list(self.bonuses)
        draw_list(self.blasts)

    def _setup_wave(self):
        match self.wave:
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

    def _spawn_row(self, x, y, count, enemy):
        for i in range(count):
            self._spawn(x + i * 16, y, enemy)
            
    def _spawn(self, x, y, enemy):
        emitter = BulletEmitter(self.enemy_bullets, enemy["shoot_cd"])
        self.enemies.append(Enemy(x, y, enemy, emitter))
