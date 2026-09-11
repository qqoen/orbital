import pyxel as px
from src.common import *
from src.start_state import StartState
from src.play_state import PlayState
from src.end_state import EndState


class Background:
    def __init__(self):
        self.stars = []
        for i in range(100):
            self.stars.append((px.rndi(0, px.width - 1), px.rndi(0, px.height - 1), px.rndf(1, 2.5)))

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed

            if y >= px.height:
                y -= px.height
            
            self.stars[i] = (x, y, speed)

    def draw(self):
        for x, y, speed in self.stars:
            px.pset(x, y, px.COLOR_LIGHT_BLUE if speed > 1.8 else px.COLOR_DARK_BLUE)


class App:
    def __init__(self):
        px.init(300, 200, "Orbital", 60, px.KEY_ESCAPE, 2)
        px.load("assets/resources.pyxres")
        self.font = px.Font("assets/umplus_j10r.bdf")
        self._state: State = StartState(self)
        self._bg = Background()
        px.run(self.update, self.draw)

    def update(self):
        self._bg.update()
        self._state.update()

    def draw(self):
        px.cls(px.COLOR_BLACK)
        self._bg.draw()
        self._state.draw()

    def switch(self, state, **payload):
        match state:
            case "start":
                self._state = StartState(self)
            case "play":
                self._state = PlayState(self)
            case "end":
                self._state = EndState(self, payload["is_win"], payload["score"])
            case _: raise ValueError(f"Unknown state: {state}")


if __name__ == "__main__":
    app = App()
