import pyxel as px


class Background:
    def __init__(self, direction=1):
        self.direction = direction
        self.stars = []

        for i in range(100):
            self.stars.append((px.rndi(0, px.width - 1), px.rndi(0, px.height - 1), px.rndf(1, 2.5)))

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed * self.direction

            if self.direction > 0 and y >= px.height:
                y -= px.height

            if self.direction < 0 and y < 0:
                y += px.height

            self.stars[i] = (x, y, speed)

    def draw(self):
        for x, y, speed in self.stars:
            px.pset(x, y, px.COLOR_LIGHT_BLUE if speed > 1.8 else px.COLOR_DARK_BLUE)
