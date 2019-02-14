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
import argparse
import deap
import magic

def play_move(engine, mv_str):
    player = HumanPlayer()
    mv = player.match_move(mv_str)
    engine.execute(mv)

engine = Engine(3, 3, card_count=2)
mv = Move(False, 2, (0,0))
engine.execute(mv)
mv = Move(False, 1, (1,0))
engine.execute(mv)
engine.printy()
moves = engine.available_moves()
print("l: ", len(moves))
print("cc: ", engine.card_count)
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
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--width", type=int, default=8, required=False,help="Set the width of the board (default: 8)")
parser.add_argument("--height", type=int, default=12, required=False,help="Set the height of the board (default: 12)")
parser.add_argument("--p1", type=str, default=["human"], nargs="*", required=False,help="Set the first player AI (default: human)")
parser.add_argument("--h1", type=str, default=["random"], nargs="*", required=False,\
        help="Set the heuristic for the first player (default: random)(possible values are: basic, random, convolution, neural, vspace)")
parser.add_argument("--p2", type=str, default=["human"], nargs="*", required=False,help="Set the second player AI (default: human)")
parser.add_argument("--h2", type=str, default=["random"], nargs="*", required=False,\
        help="Set the heuristic for the second player (default: random)(possible values are: basic, random, convolution, neural, vspace)")
parser.add_argument("--run-type", type=str, default="standard", required=False,help="Indicate what to do (default: standard)(possible values: standard, win_rate, train)")
parser.add_argument("--round", type=int, default=20, required=False,help="Set the number of round for win_rate runs (default: 20)")
parser.add_argument("--dark-magic", default=False, action="store_true", required=False,help="Enable dark powered algorithms (default: False)")
args = parser.parse_args()
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
    for mv in engine.previous_moves:
        print("play_move(engine, \"", mv.str_as_input(), "\")")
def run_win_rate(args):
    win_rate = [0, 0, 0]
    for i in range(args.round):
        engine = Engine(args.width, args.height, dark_magic=args.dark_magic)
        winner = engine.play(args.p1, args.p2)
        for mv in engine.previous_moves:
            print("play_move(engine, \"", mv.str_as_input(), "\")")
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
    engine = Engine(dark_magic=True, colors=[1, 0])
    p1 = MinMaxPlayer(HeuristicVspace(), sort_moves=False)
    p2 = MonteCarloPlayer(HeuristicVspace())
    engine.initialize_player(p1, p2)
    play_move(engine, "0 6 F 1")
    play_move(engine, "0 4 F 3")
    play_move(engine, "0 8 G 1")
    play_move(engine, "0 6 G 3")
    play_move(engine, "0 8 E 1")
    play_move(engine, "0 8 H 1")
    play_move(engine, "0 4 H 3")
    play_move(engine, "0 8 E 3")
    play_move(engine, "0 4 E 5")
    play_move(engine, "0 5 F 5")
    play_move(engine, "0 5 F 6")
    play_move(engine, "0 1 F 7")
    play_move(engine, "0 7 F 8")
    play_move(engine, "0 8 H 5")
    play_move(engine, "0 4 E 7") #Player 2 (color) should have win after that move, player 1 (dot) minmax should not have played it
    play_move(engine, "0 4 E 9")

    # play_move(engine, "0 2 H 7")
    # play_move(engine, "0 6 G 9")
    # play_move(engine, "0 6 H 9")
    # play_move(engine, "0 4 E 9")
    # play_move(engine, "0 2 F 9")
    engine.printy()
    p1.play(0, engine)
    print(p1.heuristic_object.value(0, engine))
    # mv = mm.play(0, engine)
    # mv.print_as_input()
    # mv = player.match_move("0 8 E 1")
    # engine.execute(mv)
    # mv = player.match_move("0 2 D 1")
    # engine.execute(mv)
    # engine.printy()

