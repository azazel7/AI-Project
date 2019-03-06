from engine import Engine
from move import Move

def test_out_of_board():
    engine = Engine(8, 12)
    assert(engine.is_on_board((8, 0)) == False)
    assert(engine.is_on_board((7, 0)) == True)
    assert(engine.is_on_board((0, 0)) == True)
    assert(engine.is_on_board((-1, 0)) == False)
    assert(engine.is_on_board((7, 11)) == True)
    assert(engine.is_on_board((7, 12)) == False)
    assert(engine.is_on_board((8, 11)) == False)
    assert(engine.is_on_board((8, 12)) == False)
    assert(engine.is_on_board((3, 12)) == False)
    assert(engine.is_on_board((3, -12)) == False)
    assert(engine.is_on_board((3, 10)) == True)

def test_out_of_board2():
    engine = Engine(3, 3)
    assert(engine.is_on_board((8, 0)) == False)
    assert(engine.is_on_board((7, 0)) == False)
    assert(engine.is_on_board((0, 0)) == True)
    assert(engine.is_on_board((-1, 0)) == False)
    assert(engine.is_on_board((7, 11)) == False)
    assert(engine.is_on_board((7, 12)) == False)
    assert(engine.is_on_board((8, 11)) == False)
    assert(engine.is_on_board((8, 12)) == False)
    assert(engine.is_on_board((3, 12)) == False)
    assert(engine.is_on_board((3, -12)) == False)
    assert(engine.is_on_board((3, 10)) == False)
    assert(engine.is_on_board((2, 2)) == True)
    assert(engine.is_on_board((3, 3)) == False)
    assert(engine.is_on_board((0, 3)) == False)
    assert(engine.is_on_board((3, 0)) == False)
    assert(engine.is_on_board((2, 0)) == True)

def test_available_moves():
    engine = Engine(3, 3)
    moves = engine.available_moves()
    targets = []
    targets.append(Move(False, 1, (0,0)))
    targets.append(Move(False, 2, (0,0)))
    targets.append(Move(False, 3, (0,0)))
    targets.append(Move(False, 4, (0,0)))
    targets.append(Move(False, 5, (0,0)))
    targets.append(Move(False, 6, (0,0)))
    targets.append(Move(False, 7, (0,0)))
    targets.append(Move(False, 8, (0,0)))
    targets.append(Move(False, 1, (1,0)))
    targets.append(Move(False, 2, (1,0)))
    targets.append(Move(False, 3, (1,0)))
    targets.append(Move(False, 4, (1,0)))
    targets.append(Move(False, 5, (1,0)))
    targets.append(Move(False, 6, (1,0)))
    targets.append(Move(False, 7, (1,0)))
    targets.append(Move(False, 8, (1,0)))
    targets.append(Move(False, 2, (2,0)))
    targets.append(Move(False, 4, (2,0)))
    targets.append(Move(False, 6, (2,0)))
    targets.append(Move(False, 8, (2,0)))

    assert(len(moves) == len(targets))

    for mv_target in targets:
        found = False
        for mv in moves:
            if mv.recycling == mv_target.recycling and mv.type == mv_target.type and mv.pos == mv_target.pos:
                found = True
                break
        assert(found == True)

def test_available_moves2():
    engine = Engine(3, 3)
    mv = Move(False, 1, (0,0))
    engine.execute(mv)
    moves = engine.available_moves()
    targets = []
    targets.append(Move(False, 1, (0,1)))
    targets.append(Move(False, 2, (0,1)))
    targets.append(Move(False, 3, (0,1)))
    targets.append(Move(False, 4, (0,1)))
    targets.append(Move(False, 5, (0,1)))
    targets.append(Move(False, 6, (0,1)))
    targets.append(Move(False, 7, (0,1)))
    targets.append(Move(False, 8, (0,1)))

    targets.append(Move(False, 2, (1,1)))
    targets.append(Move(False, 4, (1,1)))
    targets.append(Move(False, 6, (1,1)))
    targets.append(Move(False, 8, (1,1)))

    targets.append(Move(False, 2, (2,0)))
    targets.append(Move(False, 4, (2,0)))
    targets.append(Move(False, 6, (2,0)))
    targets.append(Move(False, 8, (2,0)))

    assert(len(moves) == len(targets))

    for mv_target in targets:
        found = False
        for mv in moves:
            if mv.recycling == mv_target.recycling and mv.type == mv_target.type and mv.pos == mv_target.pos:
                found = True
                break
        assert(found == True)

