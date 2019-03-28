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
def play_move(engine, mv_str):
    player = HumanPlayer()
    mv = player.match_move(mv_str)
    engine.execute(mv)

# engine = Engine(dark_magic=True)
# h = HeuristicVspace()
# p = MinMaxPlayer(h, 3, False)
# p2 = MinMaxPlayer(HeuristicConvolution())
# engine.initialize_player(p, p2)


# print(h.value(1, engine))
# print(HeuristicConvolution().value(1, engine))
# p.play(0, engine).print_as_input()
# p2.play(0, engine)
# engine.printy()
# sys.exit(0)

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

# self_play_nn()

def genetic():
   import random
   from scoop import futures
   import deap
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
engine = Engine(dark_magic=True)
h = HeuristicVspace()
p = MinMaxPlayer(h, 4, False)
p2 = MinMaxPlayer(h)
engine.initialize_player(p2, p)
play_move(engine, "0 5 B 1")
# play_move(engine, "0 4 A 1")
# play_move(engine, "0 5 B 2")
# play_move(engine, "0 2 C 3")
# play_move(engine, "0 2 B 3")
# play_move(engine, "0 2 A 3")
# play_move(engine, "0 5 B 5")
# play_move(engine, "0 3 B 6")
# play_move(engine, "0 1 B 7")
# play_move(engine, "0 8 A 5")
# play_move(engine, "0 5 F 1")
# play_move(engine, "0 8 A 7")
# play_move(engine, "0 4 G 2")
# play_move(engine, "0 4 C 8")
# play_move(engine, "0 6 A 9")
# play_move(engine, "0 2 B 8")
# play_move(engine, "0 6 A 11")
# play_move(engine, "0 6 C 10")
# play_move(engine, "0 2 B 10")
# play_move(engine, "0 1 B 12")
# play_move(engine, "0 4 G 4")
# play_move(engine, "0 8 G 6")
# play_move(engine, "0 6 F 2")
# play_move(engine, "0 4 F 4")
# play_move(engine, "A 11 A 12 6 E 1")
# play_move(engine, "A 9 A 10 8 E 3")
# play_move(engine, "A 7 A 8 6 A 7")
# play_move(engine, "B 12 C 12 8 A 9")
# play_move(engine, "E 3 E 4 2 E 3")
# play_move(engine, "B 10 B 11 8 E 5")

cProfile.run('mv = p.play(0, engine)', "output_stat")
# print(mv)
p = pstats.Stats('output_stat')
p.strip_dirs()
p.sort_stats('tottime')
p.print_stats()
# p.print_callers()
# p.sort_stats('cumtime')
# p.print_callees()

