#!/bin/python
import unittest

import pgntofen

class PgnToFenTester(unittest.TestCase):
    def test_promote_move(self):
       correctFen = 'Qnbqkbnr/pppppppp/8/8/8/8/1PPPPPPP/RNBQKBNR'
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.pgnToFen(['a8=Q']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_pessant_take_move(self):
       correctFen = 'rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR'
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.pgnToFen(['e4','d5','exd5']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_black_pessant_move(self):
        correctFen = 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR'
        pgnConverter = pgntofen.PgnToFen()
        pgnConverter.resetBoard()
        pgnConverter.pgnToFen(['e4','e5']);
        self.assertEqual(correctFen, pgnConverter.getFen())

    def test_castling_move(self):
       correctFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQ1RK1'
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.pgnToFen(['O-O'])
       self.assertEqual(correctFen, pgnConverter.getFen())
       correctFen = '1nkr1bnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQ1RK1'
       pgnConverter.pgnToFen(['O-O-O'])
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_black_pessant_move(self):
        correctFen = 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR'
        pgnConverter = pgntofen.PgnToFen()
        pgnConverter.resetBoard()
        pgnConverter.pgnToFen(['e4','e5']);
        self.assertEqual(correctFen, pgnConverter.getFen())

    def test_knight_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkb1r/pppppppp/5n2/8/8/5N2/PPPPPPPP/RNBQKB1R'
       pgnConverter.pgnToFen(['Nf3','Nf6']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_column_knight_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkb1r/pppppppp/5n2/8/8/8/PPPNPPPP/RNBQKB1R'
       pgnConverter.pgnToFen(['Nf3','Nf6', 'Nfd2']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_row_knight_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkb1r/pppppppp/5n2/8/8/8/PPPNPPPP/RNBQKB1R'
       pgnConverter.pgnToFen(['Nf3','Nf6', 'N3d2']);
       self.assertEqual(correctFen, pgnConverter.getFen())


    def test_bishop_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/pppppppp/8/8/8/B7/PPPPPPPP/RN1QKBNR'
       pgnConverter.pgnToFen(['Ba3']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_bishop_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/pppppppp/8/8/8/B7/PPPPPPPP/RN1QKBNR'
       pgnConverter.pgnToFen(['B1a3']);
       self.assertEqual(correctFen, pgnConverter.getFen())
#
    def test_rook_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/pppppppp/8/7R/8/8/PPPPPPPP/RNBQKBN1'
       pgnConverter.pgnToFen(['Rh1h5']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_king_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBK1BNR'
       pgnConverter.pgnToFen(['Kd1']);
       self.assertEqual(correctFen, pgnConverter.getFen())


#    def test_queen_move(self):
#       pgnConverter = pgntofen.PgnToFen()
#       pgnConverter.resetBoard()
#       correctFen = 'rnbQkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR'
#       pgnConverter.pgnToFen(['Qd8']);
#       pgnConverter.resetBoard()
#       correctFen = 'rnbqkbnr/pppppppp/8/8/Q7/8/PPPPPPPP/RNB1KBNR'
#       pgnConverter.pgnToFen(['Qa4']);
#       self.assertEqual(correctFen, pgnConverter.getFen())

#pgnFormat = 'e4 e5 Nf3 Nc6 Bb5 a6'
#pgntofen.pgnToFen(pgnFormat);

if __name__ == '__main__':
    unittest.main()


#['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R',
#'P', 'P', 'P', 'P', '1', 'P', 'P', 'P',
#'1', '1', '1', '1', '1', '1', '1', '1',
#'1', '1', '1', '1', '1', '1', '1', '1',
#'1', '1', '1', '1', 'P', '1', '1', '1',
#'1', '1', '1', '1', '1', '1', '1', '1',
#'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
#'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
