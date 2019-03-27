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

class HeuristicMuggleVspace():
    def __init__(self, weights=[0, 0, 0, 1000000, 0, 0.5, 5, 100000, 0, 1, 8, 100000]):
        self.name = "vspace"
        self.weights = np.array(weights)


    def count_line(self, x_start, y_start, x_offset_mul, y_offset_mul, board, shape_board, align, valuable_space, engine):
        offset = 0
        prev_val = -1
        prev_offset = [-1, -1]
        val_prev_poffset = [-1, -1]
        count = [0, 0]
        tmp_vspaces = [[0 for i in range(20)] for j in range(2)]

        #start do while
        while 1:
            x = x_start + offset*x_offset_mul
            y = y_start + offset*y_offset_mul
            if x < 0 or x >= shape_board[0] or y < 0 or y >= shape_board[1]:
                break
            idx = x*shape_board[1] + y
            val = board[idx]
            if prev_val == -1:
                if val != 0:
                    count[0] = count[1] = 1
                else:
                    count[0] = count[1] = 0
                    prev_offset[0] = prev_offset[1] = offset
            else:
                if val == 0: #Value is empty
                    if prev_val > 0: #The previous value wasn't empty, so we need to count a line of size count[i]
                        for i in range(2):
                            if count[i] > 0:
                                align[i][count[i]-1] += 1
                                tmp_vspaces[i][offset] += count[i]

                                if prev_offset[i] >= 0:
                                    po = prev_offset[i]
                                    v = val_prev_poffset[i]
                                    is_matching = engine.matching_cells[i][prev_val-1][v-1]
                                    if v > 0 and is_matching: #If the value before the previous space match our current line, combine the vspace
                                        tmp_vspaces[i][po] += count[i]
                                    else:
                                        tmp_vspaces[i][po] = max(count[i], tmp_vspaces[i][po])
                    count[0] = count[1] = 0
                    prev_offset[0] = prev_offset[1] = offset
                    val_prev_poffset[0] = val_prev_poffset[1] = prev_val
                elif prev_val == 0: #Value is not empty but previous value was empty
                        count[0] = count[1] = 1
                else:
                    #For both color and dot, check if the previous value match the current value so the serie keep going.
                    #For instance, if prev_val and val indicate the same color or the same type of dot.
                    for i in range(2):
                        is_matching = engine.matching_cells[i][prev_val-1][val-1]
                        if is_matching:
                            count[i] += 1;
                        else:
                            if prev_offset[i] >= 0: #Update the vspace
                                po = prev_offset[i]
                                v = val_prev_poffset[i]
                                is_matching = engine.matching_cells[i][prev_val-1][v-1]
                                if v != 0 and is_matching: #If the value before the previous space match our current line, combine the vspace
                                    tmp_vspaces[i][po] += count[i]
                                else:
                                    tmp_vspaces[i][po] = max(count[i], tmp_vspaces[i][po])
                                prev_offset[i] = -1
                                val_prev_poffset[i] = -1
                            if count[i] - 1 >= 4:
                                    count[i] = 4
                            align[i][count[i] - 1] += 1
                            count[i] = 1
                        if count[i] == 4:
                            align[i][3] += 1
            prev_val = val
            offset +=1


        if prev_val > 0: #The previous value wasn't empty, so we need to count a line of size count[i]
            for i in range(2):
                if count[i] > 0:
                    align[i][count[i]-1] += 1
                    if prev_offset[i] >= 0:
                            po = prev_offset[i]
                            v = val_prev_poffset[i]
                            is_matching = engine.matching_cells[i][prev_val-1][v-1]
                            if v != 0 and is_matching: #If the value before the previous space match our current line, combine the vspace
                                tmp_vspaces[i][po] += count[i]
                            else:
                                tmp_vspaces[i][po] = max(count[i], tmp_vspaces[i][po])

        for i in range(2):
            for j in range(offset):
                x = x_start + j*x_offset_mul
                y = y_start + j*y_offset_mul
                idx = x*shape_board[1] + y
                current_vspace = valuable_space[i][idx]
                tmp_vspaces[i][j] = min(tmp_vspaces[i][j],4)
                valuable_space[i][idx] = max(tmp_vspaces[i][j], current_vspace)

    def heuristic(self, engine, weights, next_player):
        board = engine.board
        shape_board = engine.board.shape
        prev_player = (next_player+1)%2; #It is a two player so we can do the +1 to get previous player.
        valuable_space = [[0 for i in range(96)] for j in range(2)]
        align = [[0 for i in range(10)] for j in range(2)]
        valuable_space_count = [[0 for i in range(4)] for j in range(2)]
        valuable_space_count_avail = [[0 for i in range(4)] for j in range(2)]
        for col in range(shape_board[0]):
            #Check column from (col, 0)
            self.count_line(col, 0, 0, 1, board.flatten(), shape_board, align, valuable_space, engine)
            #Check diagonal from (col, 0)
            self.count_line(col, 0, 1, 1, board.flatten(), shape_board, align, valuable_space, engine)
            #Check cdiagonal from (col, 0)
            self.count_line(col, 0, -1, 1, board.flatten(), shape_board, align, valuable_space, engine)
            if col > 0 and col < 7:
                self.count_line(col, shape_board[1] - 1, -1, -1, board.flatten(), shape_board, align, valuable_space, engine)
                self.count_line(col, shape_board[1] - 1,  1, -1, board.flatten(), shape_board, align, valuable_space, engine)

        for row in range(shape_board[1]):
            #Check row from (0, row)
            self.count_line(0, row, 1, 0, board.flatten(), shape_board, align, valuable_space, engine)
            if row > 7:
                #Check diagonal from (0, row)
                self.count_line(0, row, 1, -1, board.flatten(), shape_board, align, valuable_space, engine)
                #Check cdiagonal from (shape_board[0]-1, row)
                self.count_line(shape_board[0]-1, row, -1, -1, board.flatten(), shape_board, align, valuable_space, engine)

        for i in range(2):
            for y in range(shape_board[1]-1, -1, -1):
                for x in range(shape_board[0]):
                    val = valuable_space[i][x*shape_board[1]+y];
                    if val > 0:
                        if y - 2 < 0 or board[(x,y-2)] > 0:
                            valuable_space_count_avail[i][val- 1] += 1
                        else:
                            valuable_space_count[i][val- 1] += 1
        weight_align = weights[:4]
        weight_vspace = weights[4:8]
        weight_vspace_avail = weights[8:12]
        values = [0, 0]
        if align[prev_player][3] >= 1:
            values[prev_player] += align[prev_player][3] * weight_align[3]
        else:
            for i in range(2):
                for x in range(4):
                    values[i] += weight_align[x] * align[i][x]
                    values[i] += weight_vspace[x] * valuable_space_count[i][x]
                    if i == next_player:
                        xx = min(x+1, 3)
                        values[i] += weight_align[xx] * valuable_space_count_avail[i][x]
                    else:
                        values[i] += weight_vspace_avail[x] * valuable_space_count_avail[i][x]
        return values[0] - values[1]

    def value(self, id_ai, engine):
        id_next_ai = len(engine.previous_moves) % 2
        val = self.heuristic(engine, self.weights, engine.colors[id_next_ai])
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

