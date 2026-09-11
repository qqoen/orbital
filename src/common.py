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


class Sprite:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def draw(self, x, y):
        px.blt(x, y, 0, self.u, self.v, 16, 16, px.COLOR_BLACK)
