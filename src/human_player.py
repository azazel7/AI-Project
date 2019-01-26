import sys
import re
from engine import Engine
from move import Move

class HumanPlayer:
    def __init__(self, name="otter"):
        self.name = name
        pattern = "^0 ([1-8]) ([A-H]|[a-h]) ([1-9]$|1[0-2]$)"
        self.re_regular = re.compile(pattern)
        pattern = "^([A-H]|[a-h]) ([1-9]$|1[0-2]$) ([A-H]|[a-h]) ([1-9]$|1[0-2]$) ([1-8]) ([A-H]|[a-h]) ([1-9]$|1[0-2]$)"
        self.re_recycling = re.compile(pattern)

    def play(self, engine):
        engine.print()
        while True:
            print('(\033[33m' + self.name + '\033[00m) Move: ', end='', flush=True)
            line = sys.stdin.readline()
            matching = self.re_regular.match(line)
            move = None
            #Check if input match regular move
            if matching is not None:
                move = Move()
                move.recycling = False
                move.type = int(matching.group(1))
                #Add two -1 because our coordinates start from zero
                x = ord(matching.group(2)[0]) - 96 -1
                y = int(matching.group(3)) - 1
                move.pos = (x, y)
            else:
                #Otherwise, check if input match recycling move
                matching = self.re_recycling.match(line)
                if matching is not None:
                    #Add -1 because our coordinates start from zero
                    rec_x1 = ord(matching.group(1)[0]) - 96 -1
                    rec_y1 = int(matching.group(2)) - 1
                    rec_x2 = ord(matching.group(3)[0]) - 96 -1
                    rec_y2 = int(matching.group(4)) - 1
                    # We only use the bottom-left coordinate for the recycling
                    rec_x = min(rec_x1, rec_x2)
                    rec_y = min(rec_y1, rec_y2)
                    t = int(matching.group(5))
                    x = ord(matching.group(6)[0]) - 96 -1
                    y = int(matching.group(7)) - 1
                    move = Move()
                    move.recycling = True
                    move.type = t
                    move.pos = (x, y)
                    move.pos_rec = (rec_x, rec_y)
            #If the move has been chosen, check if it's legal
            if move is not None:
                if engine.check_move(move):
                    return move
                else:
                    print("Illegal move")
            else:
                print("Wrong input")
