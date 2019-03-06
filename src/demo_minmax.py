import time
import copy
import numpy as np
from move import Move
from engine import Engine
from operator import itemgetter

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

class DemoMinMaxPlayer:
    def __init__(self, heuristic, alphabeta=False, depth=3, output_file=None, name="MinMax"):
        self.name = name
        self.heuristic_object = heuristic
        self.depth = int(depth)
        self.alphabeta = alphabeta
        self.output_file = output_file

    # @timeit
    def play(self, id_ai, engine):
        self.id_ai = id_ai
        local_engine = copy.deepcopy(engine)
        self.all_visited_states = [] # (level, value)
        move = self.max(id_ai, engine, self.depth, -100000000, 100000000)
        if self.output_file is not None:
            count_level_3 = sum([1 for el in self.all_visited_states if el[0] == 3])
            count_level_2 = sum([1 for el in self.all_visited_states if el[0] == 2])
            file_pointer = open(self.output_file, "a")
            file_pointer.write(str(count_level_3) + "\n")
            file_pointer.write(str(move[0]) + "\n")
            file_pointer.write("\n")
            for val in self.all_visited_states:
                if val[0]==2:
                    file_pointer.write(str(val[1]) + "\n")
            file_pointer.write("\n")

            file_pointer.close()
        return move[1]

    def heuristic(self, id_ai, engine):
        val = self.heuristic_object.value(id_ai, engine)
        return val

    def max(self, id_ai, engine, depth, alpha, beta):
        if depth == 0:
            current_val = self.heuristic(self.id_ai, engine)
            self.all_visited_states.append((self.depth - depth + 1, current_val))
            return (current_val, None)

        moves = engine.available_moves()
        best_move = None

        for move in moves:
            engine.do_move(move) #No need to check if the move is legal it has already been done
            vlue = self.min((id_ai+1)%2, engine, depth-1, alpha, beta)
            engine.cancel_last_move()
            value = vlue[0] #Min return tuple
            if value > alpha:
                alpha = value
                best_move = move
            if self.alphabeta and value >= beta:
                self.all_visited_states.append((self.depth - depth + 1, value))
                return (value, move)
        self.all_visited_states.append((self.depth - depth + 1, alpha))
        return (alpha, best_move)

    def min(self, id_ai, engine, depth, alpha, beta):
        if depth == 0:
            current_val = self.heuristic(self.id_ai, engine)
            self.all_visited_states.append((self.depth - depth + 1, current_val))
            return (current_val, None)

        moves = engine.available_moves()
        best_move = None

        for move in moves:
            engine.do_move(move) #No need to check if the move is legal it has already been done
            vlue = self.max((id_ai+1)%2, engine, depth-1, alpha, beta)
            engine.cancel_last_move()
            value = vlue[0] #Min return tuple
            if value < beta:
                beta = value
                best_move = move
            if self.alphabeta and value <= alpha:
                self.all_visited_states.append((self.depth - depth + 1, value))
                return (value, move)
        self.all_visited_states.append((self.depth - depth + 1, beta))
        return (beta, best_move)
