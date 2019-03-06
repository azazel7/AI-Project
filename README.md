# Get Started
The following instruction had been tested on orwell.
Once you are in the directory of the project, run the following command:
```bash
module load python/3.5.1
make libs
```
If you want to run a basic game with two players named otter:
```bash
python src/main.py
```
Then, the program wait for the input of the first player.
For more clarity, you can use two human players with two different names:
```bash
python src/main.py --p1 human Platypus --p2 human Monkey
```
The previous command, create two human players named Platypus and Monkey.

Even though, feeding a sample file works with the program, I *do not* recommend
it, because once the file is finish the `readline` function get stuck on empty
lines.

Note that the default colors are color for the first player and dot for the second. To invert this, use the parameter `--invert-colors`.
For more information, you can use the parameter `-h` to get help message, but
it is not very clear for now, especially for AI players.

# Use an AI
To use an AI, you need to replace the human player by the AI algorithm you want.
- minmax : My minimax algorithm with alpha-beta pruning.
- mc : something that looks like a Monte Carlo Tree Search, but which is not.
- demo_mm : the minimax algorithm for the demo.
- demo_ab : the minimax algorithm with alpha-beta pruning for the demo.
- random : a random player.

Depending on which player you choose the parameters won't be the same.
- minmax <depth> <sort> <name>.
- demo_ab <depth> <output> <name>.
- demo_mm <depth> <output> <name>.
- mc <depth> <max_time> <name>.
- random <name>.
- human <name>.

For instance, running with a human as the first player and a MinMax that goes to depth 3 with no sorting as second player is done by:
```bash
python src/main.py --p1 human Platypus --p2 minmax 3 0
```
However, this minimax algorithm should not be difficult to beat because its default heuristic is a random one.
To change the demo heuristic, we will use the `--h2` parameter.
```bash
python src/main.py --p1 human Platypus --p2 minmax 3 0 --h2 demo
```

There are 5 different heuristics:
- basic: a naïve heuristic that simply check for winning condition.
- random: a heuristic that returns random values.
- convolution: a heuristic that rely on Numpy/Scipy built-in function to apply convolution and find valuable lines.
- vspace: a heuristic that rely on magic module built-in functions to estimate valuable empty tiles (needs dark magic parameter enabled).
- demo: The heuristic for the second demo.
