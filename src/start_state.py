import pyxel as px
from src.common import *


class StartState(State):
    def __init__(self, app):
        self.app = app
        self.is_music_playing = False

    def update(self):
        if not self.is_music_playing:
            px.play(1, 6, loop=True)
            self.is_music_playing = True

        if px.btnp(px.KEY_RETURN):
            self.app.switch("play")
            px.play(1, 3)

    def draw(self):
        print_center(32, "O R B I T A L", px.COLOR_LIGHT_BLUE, self.app.font)
        print_center(px.height // 2 - 10, "Press 'Enter' to start", px.COLOR_WHITE, self.app.font)
        px.text(64, px.height // 2 + 10, "Press Space to shot", px.COLOR_GRAY, self.app.font)
        px.text(64, px.height // 2 + 20, "Left or Right to move", px.COLOR_GRAY, self.app.font)
        px.text(64, px.height // 2 + 30, "or Escape to exit", px.COLOR_GRAY, self.app.font)
        print_center(px.height - 32, "2026", px.COLOR_YELLOW, self.app.font)
