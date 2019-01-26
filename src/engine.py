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

        for i in range(placement_pos.shape[0]):
            pos = tuple(placement_pos[i])
            #If we recycle a card partially on itself, we need to consider the recycled cells as empty
            if not self.is_on_board(pos) or (self.board[pos] != 0 and pos not in recycling_pos):
                return False
        for i in range(no_empty_pos.shape[0]):
            pos = tuple(no_empty_pos[i])
            on_board = self.is_on_board(pos)
            is_empty = self.board[pos] == 0
            #If we recycle a card to put it above, we need to consider the cells recycled as empty
            if on_board and (is_empty or pos in recycling_pos): #on board and empty
                return False
        for i in range(empty_pos.shape[0]):
            pos = tuple(empty_pos[i])
            if self.is_on_board(pos) and self.board[pos] != 0: #on board and not empty
                return False
        #TODO: when recycling we should not undo the last move of our opponent
        return True
    def is_on_board(self, pos):
        if pos[0] < 0 or pos[0] > self.width:
            return False
        if pos[1] < 0 or pos[1] > self.height:
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
    def isWinning(self):
        '''Return who is winning.
        -1: nobody
         0: player 1
         1: player 2
         2: tie
        '''
        return -1
    def play(self, player1, player2):
        self.ais = [player1, player2]

        current_player = 0
        current_turn = 0
        while True:
            move = self.ais[current_player].play(self) #Call the player function
            print("Player ", current_player, ": ", move)
            legal_move = self.execute(move)
            if not legal_move:
                continue
            current_player = (current_player+1)%2

            who_win = self.isWinning()
            if who_win >= 0:
                return who_win
