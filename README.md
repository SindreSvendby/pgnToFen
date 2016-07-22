PGN to FEN
=====================

A chess library, where the only purpose is to convert a PGN structur to FEN.


Does not handle a PGN file, but handles an array of  moves. But without comments or the move number.

Commen PGN Move part: `1. d4 d5`

Converted to Supported format: `['d4', 'd5']`

To convert from a string like `'d4 d5'` you can just
use the `split` function.
`'d4 d5'.split(' ')` => `['d4', 'd5']`

## E.g
```python
import pgntofen # assumes you have pgntofen.py in the same directory, or you know how to handle python modules.
pgnConverter = pgntofen.PgnToFen()
PGNMoves = 'd4 d5'
pgnConverter.pgnToFen(PGNMoves.split(''))
fen = pgnConverter.getFullFen()

#fen will be 'rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR - KQkq'


```
