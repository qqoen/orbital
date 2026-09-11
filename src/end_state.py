import pyxel as px
from src.common import *


class EndState(State):
    def __init__(self, app, is_win, score):
        self.app = app
        self.is_win = is_win
        self.score = score

    def update(self):
        if px.btnp(px.KEY_RETURN):
            self.app.highscore = max(self.app.highscore, self.score)
            self.app.switch("start")

    def draw(self):
        if self.is_win:
            print_center(px.height // 2 - 20, "Victory!", px.COLOR_YELLOW, self.app.font)
            print_center(px.height // 2 - 10, f"Final score: {self.score}", px.COLOR_WHITE, self.app.font)
            print_center(px.height // 2 + 10, "Press 'Enter' to continue", px.COLOR_GRAY, self.app.font)
        else:
            print_center(px.height // 2 - 20, "GAME OVER", px.COLOR_RED, self.app.font)
            print_center(px.height // 2 - 10, f"Final score: {self.score}", px.COLOR_WHITE, self.app.font)
            print_center(px.height // 2 + 10, "Press 'Enter' to continue", px.COLOR_GRAY, self.app.font)