from engine import Engine
from move import Move

engine = Engine()
move = Move()
move.recycling = False
move.type = 1
move.pos = (0,0)
val = engine.execute(move)
move.type = 6
move.pos = (2,0)
val = engine.execute(move)
move.type = 6
move.pos = (2,2)
val = engine.execute(move)
print(val)
print(engine.board)
engine.print()
print(engine.board)
