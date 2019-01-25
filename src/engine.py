import sys
import numpy as np

class Engine:
    def __init__(self, width=8, height=12, card_count=24, max_turn=60):
        self.width = width
        self.height = height
        self.board = np.zeros((width, height))
        self.cards = np.zeros((width, height))
        self.card_count = card_count
        self.max_turn = max_turn

    def execute(self, move):
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
            if card_to_rec in {1, 3, 5, 7}: # Horizontal recycling
                #The two cells below the move *and* the two cells above the recycling card have to be *not* be empty
                empty_pos = np.array([(move.pos_rec[0], move.pos_rec[1]+1), (move.pos_rec[0]+1, move.pos_rec[1]+1)])
            elif card_to_rec in {2, 4, 6, 8}: # vertical recycling and vertical move
                empty_pos = np.array([(move.pos_rec[0], move.pos_rec[1]+2)])
        else:
            empty_pos = np.array([])

        # From now on, the empty_pos array contains all position that should be either empty or outside the board (to recycle).
        # no_empty_pos contains all positions that should be either filled or outside the board (to place above)
        # placement_pos is where the card will be placed, thus, all position in this array should be empty and on the board.

        for i in range(placement_pos.shape[0]):
            pos = tuple(placement_pos[i])
            if not self.is_on_board(pos) or self.board[pos] != 0:
                return False
        for i in range(no_empty_pos.shape[0]):
            pos = tuple(no_empty_pos[i])
            if self.is_on_board(pos) and self.board[pos] == 0: #on board and empty
                return False
        for i in range(empty_pos.shape[0]):
            pos = tuple(empty_pos[i])
            if self.is_on_board(pos) and self.board[pos] != 0: #on board and empty
                return False
        #TODO: when recycling we should not undo the last move of our opponent

        # Now we've checked the move, let's do it
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
        if move.recycling:
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
        # TODO keep a list of move done so far
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
            sys.stdout.write(line + "\n")
            # print(line)

    def play(self, player1, player2):
        self.ais = [player1, player2]

        current_player = 0
        current_turn = 0
        while True:
            move = self.ais[current_player].play(self)
            print("Player ", current_player, ": ", move)
            legal_move = self.execute(move)
            if not legal_move:
                continue
            current_player = (current_player+1)%2
