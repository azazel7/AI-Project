from human_player import HumanPlayer

def test_input_regular():
    player = HumanPlayer()
    line = "0 1 c 8"
    mv = player.match_move(line)
    assert(mv is not None)
    assert(mv.recycling == False)
    assert(mv.type == 1)
    assert(mv.pos[0] == 2) #We expect 2, because coordinates start at zero
    assert(mv.pos[1] == 7) #Same here

def test_input_regular2():
    player = HumanPlayer()
    line = "0 1 c 10"
    mv = player.match_move(line)
    assert(mv is not None)
    assert(mv.recycling == False)
    assert(mv.type == 1)
    assert(mv.pos[0] == 2) #We expect 2, because coordinates start at zero
    assert(mv.pos[1] == 9) #Same here

def test_input_recycling():
    player = HumanPlayer()
    line = "f 3 F 4 7 c 8"
    mv = player.match_move(line)
    assert(mv is not None)
    assert(mv.recycling == True)
    assert(mv.pos_rec[0] == 5) #We expect 5, because coordinates start at zero
    assert(mv.pos_rec[1] == 2) #Same here
    assert(mv.type == 7)
    assert(mv.pos[0] == 2) #We expect 2, because coordinates start at zero
    assert(mv.pos[1] == 7) #Same here

def test_input_wrong_type():
    player = HumanPlayer()
    line = "f 3 F 4 9 c 8"
    mv = player.match_move(line)
    assert(mv is None)
    line = "f 3 F 4 0 c 8"
    mv = player.match_move(line)
    assert(mv is None)

def test_input_wrong_regular():
    player = HumanPlayer()
    line = "0 1 c 01"
    mv = player.match_move(line)
    assert(mv is None)

def test_input_negative():
    player = HumanPlayer()
    line = "0 1 c -1"
    mv = player.match_move(line)
    assert(mv is None)
    line = "0 -1 c 1"
    mv = player.match_move(line)
    assert(mv is None)

def test_input_no_adjacent_recycling():
    player = HumanPlayer()
    line = "f 3 F 5 1 c 8"
    mv = player.match_move(line)
    assert(mv is None)
    line = "a 3 b 3 1 c 8"
    mv = player.match_move(line)
    assert(mv is not None)
    line = "a 3 b 4 1 c 8"
    mv = player.match_move(line)
    assert(mv is None)
    line = "a 3 c 4 1 c 8"
    mv = player.match_move(line)
    assert(mv is None)

def test_input_fuzzy():
    player = HumanPlayer()
    line = "tèifgaf"
    mv = player.match_move(line)
    assert(mv is None)
    line = "iè-pfmþâåÊÎýÛ®\033[e"
    mv = player.match_move(line)
    assert(mv is None)
    line = "0 ±Ê Û Ø"
    mv = player.match_move(line)
    assert(mv is None)
