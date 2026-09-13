import pyxel as px
from src.player import Player
from src.common import *
from src.background import Background
from src.stages import Stage1, Stage2


class PlayState(State):
    def __init__(self, sm, assets, player_data):
        self._sm = sm
        self._font = assets["font"]
        self._highscore = player_data.highscore

        player = Player(px.width // 2, px.height - 16)
        self._stages = [
            Stage1(player),
            Stage2(player),
        ]
        self._stage = self._stages.pop(0)

        self.victory_frames = -1
        self._bg = Background()

        self._start_timer = Timer(90)
        self._start_timer.start()

    def update(self):
        self._bg.update()

        self._stage.update()

        if self._start_timer.done:
            self._stage.try_next_wave()

        if self._stage.done:
            if len(self._stages) > 0:
                self._stage = self._stages.pop(0)
                self._start_timer.start()
                return

            if self.victory_frames == -1:
                self.victory_frames = px.frame_count
            elif px.frame_count - self.victory_frames >= 60:
                self._sm.switch("end", is_win=True, score=self._stage.score * self._stage.player.health)
                px.play(1, 5)
                return

        if self._stage.player.is_destroyed:
            self._sm.switch("end", is_win=False, score=self._stage.score)
            px.play(1, 4)
            return

        self._start_timer.update()

    def draw(self):
        px.cls(px.COLOR_BLACK)
        self._bg.draw()
        self._stage.draw()
        self._draw_ui()

    def _draw_ui(self):
        score_text = f"SCORE: {self._stage.score:5}"
        print_center(0, score_text, px.COLOR_WHITE, self._font)

        if self._stage.chain_count > 1:
            st_width = self._font.text_width(score_text)
            ratio = self._stage.chain_timer.left / self._stage.chain_timer.max
            line_width = st_width * ratio
            hline(px.width // 2 - st_width // 2, 10, line_width)
            px.text(px.width // 2 + st_width // 2 + 2, 8, f"x{self._stage.chain_count}", px.COLOR_WHITE)

        hs_text = f"HIGH: {self._highscore:5}"
        hst_width = self._font.text_width(hs_text)
        px.text(px.width - hst_width, 0, hs_text, px.COLOR_WHITE, self._font)
        px.text(0, 0, "@" * self._stage.player.health, px.COLOR_WHITE, self._font)
        px.text(30, 0, f"WAVE: {self._stage.current_wave}", px.COLOR_WHITE, self._font)

        if not self._start_timer.done:
            print_center(px.height // 2, self._stage.name, px.COLOR_WHITE, self._font)
