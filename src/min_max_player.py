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

class MinMaxPlayer:
    def __init__(self, heuristic, depth=3, sort_moves=False, name="MinMax"):
        self.name = name
        self.heuristic_object = heuristic
        # print(depth)
        self.depth = int(depth)
        self.sort_moves = sort_moves

    # @timeit
    def play(self, id_ai, engine):
        self.id_ai = id_ai
        local_engine = copy.deepcopy(engine)
        self.average_number_of_moves = 0
        self.number_of_state = 0
        self.heuristic_called_count = 0
        self.current_best_val = -1000000000
        self.current_best_mov = []
        move = self.max(id_ai, engine, self.depth, -100000000, 100000000)
        # print("Visited states: ", self.number_of_state)
        # print("Average moves: ", (self.average_number_of_moves / self.number_of_state))
        # print("Heuristic called: ", self.heuristic_called_count)
        # print("Value (", self.heuristic_object.name, ") = ", move[0])
        for mv in move[1]:
            mv.print_as_input()
        print(move[1])
        return move[1][0]

    def heuristic(self, id_ai, engine):
        self.heuristic_called_count += 1
        val = self.heuristic_object.value(id_ai, engine)
        return val

    def value_move(self, engine, move, id_ai):
        engine.do_move(move) #No need to check if the move is legal it has already been done
        value = self.heuristic(self.id_ai, engine)
        engine.cancel_last_move()
        return (value, move)

    def max(self, id_ai, engine, depth, alpha, beta):
        if depth == 0:
            current_val = self.heuristic(self.id_ai, engine)
            return (current_val, None)
        moves = engine.available_moves()
        s = sum([mv.recycling for mv in moves])
        if self.sort_moves:
            value = [self.value_move(engine, mv, self.id_ai) for mv in moves]
            moves = [mv[1] for mv in sorted(value, key=itemgetter(0), reverse=True) if mv[0] > -900000 ]

        self.number_of_state += 1
        self.average_number_of_moves += len(moves)
        best_val = -100000
        best_move = None
        l_move = []
        for move in moves:
            engine.do_move(move) #No need to check if the move is legal it has already been done
            vlue = self.min((id_ai+1)%2, engine, depth-1, alpha, beta)
            engine.cancel_last_move()
            value = vlue[0] #Min return tuple
            if value > alpha:
                l_move = [copy.deepcopy(move)]
                if vlue[1] is not None:
                    l_move.extend(vlue[1])
                alpha = value
                best_move = move
            if value >= beta:
                # return (value, move)
                return (value, l_move)
        # return (alpha, best_move)
        return (alpha, l_move)

    def min(self, id_ai, engine, depth, alpha, beta):
        if depth == 0:
            current_val = self.heuristic(self.id_ai, engine)
            return (current_val, None)
        moves = engine.available_moves()

        if self.sort_moves:
            value = [self.value_move(engine, mv, self.id_ai) for mv in moves]
            # moves = [mv[1] for mv in sorted(value, key=itemgetter(0))]
            best_opponent = min([mv[0] for mv in value])
            if best_opponent <= -900000:
                return (best_opponent, None)
            moves = [mv[1] for mv in sorted(value, key=itemgetter(0), reverse=True)]


        self.number_of_state += 1
        self.average_number_of_moves += len(moves)
        best_move = None
        l_move = []
        for move in moves:
            engine.do_move(move) #No need to check if the move is legal it has already been done
            vlue = self.max((id_ai+1)%2, engine, depth-1, alpha, beta)
            engine.cancel_last_move()
            value = vlue[0] #Min return tuple
            if value < beta:
                # print(move)
                l_move = [copy.deepcopy(move)]
                if vlue[1] is not None:
                    l_move.extend(vlue[1])
                beta = value
                best_move = move
            if value <= alpha:
                # return (value, move)
                return (value, l_move)
        # return (beta, best_move)
        return (beta, l_move)
