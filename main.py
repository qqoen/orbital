import pyxel as px


def update_list(objects):
    for obj in objects:
        obj.update()
        if obj.is_destroyed:
            objects.remove(obj)


def draw_list(objects):
    for obj in objects:
        obj.draw()


def print_center(y, text, color, font):
    width = font.text_width(text)
    px.text(px.width // 2 - width // 2, y, text, color, font)


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def intersects(self, other):
        a = self.x + self.w > other.x and self.y + self.h > other.y
        b = other.x + other.w > self.x and other.y + other.h > self.y
        return a and b


class Bullet(Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 2, 8)
        self.speed = 3
        self.is_destroyed = False

    def update(self):
        self.y -= self.speed

        if self.y <= 0:
            self.is_destroyed = True

    def draw(self):
        px.rect(self.x, self.y, self.w, self.h, px.COLOR_WHITE)


class Enemy(Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.speed = 1
        self.is_destroyed = False
        self.start_x = x

    def update(self):
        if px.frame_count % 2 == 0:
            self.x += self.speed

        if self.x - self.start_x >= 112:
            self.speed = -1

        if self.x < self.start_x:
            self.speed = 1

    def draw(self):
        px.blt(self.x, self.y, 0, 16, 0, 16, 16, px.COLOR_BLACK)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.speed = 2
        self.bullets = []

    def update(self):
        if px.btn(px.KEY_LEFT):
            self.x -= self.speed
        elif px.btn(px.KEY_RIGHT):
            self.x += self.speed

        if px.btnp(px.KEY_SPACE):
            bullet = Bullet(self.x + self.w // 2 - 1, self.y)
            self.bullets.append(bullet)
            px.play(0, 0)

        self.x = px.clamp(self.x, 0, px.width - self.w)
        update_list(self.bullets)

    def draw(self):
        px.blt(self.x, self.y, 0, 0, 0, 16, 16, px.COLOR_BLACK)
        draw_list(self.bullets)


class App:
    BOOT = 0
    START = 1
    PLAY = 2
    WIN = 3

    def __init__(self):
        px.init(300, 200, "Orbital", 60, px.KEY_ESCAPE, 2)
        px.load("resources.pyxres")

        self.player = Player(px.width // 2, px.height - 16)
        self.font = px.Font("umplus_j10r.bdf")
        self.state = App.BOOT
        self.enemies = []
        self.victory_frames = -1

        px.run(self.update, self.draw)

    def update(self):
        if self.state == App.BOOT:
            px.play(1, 6, loop=True)
            self.state = App.START
        elif self.state == App.START:
            if px.btnp(px.KEY_RETURN):
                self.state = App.PLAY
                px.play(1, 3)

                for i in range(10):
                    self.enemies.append(Enemy(16 + i * 16, 16))
                    self.enemies.append(Enemy(16 + i * 16, 32))
        elif self.state == App.WIN:
            if px.btnp(px.KEY_RETURN):
                self.state = App.BOOT
        else:
            self.player.update()

            for bullet in self.player.bullets:
                for enemy in self.enemies:
                    if bullet.intersects(enemy):
                        bullet.is_destroyed = True
                        enemy.is_destroyed = True
                        px.play(2, 1)
                        break
                
                if bullet.is_destroyed:
                    continue

            update_list(self.enemies)

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
            print_center(px.height // 2 - 10, "Victory!", px.COLOR_YELLOW, self.font)
            print_center(px.height // 2 + 10, "Press 'Enter' to continue", px.COLOR_GRAY, self.font)
        elif self.state == App.PLAY:
            self.player.draw()
            draw_list(self.enemies)


if __name__ == "__main__":
    app = App()
