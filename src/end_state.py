import pyxel as px
from src.common import *


class EndState(State):
    def __init__(self, sm, assets, player_data, is_win, score):
        self._sm = sm
        self._font = assets["font"]
        self._player_data = player_data
        self._is_win = is_win
        self._score = score

    def update(self):
        if px.btnp(px.KEY_RETURN):
            self._player_data.update_score(self._score)
            self._sm.switch("start")

    def draw(self):
        px.cls(px.COLOR_BLACK)

        if self._is_win:
            print_center(px.height // 2 - 20, "Victory!", px.COLOR_YELLOW, self._font)
            print_center(px.height // 2 - 10, f"Final score: {self._score}", px.COLOR_WHITE, self._font)
            print_center(px.height // 2 + 10, "Press Enter to continue", px.COLOR_GRAY, self._font)
        else:
            print_center(px.height // 2 - 20, "GAME OVER", px.COLOR_RED, self._font)
            print_center(px.height // 2 - 10, f"Final score: {self._score}", px.COLOR_WHITE, self._font)
            print_center(px.height // 2 + 10, "Press Enter to continue", px.COLOR_GRAY, self._font)
