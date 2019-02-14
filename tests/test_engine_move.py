from engine import Engine
from move import Move
from human_player import HumanPlayer

def test_move_wrong_recycling():
    engine = Engine()
    move = Move()
    move.recycling = True
    move.type = 1
    move.pos = (0,0)
    val = engine.check_move(move)
    assert(val == False)

def test_recycling():
    '''Test replacing somewhere else'''
    engine = Engine()
    engine.card_count = 1
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.recycling = True
    move.type = 6
    move.pos = (2,0)
    move.pos_rec = (0,0)
    val = engine.execute(move)
    assert(val == True)

def test_recycling_same_cells1():
    '''Test recycling on the same cells used before'''
    engine = Engine()
    engine.card_count = 1
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.recycling = True
    move.type = 6
    move.pos = (1,0)
    move.pos_rec = (0,0)
    val = engine.execute(move)
    assert(val == True)

def test_recycling_same_cells2():
    '''Test recycling on the same cells used before with same orientation'''
    engine = Engine(card_count=2)
    move = Move(False, 1, (0,0))
    val = engine.execute(move)
    assert(val == True)
    move = Move(False, 1, (2,0))
    val = engine.execute(move)
    assert(val == True)
    move = Move(True, 7, (0,0), (0,0))
    val = engine.execute(move)
    assert(val == True)

def test_recycling_same_cells3():
    '''Test recycling with the same move'''
    engine = Engine()
    engine.card_count = 1
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.recycling = True
    move.type = 1
    move.pos = (0,0)
    move.pos_rec = (0,0)
    val = engine.execute(move)
    assert(val == False)

def test_recycling_same_cells4():
    '''Test recycling with the same move'''
    engine = Engine(3, 3, card_count=2)
    mv = Move(False, 1, (0,0))
    assert(engine.execute(mv))
    mv = Move(False, 2, (2,0))
    assert(engine.execute(mv))
    mv = Move(True, 2, (1,0), (0,0))
    print(engine.check_move(mv))
    val = engine.execute(mv)
    assert(val)

def test_recycling_above():
    '''Test recycling above the current'''
    engine = Engine()
    engine.card_count = 1
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.recycling = True
    move.pos = (0,1)
    move.pos_rec = (0,0)
    val = engine.execute(move)
    assert(val == False)

def test_move_right():
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)

def test_move_duplicate():
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    val = engine.execute(move)
    assert(val == False)

def test_move_overlap():
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.pos = (1,0)
    val = engine.execute(move)
    assert(val == False)

def test_move_empty():
    #Add a card with an empty below
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.pos = (1,1)
    val = engine.execute(move)
    assert(val == False)

def test_move_right3():
    '''Add a card then a vertical card on top of it'''
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.pos = (1,1)
    move.type = 6 #Vertical type
    val = engine.execute(move)
    assert(val == True)

def test_move_right2():
    '''Add a card then add another card somewhere else.'''
    engine = Engine()
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.pos = (2,0)
    val = engine.execute(move)
    assert(val == True)

def test_recycling_on_card():
    engine = Engine(card_count=2)
    human = HumanPlayer()
    mv_str = "0 6 A 1"
    mv = human.match_move(mv_str)
    assert(mv is not None)
    val = engine.execute(mv)
    assert(val == True)
    mv_str = "0 8 G 1"
    mv = human.match_move(mv_str)
    assert(mv is not None)
    val = engine.execute(mv)
    assert(val == True)
    mv_str = "A 1 A 2 7 F 1"
    mv = human.match_move(mv_str)
    assert(mv is not None)
    val = engine.execute(mv)
    assert(val == False)

def test_move_wrong_recycling_magic():
    engine = Engine(dark_magic=True)
    move = Move()
    move.recycling = True
    move.type = 1
    move.pos = (0,0)
    val = engine.check_move(move)
    assert(val == False)

def test_recycling_magic():
    '''Test replacing somewhere else'''
    engine = Engine(dark_magic=True)
    engine.card_count = 1
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.recycling = True
    move.type = 6
    move.pos = (2,0)
    move.pos_rec = (0,0)
    val = engine.execute(move)
    assert(val == True)

def test_recycling_same_cells1_magic():
    '''Test recycling on the same cells used before'''
    engine = Engine(dark_magic=True)
    engine.card_count = 1
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.recycling = True
    move.type = 6
    move.pos = (1,0)
    move.pos_rec = (0,0)
    val = engine.execute(move)
    assert(val == True)

def test_recycling_same_cells2_magic():
    '''Test recycling on the same cells used before with same orientation'''
    engine = Engine(card_count=2)
    move = Move(False, 1, (0,0))
    val = engine.execute(move)
    assert(val == True)
    move = Move(False, 1, (2,0))
    val = engine.execute(move)
    assert(val == True)
    move = Move(True, 7, (0,0), (0,0))
    val = engine.execute(move)
    assert(val == True)

def test_recycling_same_cells3_magic():
    '''Test recycling with the same move'''
    engine = Engine(dark_magic=True)
    engine.card_count = 1
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.recycling = True
    move.type = 1
    move.pos = (0,0)
    move.pos_rec = (0,0)
    val = engine.execute(move)
    assert(val == False)

def test_recycling_same_cells4_magic():
    '''Test recycling with the same move'''
    engine = Engine(3, 3, card_count=2, dark_magic=True)
    mv = Move(False, 1, (0,0))
    assert(engine.execute(mv))
    mv = Move(False, 2, (2,0))
    assert(engine.execute(mv))
    mv = Move(True, 2, (1,0), (0,0))
    print(engine.check_move(mv))
    val = engine.execute(mv)
    assert(val)

def test_recycling_above_magic():
    '''Test recycling above the current'''
    engine = Engine(dark_magic=True)
    engine.card_count = 1
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.recycling = True
    move.pos = (0,1)
    move.pos_rec = (0,0)
    val = engine.execute(move)
    assert(val == False)

def test_move_right_magic():
    engine = Engine(dark_magic=True)
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)

def test_move_duplicate_magic():
    engine = Engine(dark_magic=True)
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    val = engine.execute(move)
    assert(val == False)

def test_move_overlap_magic():
    engine = Engine(dark_magic=True)
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.pos = (1,0)
    val = engine.execute(move)
    assert(val == False)

def test_move_empty_magic():
    #Add a card with an empty below
    engine = Engine(dark_magic=True)
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.pos = (1,1)
    val = engine.execute(move)
    assert(val == False)

def test_move_right3_magic():
    '''Add a card then a vertical card on top of it'''
    engine = Engine(dark_magic=True)
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.pos = (1,1)
    move.type = 6 #Vertical type
    val = engine.execute(move)
    assert(val == True)

def test_move_right2_magic():
    '''Add a card then add another card somewhere else.'''
    engine = Engine(dark_magic=True)
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    move.pos = (2,0)
    val = engine.execute(move)
    assert(val == True)

def test_recycling_on_card_magic():
    engine = Engine(card_count=2, dark_magic=True)
    human = HumanPlayer()
    mv_str = "0 6 A 1"
    mv = human.match_move(mv_str)
    assert(mv is not None)
    val = engine.execute(mv)
    assert(val == True)
    mv_str = "0 8 G 1"
    mv = human.match_move(mv_str)
    assert(mv is not None)
    val = engine.execute(mv)
    assert(val == True)
    mv_str = "A 1 A 2 7 F 1"
    mv = human.match_move(mv_str)
    assert(mv is not None)
    val = engine.execute(mv)
    assert(val == False)
