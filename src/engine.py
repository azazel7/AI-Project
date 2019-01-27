import numpy as np
from move import Move

class Engine:
    def __init__(self, width=8, height=12, card_count=24, max_turn=60):
        self.width = width
        self.height = height
        self.board = np.zeros((width, height))
        self.cards = np.zeros((width, height))
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
    def do_move(self, move):
        # Now we've checked the move, let's do it
        if move.recycling:
            #Don't use recycling_pos because I intend to separate the function in two later
            pos1 = move.pos_rec
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

	#Check is placement_pos are available
        for i in range(placement_pos.shape[0]):
            pos = tuple(placement_pos[i])
            #If we recycle a card partially on itself, we need to consider the recycled cells as empty
            if not (self.is_on_board(pos) and (self.board[pos] == 0 or l_in_rec(pos))):
                return False
        for i in range(no_empty_pos.shape[0]):
            pos = tuple(no_empty_pos[i])
            on_board = self.is_on_board(pos)
            is_empty = self.board[pos] == 0
            #If we recycle a card to put it above, we need to consider the cells recycled as empty
            if on_board and (is_empty or l_in_rec(pos)): #on board and empty
                return False
        for i in range(empty_pos.shape[0]):
            pos = tuple(empty_pos[i])
            if self.is_on_board(pos) and self.board[pos] != 0: #on board and not empty
                return False
        #TODO: when recycling we should not undo the last move of our opponent
        return True
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
    def print(self):
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
    def is_winning(self):
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
    def play(self, player1, player2):
        self.ais = [player1, player2]

        current_player = 0
        current_turn = 0
        while True:
            move = self.ais[current_player].play(self) #Call the player function
            # print("Player ", current_player, ": ")
            # print(move)
            # print("Turn: ", current_turn," ",self.card_count)
            legal_move = self.execute(move)
            # self.print()
            if not legal_move:
                continue
            current_player = (current_player+1)%2

            who_win = self.is_winning()
            if who_win >= 0:
                return who_win
            current_turn += 1
