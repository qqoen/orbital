import pyxel as px
from src.common import *
from src.start_state import StartState
from src.play_state import PlayState
from src.end_state import EndState


class App(StateMachine):
    def __init__(self):
        super().__init__()
        px.init(300, 200, "Orbital", 60, px.KEY_ESCAPE, 2)
        px.load("assets/resources.pyxres")
        
        self.font = px.Font("assets/umplus_j10r.bdf")

        self.highscore = 0

        self.register("start", lambda _: StartState(self))
        self.register("play", lambda _: PlayState(self))
        self.register("end", lambda pl: EndState(self, pl["is_win"], pl["score"]))
        self.switch("start")
    
        px.run(self.update, self.draw)


if __name__ == "__main__":
    app = App()
