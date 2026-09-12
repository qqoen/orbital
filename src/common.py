import pyxel as px
from abc import ABC, abstractmethod


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


def hline(x, y, width):
    px.line(x, y, x + width, y, px.COLOR_WHITE)


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


class State(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass


class Timer:
    def __init__(self, max_ticks):
        self._max_ticks = max_ticks
        self._ticks = 0

    @property
    def done(self):
        return self._ticks == 0

    @property
    def max(self):
        return self._max_ticks

    @property
    def left(self):
        return self._ticks

    def start(self):
        self._ticks = self._max_ticks

    def stop(self):
        self._ticks = 0

    def update(self):
        self._ticks = max(0, self._ticks - 1)
