# Workshop in Machine learning and Data Analysis

## This project is submitted by

Dan Ayzik 206038929

Noam Barlin 314620071

### This file contains instruction on how to setup and play vs our bot or simulate games of our bot versus stockfish.
### For information on the notebook please refer to notebook_readme.txt
## Requirements

C++17 or higher (g++ 8 or higher)
```bash

g++ --version
```
Python 3.9 or higher
```bash

python --version
```
make 4.0 or higher
```bash

make --version
```
Pip 19.0 or higher
```bash

pip --version
```
If any don't fit the requirements, please update them.

### ******Note******
#### If you're on windows, I provided a setup.bat file. Right click that file and click "run as administrator". 
#### It will install the required tools.


## Setup
Open a terminal and navigate to the workshop directory:


```bash

cd /path/to/workshop
```

### Compile our chess bot executable:
```bash

make
```

### Install necessary libraries(Feel free to make a venv instead)
```bash

pip install -r requirements.txt
```

## Usage

### 1) Human vs Bot
Play a game against our bot
```bash

python main.py human
```
### Other two options require downloading stockfish:
```bash

https://stockfishchess.org/download/
```

### 2) Watch stockfish vs bot
Watch a game of stockfish playing against our bot
```bash

python main.py stockfish-visuals </absolute/path/to/stockfish> --elo <ELO>
```
or
```bash

python main.py stockfish-visuals </absolute/path/to/stockfish>
```
ELO is an optional parameter. Valid values are between 1320 and 3190. Default is 2000

### 3) Run concurrent simulations vs Stockfish

```bash

python main.py stockfish </absolute/path/to/stockfish>
```
Optional flags:
```bash

--elo <ELO> --num_threads <THREADS> --iterations_per_thread <GAMES>
```
ELO -> Same as before

THREADS -> Amount of threads that will run the games. default = 5

GAMES -> Amount of games per thread. default = 10

