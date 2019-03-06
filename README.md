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

For more information, you can use the parameter `-h` to get help message, but
it is not very clear for now, especially for AI players.