def test2():
    engine = Engine(colors=[1, 0])
    player = HumanPlayer()
    h = HeuristicVspace()
    mv = player.match_move("0 1 A 1")
    engine.execute(mv)
    # engine.printy()
    mv = player.match_move("0 8 B 2")
    engine.execute(mv)
    # engine.printy()
    mv = player.match_move("0 1 D 1")
    engine.execute(mv)
    # engine.printy()
    mv = player.match_move("0 4 D 2")
    engine.execute(mv)
    # engine.printy()
    mv = player.match_move("0 8 F 1")
    engine.execute(mv)
    # engine.printy()
    mv = player.match_move("0 8 E 2")
    engine.execute(mv)
    # engine.printy()
    mv = player.match_move("0 8 E 4")
    engine.execute(mv)
    engine.printy()
    mv = player.match_move("0 8 A 2")
    # engine.execute(mv)
    # engine.printy()
    val = h.value(0, engine)
    print(val)
    # engine.printy()
    mv = player.match_move("0 4 C 1")
    engine.execute(mv)
    # engine.printy()

# test1()
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
    win_rate = [0, 0, 0]
    while True:
        engine = Engine()
        winner = engine.play(players[0], players[1])
        train_on_game(engine.previous_moves, h.nn, engine.colors[winner])
        print("Game: ", i+1, " - length: ", len(engine.previous_moves))
        h.dump()
        i += 1
        if i%10 == 0:
            print_win_rate(win_rate, ["Neural", "Vspace"])

def genetic():
   import random
   from scoop import futures
   from deap import creator, base, tools, algorithms
   creator.create("FitnessMax", base.Fitness, weights=(1.0,))
   creator.create("Individual", list, fitness=creator.FitnessMax)

   toolbox = base.Toolbox()

   toolbox.register("attr_item", np.random.normal)
   toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, n=12)
   toolbox.register("population", tools.initRepeat, list, toolbox.individual)

   def eval_weights(individual):
       h1 = HeuristicVspace()
       h2 = HeuristicVspace(individual)
       p1 = MinMaxPlayer(h1, 3, True)
       p2 = MonteCarloPlayer(h2, 6, 0.9)
       win_rate = [0, 0, 0]
       average_length = 0
       for i in range(20):
           engine = Engine(dark_magic=True)
           winner = engine.play(p1, p2)
           win_rate[winner] += 1
           if winner == 0:
               average_length += len(engine.previous_moves)
       if win_rate[0] > 0:
           length_value = (average_length / win_rate[0])
       elif win_rate[0] == 0:
           length_value = -average_length;
       else:
           length_value = 100
       value = (win_rate[1] / sum(win_rate)) * 1000 + length_value
       return (value,)

   def mutate_weights(i1):
       idx = np.random.choice(len(i1), 3, False)
       for i in idx:
           i1[i] += np.random.normal()
       return (i1,)

   toolbox.register("evaluate", eval_weights)
   toolbox.register("mate", tools.cxTwoPoint)
   toolbox.register("mutate", mutate_weights)
   toolbox.register("select", tools.selTournament, tournsize=3)
   toolbox.register("map", futures.map)
   POP_SIZE = 10
   population = toolbox.population(n=POP_SIZE)


   hof = tools.ParetoFront()
   stats = tools.Statistics(lambda ind: ind.fitness.values)
   stats.register("avg", np.mean, axis=0)
   stats.register("std", np.std, axis=0)
   stats.register("min", np.min, axis=0)
   stats.register("max", np.max, axis=0)

   ret = algorithms.eaMuCommaLambda(population, toolbox, mu=POP_SIZE, lambda_=POP_SIZE+5, cxpb=0.1, mutpb=0.5, ngen=7, stats=stats, halloffame=hof)
   print(ret)
   print(hof)

# genetic()

# engine = Engine(dark_magic=True)
# h = HeuristicVspace()
# p = MinMaxPlayer(h, 3, False)
# p2 = MinMaxPlayer(h)
# engine.initialize_player(p2, p)
# play_move(engine, "0 6 F 1")
# cProfile.run('mv = p.play(1, engine)', "output_stat")
# p = pstats.Stats('output_stat')
# p.strip_dirs()
# p.sort_stats('tottime')
# p.print_stats()
# p.print_callers()
# p.sort_stats('cumtime')
# p.print_callees()

# self_play_nn()
