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
        self.depth = int(depth)
        if isinstance(sort_moves, bool):
            self.sort_moves = sort_moves
        else:
            self.sort_moves = (sort_moves == 1)

    @timeit
    def play(self, id_ai, engine):
        self.id_ai = id_ai
        local_engine = copy.deepcopy(engine)
        self.average_number_of_moves = 0
        self.number_of_state = 0
        self.heuristic_called_count = 0
        move = self.max(id_ai, engine, self.depth, -100000000, 100000000)
        # if len(engine.previous_moves) > 0:
            # move = self.max(id_ai, engine, self.depth, -100000000, 100000000)
        # else:
            # moves = engine.available_moves()
            #Exploring some first moves
            # moves = [mv for mv in moves if (mv.pos[0] != 0 and mv.pos[0] != engine.width-1) and mv.type in {2, 4, 6, 8}]
            # i = np.random.randint(0, len(moves))
            # return moves[i]

        if isinstance(move[1], list):
            for mv in move[1]:
                mv.print_as_input()
            print("Value: ", move[0])
            if len(move[1]) == 0:
                print("No viable moves")
                moves = engine.available_moves()
                i = np.random.randint(0, len(moves))
                return moves[i]
            return move[1][0]
        if move[1] is None:
            print("No viable moves")
            moves = engine.available_moves()
            i = np.random.randint(0, len(moves))
            return moves[i]
        return move[1]

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

        winner = engine.is_winning()
        if winner == engine.colors[id_ai]:
            return (self.heuristic(self.id_ai, engine), None)
        elif winner == engine.colors[(id_ai+1)%2]:
            return (alpha, None)

        moves = engine.available_moves()
        s = sum([mv.recycling for mv in moves])
        if self.sort_moves:
            value = [self.value_move(engine, mv, self.id_ai) for mv in moves]
            moves = [mv[1] for mv in sorted(value, key=itemgetter(0), reverse=True) if mv[0] > -900000 ]

        best_val = -100000
        best_move = None
        l_move = []

        for move in moves:
            engine.do_move(move) #No need to check if the move is legal it has already been done
            vlue = self.min((id_ai+1)%2, engine, depth-1, alpha, beta)
            engine.cancel_last_move()
            value = vlue[0] #Min return tuple

            if value > alpha:
                #Create an history of the best moves found
                # l_move = [copy.deepcopy(move)]
                # if vlue[1] is not None:
                    # l_move.extend(vlue[1])
                alpha = value
                best_move = move
            if value >= beta:
                return (value, move)
                # return (value, l_move)
        return (alpha, best_move)
        # return (alpha, l_move)

    def min(self, id_ai, engine, depth, alpha, beta):
        if depth == 0:
            current_val = self.heuristic(self.id_ai, engine)
            return (current_val, None)
        #NOTE: disabled for now because it made the minmax acting stupdly
        winner = engine.is_winning()
        if winner == engine.colors[id_ai]:
            return (alpha, None)
        elif winner == engine.colors[(id_ai+1)%2]:
            return (self.heuristic(self.id_ai, engine), None)

        moves = engine.available_moves()

        if self.sort_moves:
            value = [self.value_move(engine, mv, self.id_ai) for mv in moves]
            best_opponent = min([mv[0] for mv in value])
            moves = [mv[1] for mv in sorted(value, key=itemgetter(0), reverse=True)]

        #Does the TA or the teacher of AI read this comment?

        best_move = None
        l_move = []
        for move in moves:
            engine.do_move(move) #No need to check if the move is legal it has already been done
            vlue = self.max((id_ai+1)%2, engine, depth-1, alpha, beta)
            engine.cancel_last_move()
            value = vlue[0] #Min return tuple
            if value < beta:
                #Create an history of the best moves found
                # l_move = [copy.deepcopy(move)]
                # if vlue[1] is not None:
                    # l_move.extend(vlue[1])
                beta = value
                best_move = move
            if value <= alpha:
                return (value, move)
                # return (value, l_move)
        return (beta, best_move)
        # return (beta, l_move)
