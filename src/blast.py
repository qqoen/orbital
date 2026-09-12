import pyxel as px


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
