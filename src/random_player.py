import numpy as np
from engine import Engine

class RandomPlayer:
    def __init__(self):
        self.name = "Random"

    def play(self, engine):
        all_moves = engine.available_moves()
        idx = np.random.randint(0, len(all_moves))
        return all_moves[idx]
