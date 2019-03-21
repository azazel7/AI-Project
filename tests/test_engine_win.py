from engine import Engine
from move import Move
from human_player import HumanPlayer

def play_move(engine, mv_str):
    player = HumanPlayer()
    mv = player.match_move(mv_str)
    engine.execute(mv)

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

def test_win_simple_color_magic():
    engine = Engine(dark_magic=True)
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

def test_win_simple_dot_magic():
    engine = Engine(dark_magic=True)
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

def test_double_win_magic():
    engine = Engine(dark_magic=True)
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

def test_win_diagonal_color_magic():
    engine = Engine(dark_magic=True)
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

def test_win_diagonal_dot_magic():
    engine = Engine(dark_magic=True)
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

def test_win_counter_diagonal_dot_magic():
    engine = Engine(dark_magic=True)
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

def test_no_win_high():
    engine = Engine()
    play_move(engine, "0 2 A 1")
    play_move(engine, "0 4 B 1")
    play_move(engine, "0 2 C 1")
    play_move(engine, "0 4 D 1")
    play_move(engine, "0 2 A 3")
    play_move(engine, "0 2 B 3")
    play_move(engine, "0 4 C 3")
    play_move(engine, "0 4 D 3")
    play_move(engine, "0 2 A 5")
    play_move(engine, "0 4 B 5")
    play_move(engine, "0 2 C 5")
    play_move(engine, "0 4 D 5")
    val = engine.is_winning()
    assert(val == -1)

def test_no_win_high_magic():
    engine = Engine(dark_magic=True)
    play_move(engine, "0 2 A 1")
    play_move(engine, "0 4 B 1")
    play_move(engine, "0 2 C 1")
    play_move(engine, "0 4 D 1")
    play_move(engine, "0 2 A 3")
    play_move(engine, "0 2 B 3")
    play_move(engine, "0 4 C 3")
    play_move(engine, "0 4 D 3")
    play_move(engine, "0 2 A 5")
    play_move(engine, "0 4 B 5")
    play_move(engine, "0 2 C 5")
    play_move(engine, "0 4 D 5")
    val = engine.is_winning()
    assert(val == -1)

def test_win_high_magic():
    engine = Engine(dark_magic=True)
    play_move(engine, "0 2 A 1")
    play_move(engine, "0 2 B 1")
    play_move(engine, "0 2 C 1")
    play_move(engine, "0 4 D 1")
    play_move(engine, "0 2 A 3")
    play_move(engine, "0 2 B 3")
    play_move(engine, "0 2 C 3")
    play_move(engine, "0 4 D 3")
    play_move(engine, "0 2 A 5")
    play_move(engine, "0 2 B 5")
    play_move(engine, "0 2 C 5")
    play_move(engine, "0 4 D 5")

    play_move(engine, "0 2 A 7")
    play_move(engine, "0 2 B 7")
    play_move(engine, "0 2 C 7")
    play_move(engine, "0 8 D 7")
    val = engine.is_winning()
    assert(val == 1)

def test_win_high():
    engine = Engine()
    play_move(engine, "0 2 A 1")
    play_move(engine, "0 2 B 1")
    play_move(engine, "0 2 C 1")
    play_move(engine, "0 4 D 1")
    play_move(engine, "0 2 A 3")
    play_move(engine, "0 2 B 3")
    play_move(engine, "0 2 C 3")
    play_move(engine, "0 4 D 3")
    play_move(engine, "0 2 A 5")
    play_move(engine, "0 2 B 5")
    play_move(engine, "0 2 C 5")
    play_move(engine, "0 4 D 5")

    play_move(engine, "0 2 A 7")
    play_move(engine, "0 2 B 7")
    play_move(engine, "0 2 C 7")
    play_move(engine, "0 8 D 7")
    val = engine.is_winning()
    assert(val == 1)

