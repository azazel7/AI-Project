import time
import copy
import numpy as np
from move import Move
from engine import Engine
from operator import itemgetter
from threading import Timer

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

class MonteCarloPlayer:
    def __init__(self, heuristic, max_depth=3, max_time=3.0, name="MonteCarlo"):
        self.name = name
        self.heuristic_object = heuristic
        self.max_depth = int(max_depth)
        self.max_time = float(max_time)

    def stop(self):
        self.timesup = True

    @timeit
    def play(self, id_ai, engine):
        self.id_ai = id_ai
        self.timesup = False
        local_engine = copy.deepcopy(engine)
        Timer(self.max_time, self.stop).start()
        self.count_solution = 1

        best_move = self.max(id_ai, engine, self.max_depth)
        while not self.timesup:
            self.count_solution += 1
            move = self.max(id_ai, engine, self.max_depth)
            if move[0] > best_move[0]:
                best_move = move

        print("Checked ", self.count_solution, " solutions")
        return best_move[1]

    def heuristic(self, id_ai, engine):
        return self.heuristic_object.value(id_ai, engine)

    def value_move(self, engine, move, id_ai):
        engine.do_move(move) #No need to check if the move is legal it has already been done
        value = self.heuristic(id_ai, engine)
        engine.cancel_last_move()
        return value, move

    def max(self, id_ai, engine, depth):
        if depth == 0:
            current_val = self.heuristic(self.id_ai, engine)
            return (current_val, None)
        moves = engine.available_moves()

        value = [self.value_move(engine, mv, id_ai) for mv in moves]
        list_val = [mv[0] for mv in value]
        min_score = min([mv[0] for mv in value])
        sum_score = sum([mv[0]-min_score for mv in value])
        probability = [(mv[0]-min_score)/sum_score for mv in value]

        elt = np.random.choice(len(moves), p=probability)
        move = moves[elt]
        value_move = value[elt][0]


        # elt = np.random.randint(0, len(moves))
        # move = moves[elt]

        engine.do_move(move) #No need to check if the move is legal it has already been done
        value = self.max((id_ai+1)%2, engine, depth-1)
        engine.cancel_last_move()

        return (value_move, move)

