class Move:
    def __init__(self):
        self.recycling = False
        self.type = 0
        self.pos = (-1,-1)
        self.pos_rec = (-1,-1)
    def str_pos(self, pos):
        return "[" + str(pos[0]) + ", " + str(pos[1]) + "]"
    def __str__(self):
        bg_default = "\033[49m"
        bg_red = "\033[41m"
        bg_white = "\033[107m"
        fg_black = "\033[98m"
        fg_default = "\033[00m"

        if self.recycling:
            line = "R " + self.str_pos(self.pos_rec) + " -> " + self.str_pos(self.pos)
        else:
            line = "M " + self.str_pos(self.pos)
        line = line + " ("
        #Create the upper line for type of move on 2 lines
        if self.type in { 1, 3, 5, 7}:
            upper_line = ""
        else:
            upper_line = "".join([" " for i in range(len(line))])
        if self.type == 1:
            line = line + bg_red + fg_black + "x" + bg_white + "o" + fg_default + bg_default + ")"
        elif self.type == 2:
            upper_line = upper_line + bg_red + fg_black + "x" + fg_default + bg_default + "\n"
            line = line + bg_white + fg_black + "o" + fg_default + bg_default + ")"
        elif self.type == 3:
            line = line + bg_white + fg_black + "o" + bg_red + "x" + fg_default + bg_default + ")"
        elif self.type == 4:
            upper_line = upper_line + bg_white + fg_black + "o" + fg_default + bg_default + "\n"
            line = line + bg_red + fg_black + "x" + fg_default + bg_default + ")"
        elif self.type == 5:
            line = line + bg_red + fg_black + "o" + bg_white + "x" + fg_default + bg_default + ")"
        elif self.type == 6:
            upper_line = upper_line + bg_red + fg_black + "o" + fg_default + bg_default + "\n"
            line = line + bg_white + fg_black + "x" + fg_default + bg_default + ")"
        elif self.type == 7:
            line = line + bg_white + fg_black + "x" + bg_red + "o" + fg_default + bg_default + ")"
        elif self.type == 8:
            upper_line = upper_line + bg_white + fg_black + "x" + fg_default + bg_default + "\n"
            line = line + bg_red + fg_black + "o" + fg_default + bg_default + ")"
        return upper_line + line
