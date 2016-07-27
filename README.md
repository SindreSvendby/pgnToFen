PGN to FEN
=====================

A chess library, where the only purpose is to convert a PGN structur to FEN.

## Usage

The lib exposes several methods, to be used.

### Move

You can insert one and one move if you want.

#### E.g
```python
import pgntofen # assumes you have pgntofen.py in the same directory, or you know how to handle python modules.
pgnConverter = pgntofen.PgnToFen()
pgnConverter.move('d4')
fen = pgnConverter.getFullFen()
#fen will be 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b - KQkq'
```

### Moves

You can send a string, or an array of strings.
If you send a string, it may be a valid PGN Line (`1.e4 d5 2.Nf3 ....`)
if it'a and array of strings, you may only send the actulle moves (`['e4', 'd5', 'Nf3']`)

#### E.g

```python
import pgntofen # assumes you have pgntofen.py in the same directory, or you know how to handle python modules.
pgnConverter = pgntofen.PgnToFen()
PGNMoves = 'd4 d5'
pgnConverter.pgnToFen(PGNMoves.split(''))
fen = pgnConverter.getFullFen()
#fen will be 'rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR - KQkq'
```

### pgnFile

parse a pgnFile that may have sveral pgn games. See `test/Carlsen.png` for an example

#### E.g

```python
pgnConverter = pgntofen.PgnToFen()
pgnConverter.resetBoard()
file = "test/Carlsen.pgn"
stats =  pgnConverter.pgnFile(file);
# stats => {
# 'failed': [<pgntofen-error-obj>, ...],
# 'succeeded': [<game-obj>, ...]
# }

# a game-obj: (game_info, fens)
# pgntofen-error-obj: (game_info, lastMove, fen, error)
# fens: array of fen
# game_info is all the line in the pgn file working as a header before the game (e.g: all lines with [...])
```


## Speed
Running 20 000 games with pgntofen takes about 45-50 seconds on a normal laptop (4GB Ram, i7, SSD).
With chess-python this takes about 6m 15s to 6m 30s.
So you should expect an 8x improvement at least.

The file `fenStats.py` takes either "pgntofen" or "chess-python" as input.
to test on your computer run `time python fenStats.py pgntofen` and `time python fenStats.py chess-python`.

## Development

### Watch.sh
To run the test on each change, you can start the watch.sh script.
`./watch.sh `pwd` pgntofen.test.py` will run the test script `pgntofen.test.py` on each save to the current dir.

### Validate a problem
The python-chess lib is and excellent library. If something goes wrong with this library, see if you can run the same moves with chess-python. If there is a mistake there also, it's probably something wrong with the moves you are putting in.
