import numpy as np
import time
import copy
from engine import Engine
import cProfile

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed

class MinMaxPlayer:
    def __init__(self):
        self.name = "MinMax"

    @timeit
    def play(self, id_ai, engine):
        local_engine = copy.deepcopy(engine)
        move = self.max(id_ai, engine, 3, -1000000, 1000000)
        return move[1]

    def heuristic(self, id_ai, engine):
        winner = engine.is_winning()
        if winner == id_ai:
            return 10000
        elif winner == (id_ai + 1)%2:
            return -10000
        elif winner == 2:
            return -1000
        return np.random.randint(1, 10)

    def max(self, id_ai, engine, depth, alpha, beta):
        current_val = self.heuristic(id_ai, engine)
        if current_val >= 10000 or current_val <= -10000 or depth == 0:
            return (current_val, None)
        moves = engine.available_moves()
        best_val = -100000
        best_move = None
        for move in moves:
            engine.do_move(move) #No need to check if the move is legal it has already been done
            value = self.min((id_ai%2)+1, engine, depth-1, alpha, beta)
            engine.cancel_last_move()
            value = value[0] #Min return tuple
            if value > alpha:
                alpha = value
                best_move = move
            if value >= beta:
                return (value, move)
        return (alpha, best_move)

    def min(self, id_ai, engine, depth, alpha, beta):
        current_val = self.heuristic(id_ai, engine)
        if current_val >= 10000 or current_val <= -10000 or depth == 0:
            return (current_val, None)
        moves = engine.available_moves()
        best_move = None
        for move in moves:
            engine.do_move(move) #No need to check if the move is legal it has already been done
            value = self.max((id_ai%2)+1, engine, depth-1, alpha, beta)
            engine.cancel_last_move()
            value = value[0] #Min return tuple
            if value < beta:
                beta = value
                best_move = move
            if value <= alpha:
                return (value, move)
        return (beta, best_move)
