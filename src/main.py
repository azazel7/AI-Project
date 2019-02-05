import sys
import re
from engine import Engine
from move import Move
from human_player import HumanPlayer
from random_player import RandomPlayer
from min_max_player import MinMaxPlayer
from monte_carlo import MonteCarloPlayer
from heuristics import HeuristicConvolution, HeuristicNeuralNetwork, HeuristicBasic, HeuristicVspace, HeuristicRandom
from sklearn.metrics import accuracy_score
import cProfile
import pstats
import copy
import numpy as np

import hello

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    # help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
                    # const=sum, default=max,
                    # help='sum the integers (default: find the max)')
# parser.add_argument("--width", type=int, nargs="1", default=8, required=False,help="Set the width of the board (default: 8)")
parser.add_argument("--width", type=int, default=8, required=False,help="Set the width of the board (default: 8)")
parser.add_argument("--height", type=int, default=12, required=False,help="Set the height of the board (default: 12)")
parser.add_argument("--p1", type=str, default=["human"], nargs="*", required=False,help="Set the first player AI (default: human)")
parser.add_argument("--h1", type=str, default=["random"], nargs="*", required=False,\
        help="Set the heuristic for the first player (default: random)(possible values are: basic, random, convolution, neural, vspace)")
parser.add_argument("--p2", type=str, default=["human"], nargs="*", required=False,help="Set the second player AI (default: human)")
parser.add_argument("--h2", type=str, default=["random"], nargs="*", required=False,\
        help="Set the heuristic for the second player (default: random)(possible values are: basic, random, convolution, neural, vspace)")
parser.add_argument("--run_type", type=str, default="standard", required=False,help="Indicate what to do (default: standard)(possible values: standard, win_rate, train)")
parser.add_argument("--round", type=int, default=20, required=False,help="Set the number of round for win_rate runs (default: 20)")
parser.add_argument("--dark-magic", default=False, action="store_true", required=False,help="Enable dark powered algorithms (default: False)")
args = parser.parse_args()
print(args)
def print_win_rate(win_rate, names=["AI 1", "AI 2"]):
    for i in range(3):
        percent = (win_rate[i] / sum(win_rate))*100
        if i == 2:
            print("Draw: ", percent, "%")
        else:
            print(names[i],": ", percent, "%")
def load_human_player(l):
    return HumanPlayer(*l)
def load_minmax_player(l, heuristic):
    if len(l) > 3:
        print("MinMax player should have 3 parameters (depth, sort, name) at most.")
        return None
    return MinMaxPlayer(heuristic, *l)
def load_montecarlo_player(l, heuristic):
    if len(l) > 3:
        print("MinMax player should have 3 parameters (depth, max_time, name) at most.")
        return None
    return MonteCarloPlayer(heuristic, *l)
def load_random_player(l):
    if len(l) > 1:
        print("Random player should only have 1 parameter, the name.")
        return None
    return RandomPlayer(*l)
def load_vspace_heuristic(dm):
    if not dm:
        print("Using vspace heuristic require dark magic.")
        raise NameError("No dark magic")
    return HeuristicVspace()
def run_standard(args):
    engine = Engine(args.width, args.height, dark_magic=args.dark_magic)
    winner = engine.play(args.p1, args.p2)
    print("Winner is player ", (winner+1), ": ", engine.ais[winner].name)
def run_win_rate(args):
    win_rate = [0, 0, 0]
    for i in range(args.round):
        engine = Engine(args.width, args.height, dark_magic=args.dark_magic)
        winner = engine.play(args.p1, args.p2)
        win_rate[winner] += 1
        print_win_rate(win_rate, [p.name for p in engine.ais])

loader_player = {"human": lambda l,h: load_human_player(l[1:]),
                "minmax": lambda l,h: load_minmax_player(l[1:], h),
                "mc": lambda l,h: load_montecarlo_player(l[1:], h),
                "random": lambda l,h: load_random_player(l[1:])}
loader_heuristic = {"basic": lambda l: HeuristicBasic(),
                    "random": lambda l: HeuristicRandom(),
                    "convolution": lambda l: HeuristicConvolution(args.dark_magic),
                    "vspace": lambda l: load_vspace_heuristic(args.dark_magic),
                    "neural": lambda l: HeuristicNeuralNetwork(l[1])}
runner = {"standard": lambda a: run_standard(a),
        "win_rate": lambda a: run_win_rate(a),
        "train": lambda a: run_train(a)}

#Instanciate the heuristics
if len(args.h1) > 0:
    args.h1 = loader_heuristic[args.h1[0]](args.h1[1:])
