import numpy as np
from move import Move
from scipy import signal
from scipy import misc
import hello

class Engine:
    def __init__(self, width=8, height=12, card_count=24, max_turn=60, colors=[0,1]):
        self.width = width
        self.height = height
        self.board = np.zeros((width, height), dtype=np.int8)
        self.cards = np.zeros((width, height), dtype=np.int8)
        self.card_count = card_count
        self.max_turn = max_turn
        self.previous_moves = []
        self.win_length = 4
        #matching_cells describes how cells can form lines together.
        #for instance, a cell with 1 (red with filled dot) share the same color as 2 (red with empty dot)
        #matching_cells[0] is the matrix for the color
        self.matching_cells = np.zeros((2, 4, 4))
        self.matching_cells[0][0][0] = 1
        self.matching_cells[0][1][1] = 1
        self.matching_cells[0][2][2] = 1
        self.matching_cells[0][3][3] = 1
        self.matching_cells[0][0][1] = 1
        self.matching_cells[0][1][0] = 1
        self.matching_cells[0][2][3] = 1
        self.matching_cells[0][3][2] = 1
        #matching_cells[1] is the matrix for the dot
        self.matching_cells[1][0][0] = 1
        self.matching_cells[1][1][1] = 1
        self.matching_cells[1][2][2] = 1
        self.matching_cells[1][3][3] = 1
        self.matching_cells[1][0][2] = 1
        self.matching_cells[1][2][0] = 1
        self.matching_cells[1][1][3] = 1
        self.matching_cells[1][3][1] = 1

        self.all_lines = self.build_all_lines()

        self.conv_column = np.ones((1, self.win_length))
        self.conv_row = np.ones((self.win_length, 1))
        self.conv_diag = np.eye(self.win_length, dtype=np.int8)
        self.conv_cdiag = self.conv_diag[::-1] #Flip on the vertical axis
        self.colors = colors

        self.max_row = 0
        self.min_column = -1
        self.max_column = self.width+1

    def build_all_lines(self):
        '''This function build all lines of the board with coordinates of each cell. Row, column, and diagonals'''
        board = self.board
        shape = board.shape
        all_lines = []
        for x in range(shape[0]):
            all_lines.append([])
            for y in range(shape[1]):
                all_lines[-1].append((x,y))
        for y in range(shape[1]):
            all_lines.append([])
            for x in range(shape[0]):
                all_lines[-1].append((x,y))

        for y in range(shape[1]):
            x = 0
            l = self.get_counter_diagonal_line(x,y)
            if len(l) >= self.win_length:
                all_lines.append(l)
            l = self.get_diagonal_line(x,y)
            if len(l) >= self.win_length:
                all_lines.append(l)

        for x in range(1,shape[0]):
            l = self.get_counter_diagonal_line(x,0)
            if len(l) >= self.win_length:
                all_lines.append(l)
            l = self.get_diagonal_line(x,shape[1]-1)
            if len(l) >= self.win_length:
                all_lines.append(l)

        return all_lines
    def get_diagonal_line(self, start_x, start_y):
        shape = self.board.shape
        offset = 0
        line = []
        while start_x+offset < shape[0] and start_y-offset >= 0:
            coor = (start_x+offset, start_y-offset)
            line.append(coor)
            offset = offset + 1
        return line
    def get_counter_diagonal_line(self, start_x, start_y):
        shape = self.board.shape
        offset = 0
        line = []
        while start_x+offset < shape[0] and start_y + offset < shape[1]:
            coor = (start_x+offset, start_y+offset)
            line.append(coor)
            offset = offset + 1
        return line

    def execute(self, move):
        legal = self.check_move(move)
        if legal:
            self.do_move(move)
        return legal
    def cancel_last_move(self):
        last_move = self.previous_moves[-1]
        self.previous_moves.pop()
        #Recycling or not, remove the card movead
        #Do it before the recycling in order to avoid erase the card replaced by a recycling
        if last_move.type in {1, 3, 5, 7}: # horizontal last_move
            pos1 = last_move.pos
            pos2 = (last_move.pos[0]+1, last_move.pos[1])
        elif last_move.type in {2, 4, 6, 8}: # vertical last_move
            pos1 = last_move.pos
            pos2 = (last_move.pos[0], last_move.pos[1]+1)
        self.cards[pos1] = 0
        self.board[pos1] = 0
        self.board[pos2] = 0

        #if last move was a recycling one, put back the card
        if last_move.recycling:
            #Find the two position
            if last_move.type_rec in {1, 3, 5, 7}: # horizontal last_move
                pos1 = last_move.pos_rec
                pos2 = (last_move.pos_rec[0]+1, last_move.pos_rec[1])
            elif last_move.type_rec in {2, 4, 6, 8}: # vertical last_move
                pos1 = last_move.pos_rec
                pos2 = (last_move.pos_rec[0], last_move.pos_rec[1]+1)

            #Set the value on the board
            if last_move.type_rec == 1 or last_move.type_rec == 4:
                self.board[pos1] = 1
                self.board[pos2] = 4
            elif last_move.type_rec == 2 or last_move.type_rec == 3:
                self.board[pos1] = 4
                self.board[pos2] = 1
            elif last_move.type_rec == 5 or last_move.type_rec == 8:
                self.board[pos1] = 2
                self.board[pos2] = 3
            elif last_move.type_rec == 6 or last_move.type_rec == 7:
                self.board[pos1] = 3
                self.board[pos2] = 2

            #Place the type in the cards matrix
            self.cards[pos1] = last_move.type_rec
        else:
            self.card_count += 1

    def do_move(self, move):
        # Now we've checked the move, let's do it
        if move.recycling:
            #Don't use recycling_pos because I intend to separate the function in two later
            pos1 = move.pos_rec
            move.type_rec = self.cards[move.pos_rec]
            if self.cards[move.pos_rec] in {1, 3, 5, 7}:
                pos2 = (move.pos_rec[0]+1, move.pos_rec[1])
            elif self.cards[move.pos_rec] in {2, 4, 6, 8}:
                pos2 = (move.pos_rec[0], move.pos_rec[1]+1)
            # Remove cards from
            self.cards[pos1] = 0
            self.board[pos1] = 0
            self.board[pos2] = 0
        else:
            self.card_count -= 1

        if move.type in {1, 3, 5, 7}: # horizontal move
            pos1 = move.pos
            pos2 = (move.pos[0]+1, move.pos[1])
        elif move.type in {2, 4, 6, 8}: # vertical move
            pos1 = move.pos
            pos2 = (move.pos[0], move.pos[1]+1)

        if move.type == 1 or move.type == 4:
            self.board[pos1] = 1
            self.board[pos2] = 4
        elif move.type == 2 or move.type == 3:
            self.board[pos1] = 4
            self.board[pos2] = 1
        elif move.type == 5 or move.type == 8:
            self.board[pos1] = 2
            self.board[pos2] = 3
        elif move.type == 6 or move.type == 7:
            self.board[pos1] = 3
            self.board[pos2] = 2

        self.cards[pos1] = move.type
        # keep a list of move done so far
        self.previous_moves.append(move)
        self.max_row = max(self.max_row, move.pos[0] + move.type in {2, 4, 6, 8})
    def check_move(self, move):
        #  recycling,  type,          pos,    pos_rec
        # (False,      type of card, (x, y), (xx, yy))
        if move.recycling and self.card_count > 0: # Recycling while there is card left
            return False
        if not move.recycling and self.card_count == 0:
            return False

	# Create list of position to check before adding a new card
        if move.type in {1, 3, 5, 7}: # horizontal move
            placement_pos = np.array([move.pos, (move.pos[0]+1, move.pos[1])])
        if move.type in {2, 4, 6, 8}: # vertical move
            placement_pos = np.array([move.pos, (move.pos[0], move.pos[1]+1)])
        if move.type in {1, 3, 5, 7}: # horizontal move
            no_empty_pos = np.array([(move.pos[0], move.pos[1]-1), (move.pos[0]+1, move.pos[1]-1)])
        if move.type in {2, 4, 6, 8}: # vertical move
            no_empty_pos = np.array([(move.pos[0], move.pos[1]-1)])

        if move.recycling:
            if not self.is_on_board(move.pos_rec) or self.cards[move.pos_rec] == 0: #Card to move is outside of the map or there is no card
                return False
            card_to_rec = self.cards[move.pos_rec]
            if move.pos_rec == move.pos and card_to_rec == move.type:
                return False
            if card_to_rec in {1, 3, 5, 7}: # Horizontal recycling
                #The two cells above the recycling card have to be empty
                empty_pos = np.array([(move.pos_rec[0], move.pos_rec[1]+1), (move.pos_rec[0]+1, move.pos_rec[1]+1)])
                recycling_pos = np.array([move.pos_rec, (move.pos_rec[0]+1, move.pos_rec[1])])
            elif card_to_rec in {2, 4, 6, 8}: # vertical recycling
                empty_pos = np.array([(move.pos_rec[0], move.pos_rec[1]+2)])
                recycling_pos = np.array([move.pos_rec, (move.pos_rec[0], move.pos_rec[1]+1)])
        else:
            empty_pos = np.array([])
            recycling_pos = np.array([])

        # From now on, the empty_pos array contains all position that should be either empty or outside the board (to recycle).
        # no_empty_pos contains all positions that should be either filled or outside the board (to place above)
        # placement_pos is where the card will be placed, thus, all position in this array should be empty and on the board.
        # recycling_pos contains the current position of the card to recycle

        #Create the lambda to check the recycling position
        if move.recycling:
            l_in_rec = lambda p: np.any(np.all(recycling_pos == p, axis=1))
        else:
            l_in_rec = lambda p: False
        if move.recycling and move.pos_rec == move.pos and move.type == self.cards[move.pos]:
            return False
        def aaa():
            #Check is placement_pos are available
            i = 0
            pos = tuple(placement_pos[i])
            #If we recycle a card partially on itself, we need to consider the recycled cells as empty
            if not (self.is_on_board(pos) and (self.board[pos] == 0 or l_in_rec(pos))):
                return False

            i = 1
            pos = tuple(placement_pos[i])
            #If we recycle a card partially on itself, we need to consider the recycled cells as empty
            if not (self.is_on_board(pos) and (self.board[pos] == 0 or l_in_rec(pos))):
                return False

            if no_empty_pos.shape[0] >= 1:
                i = 0
                pos = tuple(no_empty_pos[i])
                on_board = self.is_on_board(pos)
                is_empty = self.board[pos] == 0
                #If we recycle a card to put it above, we need to consider the cells recycled as empty
                if on_board and (is_empty or l_in_rec(pos)): #on board and empty
                    return False
            if no_empty_pos.shape[0] == 2:
                i = 1
                pos = tuple(no_empty_pos[i])
                on_board = self.is_on_board(pos)
                is_empty = self.board[pos] == 0
                #If we recycle a card to put it above, we need to consider the cells recycled as empty
                if on_board and (is_empty or l_in_rec(pos)): #on board and empty
                    return False

            if empty_pos.shape[0] >= 1:
                i = 0
                pos = tuple(empty_pos[i])
                if self.is_on_board(pos) and self.board[pos] != 0: #on board and not empty
                    return False
            if empty_pos.shape[0] >= 2:
                i = 1
                pos = tuple(empty_pos[i])
                if self.is_on_board(pos) and self.board[pos] != 0: #on board and not empty
                    return False
            return True
        # val = aaa()
        val = hello.check_pos(self.board, placement_pos, no_empty_pos, empty_pos, recycling_pos, self.width, self.height) == 1
        return val
        #TODO: when recycling we should not undo the last move of our opponent

    def available_moves(self):
        if self.card_count == 0:
            return self.available_recycling()
        else:
            return self.available_regular()
    def available_recycling(self):
        shape = self.board.shape
        all_moves = []
        for x in range(shape[0]):
            for y in range(shape[1]-1, -1, -1):
                pos  = (x,y)
                val = self.cards[pos]
                if val != 0 and pos != self.previous_moves[-1].pos:
                    all_moves.extend(self.available_recycling_card(pos))
                    break
        return all_moves

    def available_recycling_card(self, card_pos):
        '''Return all the recycling move for one card located at card_pos'''
        shape = self.board.shape
        card_type = int(self.cards[card_pos])
        ret = []
        #Store the x corresponding to card_pos to retrieve them later
        if card_type in {1, 3, 5, 7}: #If it is an horizontal move we need to x (thus two column are concerned).
            card_pos_x = np.array([card_pos[0], card_pos[0]+1])
        else:
            card_pos_x = np.array([card_pos[0]])

        #We look were we could move the current card
        for x in range(shape[0]):
            #Find the first no-empty cell of the column
            #If it's on the column of the current card directly set the position to the card
            if x in card_pos_x:
                pos = (x, card_pos[1])
            else:
                pos = (x,0)
                for y in range(shape[1]-1, -1, -1):
                    if self.board[(x,y)] != 0:
                        pos = (x,y+1)
                        break
            #If the pos we found is not even on the board, it means the column is full
            if not self.is_on_board(pos):
                continue
            #For all type of position, we check if its a legal move and add it to the list if so.
            for t in range(1, 9):
                move = Move()
                move.recycling = True
                move.type = t
                move.pos = pos
                move.pos_rec = card_pos
                if t == card_type and pos == card_pos:
                    continue
                legal = self.check_move(move)
                if legal:
                    ret.append(move)
        return ret
    def available_regular(self):
        regular_moves = []
        shape = self.board.shape
        for x in range(shape[0]):
            #Find the first no-empty cell of the column
            pos = (x,0)
            for y in range(shape[1]-1, -1, -1):
                if self.board[(x,y)] != 0:
                    pos = (x,y+1)
                    break
            #If the pos we found is not even on the board, it means the column is full
            if not self.is_on_board(pos):
                continue
            #For all type of position, we check if its a legal move and add it to the list if so.
            for t in range(1, 9):
                move = Move()
                move.recycling = False
                move.type = t
                move.pos = pos
                legal = self.check_move(move)
                if legal:
                    regular_moves.append(move)
        return regular_moves

    def is_on_board(self, pos):
        if pos[0] < 0 or pos[0] >= self.width:
            return False
        if pos[1] < 0 or pos[1] >= self.height:
            return False
        return True

    def printy(self):
        # 0: Empty cell
        # 1: Red with filled dot
        # 2: Red with empty dot
        # 3: White with filled dot
        # 4: White with empty dot
        shape = self.board.shape
        bg_default = "\033[49m"
        bg_red = "\033[41m"
        bg_white = "\033[107m"
        fg_black = "\033[98m"
        fg_default = "\033[00m"
        for y in range(shape[1]-1, -1, -1): #Revert order for the y-axis to avoid printing it upside-down
            line = ""
            for x in range(shape[0]):
                pos = (x, y)
                if self.board[pos] == 0:
                    line = line + " "
                elif self.board[pos] == 1:
                    line = line + bg_red + fg_black + "x" + bg_default + fg_default
                elif self.board[pos] == 2:
                    line = line + bg_red + fg_black + "o" + bg_default + fg_default
                elif self.board[pos] == 3:
                    line = line + bg_white + fg_black + "x" + bg_default + fg_default
                elif self.board[pos] == 4:
                    line = line + bg_white + fg_black + "o" + bg_default + fg_default
            print(line)
    def is_winning_line(self, line):
        '''Return who made a serie on this line.
        -1: nobody
         0: player 1
         1: player 2
         2: both
        '''
        victory = [False, False]
        #Initializing with the first element of the line
        prev_val = int(self.board[line[0]])
        if prev_val != 0:
            count = [1, 1]
        else:
            count = [0, 0]

        #Start the loop over the rest of the line
        for coor in line[1:]:
            val = int(self.board[coor])
            if val == 0:
                count = [0, 0]
            elif prev_val == 0:
                count = [1, 1]
            else:
                #For both color and dot, check if the previous value match the current value so the serie keep going.
                #For instance, if prev_val and val indicate the same color or the same type of dot.
                for i in range(2):
                    if self.matching_cells[i][prev_val-1][val-1]:
                        count[i] += 1
                    else:
                        count[i] = 1
                    #NOTE: Don't break if one is winning because it may be a double win
                    victory[i] = victory[i] or (count[i] >= self.win_length)
            prev_val = val

        if victory[0] and victory[1]:
            return 2
        if victory[0]:
            return 0
        if victory[1]:
            return 1
        return -1
    def is_winning2(self):
        '''Return who is winning.
        -1: nobody
         0: player 1
         1: player 2
         2: tie
        '''
        #TODO improve the search with a maximum high
        victory = [False, False]
        #Loop through all the lines. Don't break soon, because we need to check if it's a move with double victory
        for line in self.all_lines:
            val = self.is_winning_line(line)
            if val != -1:
                if val != 2:
                    victory[val] = True
                else:
                    victory = [True, True]
            if victory[0] and victory[1]:
                return (len(self.previous_moves)-1)%2

        if victory[0]:
            return 0
        elif victory[1]:
            return 1
        if len(self.previous_moves) > 60:
            return 2
        return -1

    def is_winning(self):
        '''Return who is winning.
        -1: nobody
         0: Color
         1: Dot
         2: tie
        '''
        #NOTE: To move later as attribute
        board_color = np.array([[0,0], [-1, -1], [-1, 1], [1, -1], [1, 1]])
        board_remaped = board_color[self.board]


        # [:,:,0] --> means on the first axis take all, second axis take all, third axis only take the first index
        g_line = signal.convolve2d(board_remaped[:,:,0], self.conv_row, mode='valid')
        g_col = signal.convolve2d(board_remaped[:,:,0], self.conv_column, mode='valid')
        g_diag = signal.convolve2d(board_remaped[:,:,0], self.conv_diag, mode='valid')
        g_cdiag = signal.convolve2d(board_remaped[:,:,0], self.conv_cdiag, mode='valid')

        #The convolution will take the mask and apply it on every cell of the board.
        #A convolution will multiply the mask with the value on the board then sum all element generated this way
        val_line = np.any(np.abs(g_line) >= 4)
        val_col = np.any(np.abs(g_col) >= 4)
        val_diag = np.any(np.abs(g_diag) >= 4)
        val_cdiag = np.any(np.abs(g_cdiag) >= 4)
        color = val_line or val_col or val_diag or val_cdiag

        g_line = signal.convolve2d(board_remaped[:,:,1], self.conv_row, mode='valid')
        g_col = signal.convolve2d(board_remaped[:,:,1], self.conv_column, mode='valid')
        g_diag = signal.convolve2d(board_remaped[:,:,1], self.conv_diag, mode='valid')
        g_cdiag = signal.convolve2d(board_remaped[:,:,1], self.conv_cdiag, mode='valid')


        val_line = np.any(np.abs(g_line) >= 4)
        val_col = np.any(np.abs(g_col) >= 4)
        val_diag = np.any(np.abs(g_diag) >= 4)
        val_cdiag = np.any(np.abs(g_cdiag) >= 4)
        dot = val_line or val_col or val_diag or val_cdiag
        if dot and not color:
            return 1
        if not dot and color:
            return 0
        if dot and color:
            player_idx = (len(self.previous_moves)-1)%2
            return self.colors[player_idx]
        if len(self.previous_moves) > 60:
            return 2
        return -1

    def play(self, player1, player2):
        '''Return which player has won.
        -1: nobody
         0: Color
         1: Dot
         2: tie
        '''
        player1.color = self.colors[0]
        player2.color = self.colors[1]
        self.ais = [player1, player2]

        current_player = 0
        current_turn = 0
        while True:
            move = self.ais[current_player].play(current_player, self) #Call the player function
            # print("Player ", self.ais[current_player].name, ": ")
            # print(move)
            # print("Turn: ", current_turn," ",self.card_count)
            legal_move = self.execute(move)
            # self.print()
            if not legal_move:
                continue

            current_player = (current_player+1)%2
            who_win = self.is_winning()
            if who_win >= 0:
                winner = who_win
                for i in range(2):
                    if self.colors[i] == who_win:
                        winner = i
                return winner
            current_turn += 1
