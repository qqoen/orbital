class PlayerData:
    def __init__(self):
        self._highscore = 0

    @property
    def highscore(self):
        return self._highscore

    def update_score(self, new_score):
        self._highscore = max(self._highscore, new_score)
