import pyxel as px
from src.player import Player
from src.common import *
from src.data import ENEMIES
from .stage import Stage


class Stage2(Stage):
    def __init__(self, player: Player):
        super().__init__("Stage 2", 4, player)

    def _setup_wave(self):
        match self._wave:
            case 1:
                self._spawn(16, 16, ENEMIES["shooter2"])
                self._spawn(48, 16, ENEMIES["shooter2"])
            case 2:
                self._spawn(48, 16, ENEMIES["shooter2"])
                self._spawn(64, 16, ENEMIES["shooter2"])
                self._spawn_row(16, 32, 8, ENEMIES["diver"])
            case 3:
                self._spawn_row(48, 16, 6, ENEMIES["shooter"])
                self._spawn_row(16, 32, 10, ENEMIES["diver"])
                self._spawn_row(32, 48, 8, ENEMIES["diver"])
            case 4:
                self._spawn_row(16, 16, 2, ENEMIES["zako"])
                self._spawn_row(16 + 16 * 2, 16, 6, ENEMIES["shooter"])
                self._spawn_row(16 + 16 * 8, 16, 2, ENEMIES["zako"])
                self._spawn_row(16, 32, 10, ENEMIES["shield"])
                self._spawn_row(16, 48, 10, ENEMIES["fast"])
                self._spawn_row(16, 64, 10, ENEMIES["diver"])
