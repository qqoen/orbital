import pyxel as px
from src.common import *
from src.start_state import StartState
from src.play_state import PlayState
from src.end_state import EndState


class PlayerData:
    def __init__(self):
        self._highscore = 0

    @property
    def highscore(self):
        return self._highscore

    def update_score(self, new_score):
        self._highscore = max(self._highscore, new_score)


class App(StateMachine):
    def __init__(self):
        super().__init__()
        px.init(300, 200, "Orbital", 60, px.KEY_ESCAPE, 2)
        px.load("assets/resources.pyxres")

        assets = {
            "font": px.Font("assets/umplus_j10r.bdf"),
        }

        player_data = PlayerData()

        self.register("start", lambda _: StartState(self, assets, player_data))
        self.register("play", lambda _: PlayState(self, assets, player_data))
        self.register("end", lambda pl: EndState(self, assets, player_data, pl["is_win"], pl["score"]))
        self.switch("start")
    
        px.run(self.update, self.draw)


if __name__ == "__main__":
    app = App()
