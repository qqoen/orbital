import pyxel as px
from src.player import Player
from src.common import *
from src.data import ENEMIES
from .stage import Stage


class Stage1(Stage):
    def __init__(self, player: Player):
        super().__init__("Stage 1", 5, player)

    def _setup_wave(self):
        match self._wave:
            case 1:
                self._spawn_row(16, 16, 10, ENEMIES["zako"])
                self._spawn_row(16, 32, 10, ENEMIES["zako"])
            case 2:
                self._spawn(16, 16, ENEMIES["shooter"])
                self._spawn_row(32, 16, 8, ENEMIES["zako"])
                self._spawn(32 + 8 * 16, 16, ENEMIES["shooter"])
                self._spawn_row(16, 32, 10, ENEMIES["zako"])
                self._spawn_row(32, 48, 8, ENEMIES["zako"])
            case 3:
                self._spawn_row(16, 16, 2, ENEMIES["shooter"])
                self._spawn_row(16 + 16 * 2, 16, 6, ENEMIES["zako"])
                self._spawn_row(16 + 16 * 8, 16, 2, ENEMIES["shooter"])
                self._spawn_row(16, 32, 10, ENEMIES["zako"])
                self._spawn_row(16, 48, 10, ENEMIES["shield"])
            case 4:
                self._spawn_row(16, 16, 2, ENEMIES["zako"])
                self._spawn_row(16 + 16 * 2, 16, 6, ENEMIES["shooter"])
                self._spawn_row(16 + 16 * 8, 16, 2, ENEMIES["zako"])
                self._spawn_row(16, 32, 10, ENEMIES["fast"])
                self._spawn_row(16, 48, 10, ENEMIES["fast"])
            case 5:
                self._spawn(16, 32, ENEMIES["shooter"])
                self._spawn(48, 32, ENEMIES["boss"])
                self._spawn(80, 32, ENEMIES["shooter"])
                self._spawn_row(16, 48, 5, ENEMIES["shield"])
