from engine import Engine
from move import Move

def test_win_simple_color():
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

    val = engine.is_winning()
    #NOTE because color are winning and color is player 0
    assert(val == 0)

def test_win_simple_dot():
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

    val = engine.is_winning()
    #NOTE because dot are winning and dot is player 1
    assert(val == 1)

def test_double_win():
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    engine.execute(move) #Player 1 play
    move.pos = (0,1)
    engine.execute(move) #Player 2 play
    move.pos = (0,2)
    engine.execute(move) #Player 1 play
    move.pos = (0,3)
    engine.execute(move) #Player 2 play

    #Because both player should win but player 2 was the last one to play, player 2 should win
    val = engine.is_winning()
    assert(val == 1)

def test_win_diagonal_color():
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    engine.execute(move) #Player 1 play
    move.pos = (2,0)
    engine.execute(move) #Player 2 play
    move.pos = (1,1)
    engine.execute(move) #Player 1 play
    move.pos = (4,0)
    engine.execute(move) #Player 2 play
    move.type = 6
    move.pos = (3,1)
    engine.execute(move) #Player 2 play
    move.pos = (4,1)
    engine.execute(move) #Player 2 play
    move.type = 4
    move.pos = (2,2)
    engine.execute(move) #Player 2 play
    move.type = 8
    move.pos = (3,3)
    engine.execute(move) #Player 2 play

    #Color should win
    val = engine.is_winning()
    assert(val == 0)

def test_win_diagonal_dot():
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    engine.execute(move) #Player 1 play
    move.pos = (2,0)
    engine.execute(move) #Player 2 play
    move.pos = (1,1)
    engine.execute(move) #Player 1 play
    move.type = 1
    move.pos = (4,0)
    engine.execute(move) #Player 2 play
    move.type = 6
    move.pos = (3,1)
    engine.execute(move) #Player 1 play
    move.pos = (4,1)
    engine.execute(move) #Player 2 play
    move.type = 4
    move.pos = (2,2)
    engine.execute(move) #Player 1 play
    move.type = 6
    move.pos = (3,3)
    engine.execute(move) #Player 2 play

    #Dot should win
    val = engine.is_winning()
    assert(val == 1)

def test_win_counter_diagonal_dot():
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    engine.execute(move) #Player 1 play
    move.pos = (2,0)
    engine.execute(move) #Player 2 play
    move.pos = (1,1)
    engine.execute(move) #Player 1 play
    move.type = 3
    move.pos = (4,0)
    engine.execute(move) #Player 2 play
    move.type = 8
    move.pos = (3,1)
    engine.execute(move) #Player 2 play
    move.pos = (4,1)
    move.type = 6
    engine.execute(move) #Player 2 play
    move.type = 2
    move.pos = (2,2)
    engine.execute(move) #Player 2 play
    move.type = 6
    move.pos = (3,3)
    engine.execute(move) #Player 2 play

    #Dot should win
    val = engine.is_winning()
    assert(val == 1)
