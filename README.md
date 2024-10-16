# CS365 LabB

## Running Matches

To run matches between different AI agents, you can use the `main.py` script with the following options:

- `-r`: Number of rows in the game board.
- `-c`: Number of columns in the game board.
- `-p`: Number of initial rows of pieces for each player.
- `-w`: Heuristic function for the white player.
- `-b`: Heuristic function for the black player.
- `-t`: Test mode.

*Without the `-t` option, the program will print a state that displays each move. With the `-t` option, the program will only print the winner.*

For example, to run a match between an AI using the Evasive heuristic and an AI using the Conqueror heuristic on an 8x8 board with 2 initial rows of pieces, use the following command:

```
python main.py -r 8 -c 8 -p 2 -w evasive -b conqueror
```

## Running Test Script

The provided Bash script `test-heuristic.sh` automates the process of running multiple matches of our heuristic functions against conquerer and evasive and calculating their win rates. To run the test script, use the following command:

```
./test-heuristic.sh
```

*Depending on the size of the board and the number of games this script can take a while to run. Using 10 games on an 8 by 8 board with 2 rows of pieces will take around 15/20 minutes to test both our heurisitcs against either evasive or conquerer.*