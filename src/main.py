import sys
import re
from engine import Engine
from move import Move
from human_player import HumanPlayer
from random_player import RandomPlayer
from min_max_player import MinMaxPlayer
from demo_minmax import DemoMinMaxPlayer
from monte_carlo import MonteCarloPlayer
from heuristics import HeuristicConvolution, HeuristicNeuralNetwork, HeuristicBasic, HeuristicVspace, HeuristicRandom, HeuristicDemo, HeuristicMuggleVspace
from sklearn.metrics import accuracy_score
import cProfile
import pstats
import copy
import numpy as np
import argparse
import magic

# Set the parameter system
parser = argparse.ArgumentParser(description='Run the Double Card game.')
parser.add_argument("--width", type=int, default=8, required=False,help="Set the width of the board (default: 8)")
parser.add_argument("--height", type=int, default=12, required=False,help="Set the height of the board (default: 12)")
parser.add_argument("--p1", type=str, default=["human"], nargs="*", required=False,help="Set the first player AI (default: human, demo_mm, demo_ab, minmax, mc, random)")
parser.add_argument("--h1", type=str, default=["random"], nargs="*", required=False,\
        help="Set the heuristic for the first player (default: random)(possible values are: basic, random, convolution, neural, vspace, demo)")
parser.add_argument("--p2", type=str, default=["human"], nargs="*", required=False,help="Set the second player AI (default: human, demo_mm, demo_ab, minmax, mc, random)")
parser.add_argument("--h2", type=str, default=["random"], nargs="*", required=False,\
        help="Set the heuristic for the second player (default: random)(possible values are: basic, random, convolution, neural, vspace)")
parser.add_argument("--run-type", type=str, default="standard", required=False,help="Indicate what to do (default: standard)(possible values: standard, win_rate, train)")
parser.add_argument("--round", type=int, default=20, required=False,help="Set the number of round for win_rate runs (default: 20)")
parser.add_argument("--dark-magic", default=False, action="store_true", required=False,help="Enable dark powered algorithms (default: False)")
parser.add_argument("--invert-colors", default=False, action="store_true", required=False,help="Invert the color to [dot, color] (default: [color, dot])")
args = parser.parse_args()

# Define useful functions
def print_win_rate(win_rate, names=["AI 1", "AI 2"]):
    for i in range(3):
        percent = (win_rate[i] / sum(win_rate))*100
        if i == 2:
            print("Draw: ", percent, "%")
        else:
            print(names[i],": ", percent, "%")

#Define loader function
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
def load_demo_minimax_player(l, heuristic):
    return DemoMinMaxPlayer(heuristic, False, *l)
def load_demo_alphabeta_player(l, heuristic):
    return DemoMinMaxPlayer(heuristic, True, *l)
def load_random_player(l):
    if len(l) > 1:
        print("Random player should only have 1 parameter, the name.")
        return None
    return RandomPlayer(*l)
def load_vspace_heuristic(dm):
    if not dm:
        return HeuristicMuggleVspace()
    return HeuristicVspace()

#define the run functions
def run_standard(args):
    print(args)
    colors = [1, 0] if args.invert_colors else [0, 1]
    engine = Engine(args.width, args.height, colors=colors, dark_magic=args.dark_magic)
    winner = engine.play(args.p1, args.p2)
    print("Winner is player ", (winner+1), ": ", engine.ais[winner].name)
    i = 0
    for mv in engine.previous_moves:
        print("play_move(engine, \"" + mv.str_as_input() + "\") # " + engine.ais[i].name)
        i = (i + 1)%2
def run_win_rate(args):
    win_rate = [0, 0, 0]
    colors = [1, 0] if args.invert_colors else [0, 1]
    for i in range(args.round):
        engine = Engine(args.width, args.height, colors=colors, dark_magic=args.dark_magic, verbose=False)
        winner = engine.play(args.p1, args.p2)
        for mv in engine.previous_moves:
            print("play_move(engine, \"" + mv.str_as_input().strip() + "\")")
        win_rate[winner] += 1
        print_win_rate(win_rate, [p.name for p in engine.ais])

#Define dictionnary to load every thing
loader_player = {"human": lambda l,h: load_human_player(l[1:]),
                "minmax": lambda l,h: load_minmax_player(l[1:], h),
                "mc": lambda l,h: load_montecarlo_player(l[1:], h),
                "demo_mm": lambda l,h: load_demo_minimax_player(l[1:], h),
                "demo_ab": lambda l,h: load_demo_alphabeta_player(l[1:], h),
                "random": lambda l,h: load_random_player(l[1:])}
loader_heuristic = {"basic": lambda l: HeuristicBasic(),
                    "random": lambda l: HeuristicRandom(),
                    "convolution": lambda l: HeuristicConvolution(args.dark_magic),
                    "vspace": lambda l: load_vspace_heuristic(args.dark_magic),
                    "demo": lambda l: HeuristicDemo(),
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

# Run the game
runner[args.run_type](args)
