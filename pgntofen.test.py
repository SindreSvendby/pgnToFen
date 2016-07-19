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
       correctFen = 'rnbqkbnr/pppppppp/8/8/8/8/PBPPPPPP/RN1QKBNR'
       pgnConverter.pgnToFen(['Bb2']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_bishop_advanced_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/pppppppp/8/8/8/8/PBPPPPPP/RN1QKBNR'
       pgnConverter.pgnToFen(['B1b2']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_rook_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/1ppppppp/p7/8/8/P7/RPPPPPPP/1NBQKBNR'
       pgnConverter.pgnToFen(['a3', 'a6', 'Ra2']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_rook_on_line_but_one_is_blocked_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.internalChessBoard = [
           'R','1','1','1','K','1','1','R',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           'p','p','p','p','p','p','p','p',
           'r','n','b','q','k','b','n','r']

       correctFen = 'rnbqkbnr/pppppppp/8/8/8/8/8/3RK2R'
       pgnConverter.pgnToFen(['Rd1']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_rook_on_line_but_one_is_blocked_move2(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.internalChessBoard = [
           'R','1','1','1','K','1','1','R',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           'p','p','p','p','p','p','p','p',
           'r','n','b','q','k','b','n','r']

       correctFen = 'rnbqkbnr/pppppppp/8/8/8/8/8/R3KR2'
       pgnConverter.pgnToFen(['Rf1']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_rook_on_column_but_one_is_blocked_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.internalChessBoard = [
           'R','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           'K','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           'R','1','1','1','1','1','1','1',
           'p','p','p','p','p','p','p','p',
           'r','n','b','q','k','b','n','r']

       correctFen = 'rnbqkbnr/pppppppp/R7/8/K7/R7/8/8'
       pgnConverter.pgnToFen(['Ra3']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_rook_on_column_but_one_is_blocked_move2(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.internalChessBoard = [
           'R','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           'K','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           'R','1','1','1','1','1','1','1',
           'p','p','p','p','p','p','p','p',
           'r','n','b','q','k','b','n','r']

       correctFen = 'rnbqkbnr/pppppppp/8/R7/K7/8/8/R7'
       pgnConverter.pgnToFen(['Ra5']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_king_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBK1BNR'
       pgnConverter.pgnToFen(['Kd1']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_chess_game(self):
        pgnConverter = pgntofen.PgnToFen()
        pgnConverter.resetBoard()
        correctFen = '8/8/4R1p1/2k3p1/1p4P1/1P1b1P2/3K1n2/8'
        #correctFen = 'r4rk1/1b1nqpp1/3p3p/2p1P3/1p2n3/1B3N1P/PP3PP1/RN1QR1K1' #Qxe7
        #correctFen = '4rrk1/1b3pp1/1n3q1p/2p1N3/1pB5/7P/PP3PP1/R2QR1K1' #Rae8
        #correctFen = '4r1k1/1b3rp1/1n3q1p/2p1N3/1p6/7P/PP3PP1/R2QR1K1' #Rxf7
        pgnFormat = 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3 Nb8 d4 Nbd7 c4 c6 cxb5 axb5 Nc3 Bb7 Bg5 b4 Nb1 h6 Bh4 c5 dxe5 Nxe4 Bxe7 Qxe7 exd6 Qf6 Nbd2 Nxd6 Nc4 Nxc4 Bxc4 Nb6 Ne5 Rae8 Bxf7+ Rxf7 Nxf7 Rxe1+ Qxe1 Kxf7 Qe3 Qg5 Qxg5 hxg5 b3 Ke6 a3 Kd6 axb4 cxb4 Ra5 Nd5 f3 Bc8 Kf2 Bf5 Ra7 g6 Ra6+ Kc5 Ke1 Nf4 g3 Nxh3 Kd2 Kb5 Rd6 Kc5 Ra6 Nf2 g4 Bd3 Re6'
        pgnConverter.pgnToFen(pgnFormat.split(' '))
        self.assertEqual(correctFen, pgnConverter.getFen())

    def test_chess_game2(self):
        pgnConverter = pgntofen.PgnToFen()
        pgnConverter.resetBoard()
        correctFen = 'r3k2r/2p1bppp/p3b3/1pn1P3/3q4/8/PPBN1PPP/R1BQ1RK1'#Qxd4
        pgnFormat = 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Nxe4 d4 b5 Bb3 d5 dxe5 Be6 Nbd2 Nc5 c3 Be7 Bc2 d4 Nxd4 Nxd4 cxd4 Qxd4 Nf3 Qxd1 Rxd1 O-O Be3 Rfd8 Rdc1 h6 Nd4 Bd5 f4 Ne6 Nxe6 fxe6 Bg6 Rac8 Bc5 Kf8 Kf2 Bb7 Bxe7+ Kxe7 Rc2 c5 Ke3 c4 a4 Bd5 axb5 axb5 g4 b4 Ra4 Rb8 Be4 b3 Rc3 Bxe4 Kxe4 Rb7 Ke3 Rd1 Rcxc4 Rb1 Ra6 Rxb2 Rcc6 Rb1 Rxe6+ Kf7 Reb6 Rxb6 Rxb6 b2 Kd3 Rf1 Rxb2 Rxf4 Rb7+ Ke6 Rxg7 Kxe5 Ke3 Ra4 Rg6 Ra3+ Kf2 Kf4 Kg2 Rb3 h3 Rb2+ Kf1 Rb1+ Ke2 Rb2+ Ke1 h5 gxh5 Rb5 Rg4+ Kf3'
        correctFen = '8/8/8/1r5P/6R1/5k1P/8/4K3'
        pgnConverter.pgnToFen(pgnFormat.split(' '))
        self.assertEqual(correctFen, pgnConverter.getFen())

    def test_queen_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPQPPPP/RNB1KBNR'
       pgnConverter.pgnToFen(['Qd2']);
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPQPPP/RNB1KBNR'
       pgnConverter.pgnToFen(['Qe2']);
       self.assertEqual(correctFen, pgnConverter.getFen())

    def test_enpassent_move(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       correctFen = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR d4 KQkq'
       pgnConverter.pgnToFen(['d4', 'd6']);
       correctFen = 'rnbqkbnr/ppp1pppp/3p4/8/3P4/8/PPP1PPPP/RNBQKBNR - KQkq'
       self.assertEqual(correctFen, pgnConverter.getFullFen())

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
