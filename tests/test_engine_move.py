from engine import Engine
from move import Move

def test_move_wrong_recycling():
    engine = Engine()
    move = Move()
    move.recycling = True
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
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
    engine.print()
    move.recycling = True
    move.type = 6
    move.pos = (1,0)
    move.pos_rec = (0,0)
    val = engine.execute(move)
    assert(val == True)

def test_recycling_same_cells2():
    '''Test recycling on the same cells used before with same orientation'''
    engine = Engine()
    engine.card_count = 1
    move = Move()
    move.recycling = False
    move.type = 1
    move.pos = (0,0)
    val = engine.execute(move)
    assert(val == True)
    engine.print()
    move.recycling = True
    move.type = 7
    move.pos = (0,0)
    move.pos_rec = (0,0)
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
    engine.print()
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
