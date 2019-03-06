from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from scipy import signal
from scipy import misc
import numpy as np
import pickle
import magic
import os

from move import Move
from engine import Engine

class HeuristicRandom():
    def __init__(self):
        self.name = "random"

    def value(self, id_ai, engine):
        return np.random.randint(0, 10)

class HeuristicBasic():
    def __init__(self):
        self.name = "basic"

    def value(self, id_ai, engine):
        winner = engine.is_winning()
        if winner == engine.ais[id_ai].color:
            return 10000
        elif winner == engine.ais[(id_ai + 1)%2].color:
            return -10000
        elif winner == 2:
            return -1000
        return 1

class HeuristicConvolution():
    def __init__(self, dark_magic=False):
        self.name = "convolution"
        self.dark_magic = dark_magic

    def value(self, id_ai, engine):
        board_color = np.array([[0,0], [-1, -1], [-1, 1], [1, -1], [1, 1]])
        max_row = max(engine.max_row, engine.win_length)
        board_remaped = board_color[engine.board[:,:max_row]]

        # [:,:,0] --> means on the first axis take all, second axis take all, third axis only take the first index
        g_line = signal.convolve2d(board_remaped[:,:,0], engine.conv_row, mode='valid')
        g_col = signal.convolve2d(board_remaped[:,:,0], engine.conv_column, mode='valid')
        g_diag = signal.convolve2d(board_remaped[:,:,0], engine.conv_diag, mode='valid')
        g_cdiag = signal.convolve2d(board_remaped[:,:,0], engine.conv_cdiag, mode='valid')


        convol_color = np.abs(np.concatenate((g_line.reshape(g_line.shape[0] * g_line.shape[1]),\
                g_col.reshape((g_col.shape[0] * g_col.shape[1])), \
                g_diag.reshape((g_diag.shape[0] * g_diag.shape[1])), \
                g_cdiag.reshape((g_cdiag.shape[0] * g_cdiag.shape[1])), \
                ), axis=0))
        if engine.ais[id_ai].color != 0: #Our color is not the color
            convol_color = convol_color *-1

        g_line_dot = signal.convolve2d(board_remaped[:,:,1], engine.conv_row, mode='valid')
        g_col_dot = signal.convolve2d(board_remaped[:,:,1], engine.conv_column, mode='valid')
        g_diag_dot = signal.convolve2d(board_remaped[:,:,1], engine.conv_diag, mode='valid')
        g_cdiag_dot = signal.convolve2d(board_remaped[:,:,1], engine.conv_cdiag, mode='valid')

        convol_dot = np.abs(np.concatenate((g_line_dot.reshape(g_line_dot.shape[0] * g_line_dot.shape[1]),\
                g_col_dot.reshape((g_col_dot.shape[0] * g_col_dot.shape[1])), \
                g_diag_dot.reshape((g_diag_dot.shape[0] * g_diag_dot.shape[1])), \
                g_cdiag_dot.reshape((g_cdiag_dot.shape[0] * g_cdiag_dot.shape[1])), \
                ), axis=0))
        if engine.ais[id_ai].color != 1: #Our color is not the dot
            convol_dot = convol_dot *-1

        complete = np.concatenate((convol_color, convol_dot), axis=0) +4
        if self.dark_magic:
            value = magic.histogram(complete)
        else:
            my_count = np.histogram(complete, bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])[0]
            weight = np.array([-10000, -16, -8, -1, 0, 1, 8, 16, 10000])
            value = np.sum(my_count * weight)
        return value

class HeuristicVspace():
    def __init__(self, weights=[0, 0, 0, 1000000, 0, 0.5, 5, 100000, 0, 1, 8, 100000]):
        self.name = "vspace"
        self.weights = np.array(weights)

    def value(self, id_ai, engine):
        id_next_ai = len(engine.previous_moves) % 2
        val = magic.heuristic(engine.board, self.weights, engine.colors[id_next_ai])
        if engine.colors[id_ai] == 1: #Our color is the dot
            val *= -1
        return val

class HeuristicNeuralNetwork():
    def __init__(self, filename="", name = "neural"):
        self.name = name
        self.filename = filename
        if filename == "" or not os.path.isfile(filename):
            print("New Neural Model")
            self.nn = MLPClassifier(solver='adam', alpha=0, hidden_layer_sizes=(128, 256, 256, 128, 64, 32, 16, 8, 4, 2), random_state=1)
            self.basic_train()
            print("Basic training is done.")
        else:
            self.nn = pickle.load(open(filename, 'rb'))
            print("Loading from \"", filename, "\" is done.")

    def dump(self):
        pickle.dump(self.nn, open(self.filename, 'wb'))

    def basic_train(self):
        engine = Engine()
        move = Move()
        move.recycling = False
        move.type = 1
        move.pos = (0,0)
        engine.execute(move)
        move.pos = (0,1)
        engine.execute(move)
        move.pos = (0,2)
        engine.execute(move)
        move.type = 8 # type 8 so only color win, with only one column
        move.pos = (0,3)
        engine.execute(move)

        shape = engine.board.shape
        board = engine.board.reshape((shape[0] * shape[1]))
        self.nn.partial_fit([board], [0], [0, 1])

        engine = Engine()
        move = Move()
        move.recycling = False
        move.type = 1
        move.pos = (0,0)
        engine.execute(move)
        move.pos = (0,1)
        engine.execute(move)
        move.pos = (0,2)
        engine.execute(move)
        move.type = 6 # type 6 so only dot win, with only one column
        move.pos = (0,3)
        engine.execute(move)

        shape = engine.board.shape
        board = engine.board.reshape((shape[0] * shape[1]))
        self.nn.partial_fit([board], [1], [0, 1])

    def value(self, id_ai, engine):
        shape = engine.board.shape
        board = engine.board.reshape((shape[0] * shape[1]))
        value = self.nn.predict_proba([board])[0][engine.colors[id_ai]]
        # print(self.nn.predict_proba([board]))
        return value

class HeuristicDemo():
    def __init__(self):
        self.name = "Demo"

    def value(self, id_ai, engine):
        shape = engine.board.shape

        sum_val = 0
        for y in range(shape[1]):
            for x in range(shape[0]):
                idx = y * 10 + x + 1
                board_val = engine.board[(x, y)]
                if board_val > 0:
                    if board_val == 1: #red cross
                        sum_val -= 2 * idx
                    elif board_val == 2: #red circle
                        sum_val -= 1.5 * idx
                    elif board_val == 3: # white cross
                        sum_val += 3*idx
                    elif board_val == 4: # white circle
                        sum_val += idx
        return sum_val

