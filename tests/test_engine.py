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