def test_available_moves3():
    engine = Engine(3, 3, card_count=2)
    mv = Move(False, 2, (0,0))
    engine.execute(mv)
    mv = Move(False, 1, (1,0))
    engine.execute(mv)
    engine.printy()
    moves = engine.available_moves()
    targets = []

    targets.append(Move(True, 4, (0,0), (0,0)))
    targets.append(Move(True, 6, (0,0), (0,0)))
    targets.append(Move(True, 8, (0,0), (0,0)))

    targets.append(Move(True, 1, (1,1), (0,0)))
    targets.append(Move(True, 2, (1,1), (0,0)))
    targets.append(Move(True, 3, (1,1), (0,0)))
    targets.append(Move(True, 4, (1,1), (0,0)))
    targets.append(Move(True, 5, (1,1), (0,0)))
    targets.append(Move(True, 6, (1,1), (0,0)))
    targets.append(Move(True, 7, (1,1), (0,0)))
    targets.append(Move(True, 8, (1,1), (0,0)))

    targets.append(Move(True, 2, (2,1), (0,0)))
    targets.append(Move(True, 4, (2,1), (0,0)))
    targets.append(Move(True, 6, (2,1), (0,0)))
    targets.append(Move(True, 8, (2,1), (0,0)))

    assert(len(moves) == len(targets))

    for mv_target in targets:
        found = False
        for mv in moves:
            if mv.recycling == mv_target.recycling and mv.type == mv_target.type and mv.pos == mv_target.pos and mv.pos_rec == mv_target.pos_rec:
                found = True
                break
        assert(found == True)

def test_available_moves_magic():
    engine = Engine(3, 3, dark_magic=True)
    moves = engine.available_moves()
    targets = []
    targets.append(Move(False, 1, (0,0)))
    targets.append(Move(False, 2, (0,0)))
    targets.append(Move(False, 3, (0,0)))
    targets.append(Move(False, 4, (0,0)))
    targets.append(Move(False, 5, (0,0)))
    targets.append(Move(False, 6, (0,0)))
    targets.append(Move(False, 7, (0,0)))
    targets.append(Move(False, 8, (0,0)))
    targets.append(Move(False, 1, (1,0)))
    targets.append(Move(False, 2, (1,0)))
    targets.append(Move(False, 3, (1,0)))
    targets.append(Move(False, 4, (1,0)))
    targets.append(Move(False, 5, (1,0)))
    targets.append(Move(False, 6, (1,0)))
    targets.append(Move(False, 7, (1,0)))
    targets.append(Move(False, 8, (1,0)))
    targets.append(Move(False, 2, (2,0)))
    targets.append(Move(False, 4, (2,0)))
    targets.append(Move(False, 6, (2,0)))
    targets.append(Move(False, 8, (2,0)))

    assert(len(moves) == len(targets))

    for mv_target in targets:
        found = False
        for mv in moves:
            if mv.recycling == mv_target.recycling and mv.type == mv_target.type and mv.pos == mv_target.pos:
                found = True
                break
        assert(found == True)

def test_available_moves2_magic():
    engine = Engine(3, 3, dark_magic=True)
    mv = Move(False, 1, (0,0))
    engine.execute(mv)
    moves = engine.available_moves()
    targets = []
    targets.append(Move(False, 1, (0,1)))
    targets.append(Move(False, 2, (0,1)))
    targets.append(Move(False, 3, (0,1)))
    targets.append(Move(False, 4, (0,1)))
    targets.append(Move(False, 5, (0,1)))
    targets.append(Move(False, 6, (0,1)))
    targets.append(Move(False, 7, (0,1)))
    targets.append(Move(False, 8, (0,1)))

    targets.append(Move(False, 2, (1,1)))
    targets.append(Move(False, 4, (1,1)))
    targets.append(Move(False, 6, (1,1)))
    targets.append(Move(False, 8, (1,1)))

    targets.append(Move(False, 2, (2,0)))
    targets.append(Move(False, 4, (2,0)))
    targets.append(Move(False, 6, (2,0)))
    targets.append(Move(False, 8, (2,0)))

    assert(len(moves) == len(targets))

    for mv_target in targets:
        found = False
        for mv in moves:
            if mv.recycling == mv_target.recycling and mv.type == mv_target.type and mv.pos == mv_target.pos:
                found = True
                break
        assert(found == True)

def test_available_moves3_magic():
    engine = Engine(3, 3, card_count=2, dark_magic=True)
    mv = Move(False, 2, (0,0))
    engine.execute(mv)
    mv = Move(False, 1, (1,0))
    engine.execute(mv)
    engine.printy()
    moves = engine.available_moves()
    targets = []

    targets.append(Move(True, 4, (0,0), (0,0)))
    targets.append(Move(True, 6, (0,0), (0,0)))
    targets.append(Move(True, 8, (0,0), (0,0)))

    targets.append(Move(True, 1, (1,1), (0,0)))
    targets.append(Move(True, 2, (1,1), (0,0)))
    targets.append(Move(True, 3, (1,1), (0,0)))
    targets.append(Move(True, 4, (1,1), (0,0)))
    targets.append(Move(True, 5, (1,1), (0,0)))
    targets.append(Move(True, 6, (1,1), (0,0)))
    targets.append(Move(True, 7, (1,1), (0,0)))
    targets.append(Move(True, 8, (1,1), (0,0)))

    targets.append(Move(True, 2, (2,1), (0,0)))
    targets.append(Move(True, 4, (2,1), (0,0)))
    targets.append(Move(True, 6, (2,1), (0,0)))
    targets.append(Move(True, 8, (2,1), (0,0)))

    assert(len(moves) == len(targets))

    for mv_target in targets:
        found = False
        for mv in moves:
            if mv.recycling == mv_target.recycling and mv.type == mv_target.type and mv.pos == mv_target.pos and mv.pos_rec == mv_target.pos_rec:
                found = True
                break
        assert(found == True)
