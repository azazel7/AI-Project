from sklearn.neural_network import MLPClassifier
from scipy import signal
from scipy import misc
import numpy as np

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
        if winner == id_ai:
            return 10000
        elif winner == (id_ai + 1)%2:
            return -10000
        elif winner == 2:
            return -1000
        return 1

class HeuristicConvolution():
    def __init__(self):
        self.name = "convolution"

    def value(self, id_ai, engine):
        board_color = np.array([[0,0], [-1, -1], [-1, 1], [1, -1], [1, 1]])
        board_remaped = board_color[engine.board]

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
            convol_color = convol_color * -1

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
            convol_dot = convol_dot * -1

        complete = np.concatenate((convol_color, convol_dot), axis=0)

        my_count = np.histogram(np.abs(complete), bins=[-5, -3, -2, -1, 0, 1, 2, 3, 4, 5])[0]
        weight = np.array([10000, 16, 8, 1, 0, 1, 8, 16, 10000])
        value = np.sum(my_count * weight)

        return value
class HeuristicNeuralNetwork():
    def __init__(self):
        self.name = "neural"
        self.nn = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10,10,10,10,10,2), random_state=1)
        self.basic_train()
        print("Training is done")

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
        self.nn.fit([board], [0])

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
        self.nn.fit([board], [1])

    def value(self, id_ai, engine):
        shape = engine.board.shape
        board = engine.board.reshape((shape[0] * shape[1]))
        value = self.nn.predict_proba([board])[0][engine.ais[id_ai].color]
        return value
