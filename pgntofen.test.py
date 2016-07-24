#!/bin/python
# coding=utf8
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
       pgnConverter.moves(['Nf3','Nf6']);
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
       correctFen = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b d3 KQkq'
       pgnConverter.pgnToFen(['d4']);
       self.assertEqual(correctFen, pgnConverter.getFullFen())

    def test_self_discovery_chek_rook_move_diagonal(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.internalChessBoard = [
           'K','1','1','1','1','1','1','R',
           '1','1','1','1','1','1','1','1',
           '1','1','R','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','q','1',
           '1','1','1','1','1','1','1','1']
       pgnConverter.pgnToFen(['Rc1']);
       correctFen = '8/6q1/8/8/8/2R5/8/K1R5 b - Qkq'
       self.assertEqual(correctFen, pgnConverter.getFullFen())

    def test_self_discovery_chek_rook_move_line(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.internalChessBoard = [
           'K','1','R','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           'R','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           'q','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','1','1']
       pgnConverter.pgnToFen(['Rc3']);
       correctFen = '8/q7/8/8/8/R1R5/8/K7 b - KQkq'
       self.assertEqual(correctFen, pgnConverter.getFullFen())

    def test_self_discovery_chek_rook_move_diagnal_another_pos(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.internalChessBoard = [
           '1','1','1','K','1','1','1','1',
           '1','1','R','1','1','1','1','1',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','1','1','R','1',
           '1','1','1','1','1','1','1','q',
           '1','1','1','1','1','1','1','1',
           '1','1','1','1','q','1','1','1',
           '1','1','1','1','1','1','1','1']
       pgnConverter.pgnToFen(['Rc4']);
       correctFen = '8/4q3/8/7q/2R3R1/8/8/3K4 b - KQkq'
       self.assertEqual(correctFen, pgnConverter.getFullFen())

    def test_full_game_3(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       moves = "e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 Nc6 Bg5 e5 Bxf6 gxf6 Nf5 Bxf5 exf5 Be7 Nd5 O-O c3 Kh8 Bd3 Nb8 O-O Nd7 Be4 Nb6 Nxb6 Qxb6 Qb3 Qc7 Bd5 Bd8 Rad1 Qd7 Rd3 Qxf5 Rf3 Qg6 Qxb7 Bb6 Be4 Qg4 Bxh7 Kxh7 Rh3+ Qxh3 gxh3 f5 Kh1 Rae8 Rg1 Bxf2 Rg2 Be3 Qf3 Bh6 Qxf5+ Kh8 Qf6+ Kh7 Qxd6 e4 Rg4 Re6 Qc5 e3 Qf5+ Kh8 Re4 Rg6 Rg4 Re6 Re4 Rg6 Rh4 Kg7 Qe5+ Kg8 Rg4 Kh7 Qe4 Rg8 Qf5 Rf8 Kg2 Kg7 Kf3 Kh8 Qe5+ Kh7 Qe4 Kh8 Ke2 Re6 Qd4+ Kh7 Qxa7 Rf6 Qd4 Rf2+ Ke1 Re8 Qd3+ Kh8 Qd6 Kh7 Rh4 Re6 Qd3+ Kh8 Qd4+ Kh7 Qd3+ Kh8 Rxh6+ Rxh6 Qxe3 Rff6 Qd4 Kg8 a4 Re6+ Kf2 Ref6+ Kg3 Rhg6+ Kh4 Rd6 Qe4 Rde6 Qa8+ Kg7 Qd5 Re2 Qd4+ Kh7 Qf4 Kg8 Qb8+ Kg7 Qf4 Reg2 Qd4+ Kh7 Qe4 Rxb2 a5 Rb8 a6 Rh8 Qe5 Kg8+"
       pgnConverter.moves(moves.split(' '));
       correctFen = '6kr/5p2/P5r1/4Q3/7K/2P4P/7P/8 w - -'
       self.assertEqual(correctFen, pgnConverter.getFullFen())

    def test_file_accecpt_file(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       file = "test/Carlsen.pgn"
       stats =  pgnConverter.pgnFile(file);
       self.assertEqual(len(stats['failed']), 0)
       self.assertEqual(len(stats['succeeded']), 1974)

    def test_moves_accecpt_str(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       moves = "1.e4 c5 2.Nf3 d6 1/2-1/2"
       pgnConverter.moves(moves);
       correctFen = 'rnbqkbnr/pp2pppp/3p4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w - KQkq'
       self.assertEqual(correctFen, pgnConverter.getFullFen())

    def test_real_example_self_discovery_chess(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       pgnConverter.internalChessBoard = [
           '1','1','1','1','1','1','1','K',
           'P','P','1','1','1','1','1','P',
           '1','1','P','1','p','1','1','P',
           '1','1','1','1','Q','1','R','1',
           '1','1','1','1','1','1','1','q',
           '1','1','1','1','1','1','r','b',
           'p','1','1','1','1','p','1','k',
           '1','1','1','1','1','r','1','1']
       pgnConverter.whiteToMove = False

       pgnConverter.pgnToFen(['Rg8']);
       correctFen = '6r1/p4p1k/6rb/7q/4Q1R1/2P1p2P/PP5P/7K w - KQkq'
       self.assertEqual(correctFen, pgnConverter.getFullFen())

    def test_game_4(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       moves = 'd4 d5 c4 c6 Nf3 Nf6 Nc3 e6 e3 Nbd7 Qc2 Bd6 b3 O-O Be2 b6 Bb2 Qe7 O-O Bb7 Rfe1 Rfe8 Rad1 Rad8 Bf1 Bb4 a3 Bxa3 Bxa3 Qxa3 cxd5 exd5 Ra1 Qd6 Rxa7 Qb8 Rea1 c5 b4 cxd4 Nxd4 Rc8 Qb3 Ne5 h3 g6 Be2 Re7 R7a2 Nc4 Rd1 Nxe3 fxe3 Rxe3 Rd3 Qg3 Nd1 Qe1+ Bf1 Rxd3 Qxd3 Qxb4 Qd2 Qd6 Nf3 Ne4 Qd4 Rc1 Rb2 Qc5 Ne3 Ba6 Rxb6 Qxd4 Nxd4 Bxf1 Nxf1 Nd2 Rf6 Rd1 Ne2 d4 Ng3 h5 Rf2 Nb1 Rb2 f5 Nh1 Nc3 Rd2 Ra1 h4 Kg7 Ng3 Ra4 Nh2 Ne4 Rd3 Nxg3 Rxg3 d3 Rxd3 Rxh4 Rd7+ Kh6 Nf3 Re4 Rd6 Kg7 Kh2 Kh6 Nd4 Rh4+ Kg3 Rg4+ Kh3 Kg7 g3 Kf7 Nf3 Ke7 Ra6 f4 gxf4 Rxf4 Ne5 Re4 Nxg6+'
       pgnConverter.pgnToFen(moves.split());
       correctFen = '8/4k3/R5N1/7p/4r3/7K/8/8 b - -'
       self.assertEqual(correctFen, pgnConverter.getFullFen())

    def test_game_5(self):
       pgnConverter = pgntofen.PgnToFen()
       pgnConverter.resetBoard()
       moves = 'e4 d6 d4 Nf6 Nc3 e5 dxe5 dxe5 Qxd8+ Kxd8 Nf3 Bd6 Bg5 Be6 O-O-O Nd7 Nb5 Ke7 Nxd6 cxd6 Bb5 Rhd8 Nd2 h6 Bh4 g5 Bg3 a6 Bxd7 Rxd7         f3 Rc8 Kb1 Nh5 Nf1 f5 exf5 Bxf5 Ne3 Bg6 Rd2 Ke6 b3 b5         Kb2 d5 Re1 Nxg3 hxg3 h5 c3 d4 cxd4 Rxd4 Rxd4 exd4 Nc2+ Kd5         Nb4+ Kd6 Rc1 Rxc1 Kxc1 h4 gxh4 gxh4 Nxa6 Bd3 Nb4 Bf1 Kd2 Bxg2         Ke2 Bh3 a4 Bf5 axb5 d3+ Ke3 h3 Nxd3 Bxd3 Kd4'
       pgnConverter.pgnToFen(moves.split());
       correctFen = '8/8/3k4/1P6/3K4/1P1b1P1p/8/8 b - -'
       self.assertEqual(correctFen, pgnConverter.getFullFen())


    def test_real_example_self_discovery_chess2(self):
        pgnConverter = pgntofen.PgnToFen()
        pgnConverter.resetBoard()
        pgnConverter.internalChessBoard = [
            '1', '1', 'K', 'R', '1', 'B', '1', 'R',
            'P', 'P', 'P', '1', '1', 'P', 'P', 'P',
            '1', '1', 'N', '1', '1', 'N', '1', '1',
            '1', '1', '1', '1', 'P', '1', '1', '1',
            '1', '1', '1', '1', 'p', '1', 'B', '1',
            '1', '1', '1', 'b', 'b', 'n', '1', '1',
            'p', 'p', 'p', '1', '1', 'p', 'p', 'p',
            'r', 'n', '1', 'k', '1', '1', '1', 'r']
        pgnConverter.whiteToMove = False
        pgnConverter.pgnToFen(['Nd7']);
        correctFen = 'r2k3r/pppn1ppp/3bbn2/4p1B1/4P3/2N2N2/PPP2PPP/2KR1B1R w - KQkq'
        self.assertEqual(correctFen, pgnConverter.getFullFen())


if __name__ == '__main__':
    unittest.main()
