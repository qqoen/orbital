import pyxel as px
from src.common import *
from src.start_state import StartState
from src.play_state import PlayState
from src.end_state import EndState


class App:
    def __init__(self):
        px.init(300, 200, "Orbital", 60, px.KEY_ESCAPE, 2)
        px.load("assets/resources.pyxres")
        self.font = px.Font("assets/umplus_j10r.bdf")
        self._state: State = StartState(self)
        px.run(self.update, self.draw)

    def update(self):
        self._state.update()

    def draw(self):
        px.cls(px.COLOR_BLACK)
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
