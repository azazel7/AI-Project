import sys
import re
from engine import Engine
from move import Move
from human_player import HumanPlayer
from random_player import RandomPlayer
from min_max_player import MinMaxPlayer
from monte_carlo import MonteCarloPlayer
from heuristics import HeuristicConvolution, HeuristicNeuralNetwork, HeuristicBasic
from sklearn.metrics import accuracy_score
import cProfile
import pstats
import copy
import numpy as np

# import hello

# hello.hello_python()
# hello.hello_numpy(np.array([[1,2],[3, 4]]))

def print_win_rate(win_rate):
    for i in range(3):
        percent = (win_rate[i] / sum(win_rate))*100
        if i == 2:
            print("Draw: ", percent, "%")
        else:
            print("AI ",i+1,": ", percent, "%")


# engine = Engine()
# move = Move()
# move.recycling = False
# move.type = 1
# move.pos = (0,0)
# engine.execute(move)
# move.pos = (0,1)
# engine.execute(move)
# move.pos = (0,2)
# engine.execute(move)
# move.type = 8 # type 8 so only color win, with only one column
# move.pos = (0,3)
# engine.execute(move)

# val = engine.is_winning()
# #NOTE because color are winning and color is player 0
# assert(val == 0)

# for mv_str in a:
    # print(mv_str)
    # mv = human.match_move(mv_str)
    # assert(mv is not None)
    # val = engine.execute(mv)
    # assert(val == True)
    # engine.print()
all_states = []
def train_on_game(moves, classifier, winner):
    engine = Engine()
    list_of_state = []
    reshaping = (engine.width * engine.height)
    for move in moves:
        engine.do_move(move)
        list_of_state.append(copy.deepcopy(engine.board).reshape(reshaping))
    y = [winner for i in range(len(list_of_state))]
    classifier.fit(list_of_state, y)
    predicted = classifier.predict(list_of_state)
    accuracy = accuracy_score(y, predicted)
    print(predicted)
    print([move.print_as_input() for move in moves])
    print("Accuracy: ", accuracy)

def self_play_nn():
    h = HeuristicNeuralNetwork("model.nn")
    players = [MinMaxPlayer(h), MinMaxPlayer(h)]
    i = 0
    while True:
        engine = Engine()
        winner = engine.play(players[0], players[1])
        train_on_game(engine.previous_moves, h.nn, engine.ais[winner].color)
        print("Game: ", i+1, " - length: ", len(engine.previous_moves))
        h.dump()
        i += 1




engine = Engine()
h = HeuristicConvolution()
# h = HeuristicNeuralNetwork()
p = MinMaxPlayer(h, 3)
p.color = 1
p2 = MinMaxPlayer(h)
p2.color = 0

engine.ais = [p2, p]
cProfile.run('mv = p.play(1, engine)', "output_stat")
p = pstats.Stats('output_stat')
p.strip_dirs()
p.sort_stats('tottime')
p.print_stats()
# p.print_callers()
# p.sort_stats('cumtime')
# p.print_callees()

def run_win_rate():
    win_rate = [0, 0, 0]
    for i in range(20):
        engine = Engine(colors=[1, 0])
        val = engine.play(MinMaxPlayer(HeuristicBasic(), 4), RandomPlayer())
        # val = engine.play(MonteCarloPlayer(HeuristicConvolution(), 4), MinMaxPlayer(HeuristicConvolution(), 3))
        # val = engine.play(MonteCarloPlayer(HeuristicConvolution(), 4), RandomPlayer())
        win_rate[val] += 1
        print_win_rate(win_rate)

# run_win_rate()
# self_play_nn()
