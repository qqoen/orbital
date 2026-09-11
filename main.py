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


class App:
    BOOT = 0
    START = 1
    PLAY = 2
    WIN = 3
    LOOSE = 4

    def __init__(self):
        px.init(300, 200, "Orbital", 60, px.KEY_ESCAPE, 2)
        px.load("assets/resources.pyxres")
        self.font = px.Font("assets/umplus_j10r.bdf")

        self.state = App.BOOT
        self.player = Player(0, 0)
        self.enemies = []
        self.enemy_bullets = []
        self.victory_frames = -1
        self.score = 0

        px.run(self.update, self.draw)

    def update(self):
        if self.state == App.BOOT:
            px.play(1, 6, loop=True)
            self.state = App.START
        elif self.state == App.START:
            if px.btnp(px.KEY_RETURN):
                self.state = App.PLAY
                px.play(1, 3)

                self.player = Player(px.width // 2, px.height - self.player.h)
                self.enemies.clear()
                self.enemy_bullets.clear()
                self.victory_frames = -1
                self.score = 0

                for i in range(10):
                    self.enemies.append(Enemy(16 + i * 16, 16, self.enemy_bullets, ENEMIES[2]))
                    self.enemies.append(Enemy(16 + i * 16, 32, self.enemy_bullets, ENEMIES[0]))
                    self.enemies.append(Enemy(16 + i * 16, 48, self.enemy_bullets, ENEMIES[1]))
        elif self.state == App.WIN or self.state == App.LOOSE:
            if px.btnp(px.KEY_RETURN):
                self.state = App.BOOT
        else:
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
                    self.state = App.LOOSE
                    px.play(1, 4)
                    return

            update_list(self.enemies)
            update_list(self.enemy_bullets)

            if len(self.enemies) == 0:
                if self.victory_frames == -1:
                    self.victory_frames = px.frame_count
                elif px.frame_count - self.victory_frames >= 60:
                    self.state = App.WIN
                    px.play(1, 5)

    def draw(self):
        px.cls(px.COLOR_BLACK)

        if self.state == App.BOOT:
            pass
        elif self.state == App.START:
            print_center(32, "O R B I T A L", px.COLOR_LIGHT_BLUE, self.font)

            print_center(px.height // 2 - 10, "Press 'Enter' to start", px.COLOR_WHITE, self.font)

            px.text(64, px.height // 2 + 10, "Press Space to shot", px.COLOR_GRAY, self.font)
            px.text(64, px.height // 2 + 20, "Left or Right to move", px.COLOR_GRAY, self.font)
            px.text(64, px.height // 2 + 30, "or Escape to exit", px.COLOR_GRAY, self.font)

            print_center(px.height - 32, "2026", px.COLOR_YELLOW, self.font)
        elif self.state == App.WIN:
            print_center(px.height // 2 - 20, "Victory!", px.COLOR_YELLOW, self.font)
            print_center(px.height // 2 - 10, f"SCORE: {self.score}", px.COLOR_WHITE, self.font)
            print_center(px.height // 2 + 10, "Press 'Enter' to continue", px.COLOR_GRAY, self.font)
        elif self.state == App.LOOSE:
            print_center(px.height // 2 - 20, "GAME OVER", px.COLOR_RED, self.font)
            print_center(px.height // 2 - 10, f"SCORE: {self.score}", px.COLOR_WHITE, self.font)
            print_center(px.height // 2 + 10, "Press 'Enter' to continue", px.COLOR_GRAY, self.font)
        elif self.state == App.PLAY:
            print_center(0, f"SCORE: {self.score}", px.COLOR_WHITE, self.font)

            self.player.draw()
            draw_list(self.enemies)
            draw_list(self.enemy_bullets)


if __name__ == "__main__":
    app = App()
