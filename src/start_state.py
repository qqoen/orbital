import pyxel as px
from src.common import *
from src.background import Background


class StartState(State):
    def __init__(self, sm, assets, player_data):
        self._sm = sm
        self._font = assets["font"]
        self._highscore = player_data.highscore
        self._bg = Background(-1)

        px.play(1, 6, loop=True)

    def update(self):
        self._bg.update()

        if px.btnp(px.KEY_RETURN):
            self._sm.switch("play")
            px.play(1, 3)

    def draw(self):
        px.cls(px.COLOR_BLACK)
        self._bg.draw()

        print_center(32, "O R B I T A L", px.frame_count % len(px.colors), self._font)

        if self._highscore > 0:
            print_center(64, f"Highscore: {self._highscore}", px.COLOR_YELLOW, self._font)

        print_center(px.height // 2 - 10, "Press Enter to start", px.COLOR_WHITE, self._font)
        px.text(64, px.height // 2 + 10, "Press Space to shot", px.COLOR_GRAY, self._font)
        px.text(64, px.height // 2 + 20, "Left or Right to move", px.COLOR_GRAY, self._font)
        px.text(64, px.height // 2 + 30, "or Escape to exit", px.COLOR_GRAY, self._font)
        print_center(px.height - 32, "2026", px.COLOR_YELLOW, self._font)