def test_win_high_diag_magic():
    engine = Engine(dark_magic=True)
    play_move(engine, "0 2 C 1")
    play_move(engine, "0 2 D 1")
    play_move(engine, "0 2 E 1")
    play_move(engine, "0 4 F 1")
    play_move(engine, "0 2 C 3")
    play_move(engine, "0 2 D 3")
    play_move(engine, "0 2 E 3")
    play_move(engine, "0 4 F 3")
    play_move(engine, "0 2 C 5")
    play_move(engine, "0 2 D 5")
    play_move(engine, "0 2 E 5")
    play_move(engine, "0 4 F 5")

    play_move(engine, "0 2 C 7")
    play_move(engine, "0 2 D 7")
    play_move(engine, "0 2 E 7")
    play_move(engine, "0 4 F 7")

    play_move(engine, "0 2 C 9")
    play_move(engine, "0 8 D 9")
    play_move(engine, "0 2 E 9")
    play_move(engine, "0 4 F 9")
    val = engine.is_winning()
    assert(val == 0)

def test_win_high_diag():
    engine = Engine(dark_magic=True)
    play_move(engine, "0 2 C 1")
    play_move(engine, "0 2 D 1")
    play_move(engine, "0 2 E 1")
    play_move(engine, "0 4 F 1")
    play_move(engine, "0 2 C 3")
    play_move(engine, "0 2 D 3")
    play_move(engine, "0 2 E 3")
    play_move(engine, "0 4 F 3")
    play_move(engine, "0 2 C 5")
    play_move(engine, "0 2 D 5")
    play_move(engine, "0 2 E 5")
    play_move(engine, "0 4 F 5")

    play_move(engine, "0 2 C 7")
    play_move(engine, "0 2 D 7")
    play_move(engine, "0 2 E 7")
    play_move(engine, "0 4 F 7")

    play_move(engine, "0 2 C 9")
    play_move(engine, "0 8 D 9")
    play_move(engine, "0 2 E 9")
    play_move(engine, "0 4 F 9")
    val = engine.is_winning()
    assert(val == 0)

def test_win_high_diag2_magic():
    engine = Engine(dark_magic=True)
    play_move(engine, "0 2 C 1")
    play_move(engine, "0 2 D 1")
    play_move(engine, "0 2 E 1")
    play_move(engine, "0 4 F 1")
    play_move(engine, "0 2 C 3")
    play_move(engine, "0 2 D 3")
    play_move(engine, "0 2 E 3")
    play_move(engine, "0 4 F 3")
    play_move(engine, "0 2 C 5")
    play_move(engine, "0 2 D 5")
    play_move(engine, "0 2 E 5")
    play_move(engine, "0 4 F 5")

    play_move(engine, "0 4 C 7")
    play_move(engine, "0 2 D 7")
    play_move(engine, "0 2 E 7")
    play_move(engine, "0 4 F 7")

    play_move(engine, "0 4 C 9")
    play_move(engine, "0 4 D 9")
    play_move(engine, "0 8 E 9")
    play_move(engine, "0 2 F 9")
    val = engine.is_winning()
    assert(val == 0)

def test_win_high_diag2():
    engine = Engine()
    play_move(engine, "0 2 C 1")
    play_move(engine, "0 2 D 1")
    play_move(engine, "0 2 E 1")
    play_move(engine, "0 4 F 1")
    play_move(engine, "0 2 C 3")
    play_move(engine, "0 2 D 3")
    play_move(engine, "0 2 E 3")
    play_move(engine, "0 4 F 3")
    play_move(engine, "0 2 C 5")
    play_move(engine, "0 2 D 5")
    play_move(engine, "0 2 E 5")
    play_move(engine, "0 4 F 5")

    play_move(engine, "0 4 C 7")
    play_move(engine, "0 2 D 7")
    play_move(engine, "0 2 E 7")
    play_move(engine, "0 4 F 7")

    play_move(engine, "0 4 C 9")
    play_move(engine, "0 4 D 9")
    play_move(engine, "0 8 E 9")
    play_move(engine, "0 2 F 9")
    val = engine.is_winning()
    assert(val == 0)