if len(args.h2) > 0:
    args.h2 = loader_heuristic[args.h2[0]](args.h2[1:])

#Instanciate the players
if len(args.p1) > 0:
    type_ai = args.p1[0]
    args.p1 = loader_player[type_ai](args.p1, args.h1)
if len(args.p2) > 0:
    type_ai = args.p2[0]
    args.p2 = loader_player[type_ai](args.p2, args.h2)

runner[args.run_type](args)


def test1():
    engine = Engine(colors=[1, 0])
    player = HumanPlayer()
    h = HeuristicVspace()
    mv = player.match_move("0 2 A 1")
    engine.execute(mv)
    val = h.value(0, engine)
    print("Val = ", val)
    mv = player.match_move("0 6 C 1")
    engine.execute(mv)
    engine.printy()
    val = h.value(0, engine)
    print("Val = ", val)

def test2():
    engine = Engine(colors=[1, 0])
    player = HumanPlayer()
    h = HeuristicVspace()
    mv = player.match_move("0 1 A 1")
    engine.execute(mv)
    engine.printy()
    mv = player.match_move("0 8 B 2")
    engine.execute(mv)
    engine.printy()
    mv = player.match_move("0 1 D 1")
    engine.execute(mv)
    engine.printy()
    mv = player.match_move("0 4 D 2")
    engine.execute(mv)
    engine.printy()
    mv = player.match_move("0 8 F 1")
    engine.execute(mv)
    engine.printy()
    mv = player.match_move("0 8 E 2")
    engine.execute(mv)
    engine.printy()
    mv = player.match_move("0 8 E 4")
    engine.execute(mv)
    engine.printy()
    mv = player.match_move("0 8 A 2")
    engine.execute(mv)
    val = h.value(0, engine)
    print(val)
    engine.printy()
    mv = player.match_move("0 4 C 1")
    engine.execute(mv)
    engine.printy()


def train_on_game(moves, classifier, winner):
    engine = Engine()
    list_of_state = []
    reshaping = (engine.width * engine.height)
    for move in moves:
        engine.do_move(move)
        list_of_state.append(copy.deepcopy(engine.board).reshape(reshaping))
    y = [winner for i in range(len(list_of_state))]
    classifier.partial_fit(list_of_state, y, [0, 1])
    predicted = classifier.predict(list_of_state)
    accuracy = accuracy_score(y, predicted)
    print(predicted)
    # print([move.print_as_input() for move in moves])
    print("Accuracy: ", accuracy)

def self_play_nn():
    h = HeuristicNeuralNetwork("model.nn")
    players = [MonteCarloPlayer(h), MinMaxPlayer(HeuristicVspace(), 3)]
    i = 0
    while True:
        engine = Engine()
        winner = engine.play(players[0], players[1])
        train_on_game(engine.previous_moves, h.nn, engine.colors[winner])
        print("Game: ", i+1, " - length: ", len(engine.previous_moves))
        h.dump()
        i += 1




# engine = Engine()
# # h = HeuristicConvolution()
# h = HeuristicVspace()
# # h = HeuristicNeuralNetwork()
# p = MinMaxPlayer(h, 3)
# p.color = 1
# p2 = MinMaxPlayer(h)
# p2.color = 0

# engine.ais = [p2, p]
# cProfile.run('mv = p.play(1, engine)', "output_stat")
# p = pstats.Stats('output_stat')
# p.strip_dirs()
# p.sort_stats('tottime')
# p.print_stats()
# p.print_callers()
# p.sort_stats('cumtime')
# p.print_callees()

def run_win_rate():
    win_rate = [0, 0, 0]
    for i in range(1):
        engine = Engine(colors=[1, 0])
        # val = engine.play(MinMaxPlayer(HeuristicConvolution(), 3), RandomPlayer())
        # val = engine.play(MinMaxPlayer(HeuristicVspace(), 3), RandomPlayer())
        val = engine.play(MinMaxPlayer(HeuristicVspace(), 3, True), MinMaxPlayer(HeuristicConvolution(), 3))
        # val = engine.play(RandomPlayer(), RandomPlayer())
        # val = engine.play(MonteCarloPlayer(HeuristicVspace(), 5), MinMaxPlayer(HeuristicConvolution(), 3))
        # val = engine.play(MonteCarloPlayer(HeuristicConvolution(), 4), RandomPlayer())
        win_rate[val] += 1
        print_win_rate(win_rate)

# test2()
# run_win_rate()
# self_play_nn()
