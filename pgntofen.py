#!/bin/python
import math

class PgnToFen:
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    whiteToMove = True
    internalChessBoard = [
        'R','N','B','Q','K','B','N','R',
        'P','P','P','P','P','P','P','P',
        '1','1','1','1','1','1','1','1',
        '1','1','1','1','1','1','1','1',
        '1','1','1','1','1','1','1','1',
        '1','1','1','1','1','1','1','1',
        'p','p','p','p','p','p','p','p',
        'r','n','b','q','k','b','n','r']
    enpassant = ''
    castlingRights = 'KQkq'

    def getFullFen(self):
        return self.getFen() + ' ' + self.enpassant

    def getFen(self):
        fenpos = ''
        for n in reversed((8,16,24,32,40,48,56,64)):
            emptyPosLength = 0;
            for i in self.internalChessBoard[n-8:n]:
                if(i is not '1'):
                    if(emptyPosLength is not 0):
                        fenpos = fenpos + str(emptyPosLength);
                        emptyPosLength = 0
                    fenpos = fenpos + i
                else:
                    emptyPosLength = emptyPosLength + 1
            if(emptyPosLength is not 0):
                fenpos = fenpos + str(emptyPosLength);
            fenpos = fenpos + '/'
        fenpos = fenpos[:-1]
        return fenpos

    def printFen(self):
        print self.getFen()

    def pgnToFen(self, moves):
        for move in moves:
            print('MOVE', move)
            self.handleAllmoves(move)
            #self.printFen()
            if(self.whiteToMove):
                self.whiteToMove = False
            else:
                self.whiteToMove = True
        return self


#    def findPiece(self, move):
#        moves = {
#            2: self.simpleMove,
#        }
#        print 'Move:' + move
#        func = moves.get(len(move), self.handleAllmoves)
#        return func(move)

    def handleAllmoves(self, move):
        move = move.replace('+', '')
        move = move.replace('#', '')
        promote = ''
        if(move.find('=') > -1):
            promote = move[-1]
            move = move[:-2]
        if(move.find('-O') != -1):
            self.castelingMove(move)
            return;
        toPosition = move[-2:]
        move = move[:-2]
        if len(move) > 0:
            if move[0] in ['R','N','B','Q','K']:
                officer = move[0]
                move = move[1:]
            else:
                officer = 'P'
        else:
            officer = 'P'
        takes = False
        if 'x' in move:
            takes = True
            move = move[:-1]
        specificRow = ""
        specificCol = ""
        if len(move) > 0:
            if move in ['1','2','3','4','5','6','7','8']:
                specificRow = move
            elif move in ['a','b','c','d','e','f','g','h']:
                specificCol = move
            elif len(move) == 2:
                specificCol = move[0]
                specificRow = move[1]
        if(officer == 'N'):
            self.knightMove(toPosition, specificCol, specificRow)
        elif(officer == 'B'):
            self.bishopMove(toPosition, specificCol, specificRow)
        elif(officer == 'R'):
            self.rookMove(toPosition, specificCol, specificRow)
        elif(officer == 'Q'):
            self.queenMove(toPosition, specificCol, specificRow)
        elif(officer == 'K'):
            self.kingMove(toPosition, specificCol, specificRow)
        elif(officer == 'P'):
            self.pawnMove(toPosition, specificCol, specificRow, takes, promote)

    def castelingMove(self, move):
        if(len(move) == 3): #short castling
            if(self.whiteToMove):
                self.internalChessBoard[7] = '1'
                self.internalChessBoard[6] = 'K'
                self.internalChessBoard[5] = 'R'
                self.internalChessBoard[4] = '1'
                self.castlingRights = self.castlingRights.replace('KQ','')

            else:
                self.internalChessBoard[63] = '1'
                self.internalChessBoard[62] = 'k'
                self.internalChessBoard[61] = 'r'
                self.internalChessBoard[60] = '1'
                self.castlingRights = self.castlingRights.replace('kq', '')
        else: # long castling
            if(self.whiteToMove):
                self.internalChessBoard[0] = '1'
                self.internalChessBoard[2] = 'K'
                self.internalChessBoard[3] = 'R'
                self.internalChessBoard[4] = '1'
                self.castlingRights = self.castlingRights.replace('KQ', '')
            else:
                self.internalChessBoard[60] = '1'
                self.internalChessBoard[59] = 'r'
                self.internalChessBoard[58] = 'k'
                self.internalChessBoard[56] = '1'
                self.castlingRights = self.castlingRights.replace('kq', '')

    def queenMove(self, move, specificCol, specificRow):
        column = move[:1]
        row = move[1:2]
        chessBoardNumber = self.placeOnBoard(row, column)
        piece = 'Q' if self.whiteToMove else 'q'
        possibelPositons = [i for i, pos in enumerate(self.internalChessBoard) if pos == piece]
        self.validQueenMoves(possibelPositons, move, specificCol, specificRow)
        self.internalChessBoard[chessBoardNumber] = piece

    def validQueenMoves(self, posistions, move, specificCol, specificRow):
        newColumn = self.columnToInt(move[:1])
        newRow = self.rowToInt(move[1:2])
        newPos = self.placeOnBoard(newRow + 1, move[:1])
        for pos in posistions:
            (existingRow, existingCol) = self.internalChessBoardPlaceToPlaceOnBoard(pos)
            diffRow = int(existingRow - newRow)
            diffCol = int(self.columnToInt(existingCol) - newColumn)
            if diffRow == 0 or diffCol == 0 or diffRow == diffCol or -diffRow == diffCol or diffRow == -diffCol:
                if not specificCol or specificCol == existingCol:
                    if not specificRow or (int(specificRow) -1) == int(existingRow):
                        xVect = 0
                        yVect = 0
                        if abs(diffRow) > abs(diffCol):
                            xVect = -(diffCol / abs(diffRow))
                            yVect = -(diffRow / abs(diffRow))
                        else:
                            xVect = -(diffCol / abs(diffCol))
                            yVect = -(diffRow / abs(diffCol))
                        checkPos = pos
                        nothingInBetween = True
                        print('newPos', newPos)
                        while(checkPos != newPos):
                            checkPos = checkPos + yVect * 8 + xVect
                            if(checkPos == newPos):
                                continue
                            print('checkPos', checkPos)
                            if self.internalChessBoard[checkPos] != "1":
                                nothingInBetween = False
                        if nothingInBetween:
                            self.internalChessBoard[pos] = "1"
                            return

    def rookMove(self, move, specificCol, specificRow):
        column = move[:1]
        row = move[1:2]
        chessBoardNumber = self.placeOnBoard(row, column)
        piece = 'R' if self.whiteToMove else 'r'
        possibelPositons = [i for i, pos in enumerate(self.internalChessBoard) if pos == piece]
        self.validRookMoves(possibelPositons, move, specificCol, specificRow)
        self.internalChessBoard[chessBoardNumber] = piece

    def validRookMoves(self, posistions, move, specificCol, specificRow):
        newColumn = self.columnToInt(move[:1])
        newRow = self.rowToInt(move[1:2])
        print('newRow', newRow)
        print('newColumn', move[:1])
        newPos = self.placeOnBoard(newRow + 1, move[:1])

        for pos in posistions:
            (existingRow, existingCol) = self.internalChessBoardPlaceToPlaceOnBoard(pos)
            diffRow = int(existingRow - newRow)
            diffCol = int(self.columnToInt(existingCol) - newColumn)
            if diffRow == 0 or diffCol == 0:
                if not specificCol or specificCol == existingCol:
                    if not specificRow or (int(specificRow) -1) == int(existingRow):
                        xVect = 0
                        yVect = 0
                        if abs(diffRow) > abs(diffCol):
                            xVect = -(diffCol / abs(diffRow))
                            yVect = -(diffRow / abs(diffRow))
                        else:
                            xVect = -(diffCol / abs(diffCol))
                            yVect = -(diffRow / abs(diffCol))
                        checkPos = pos
                        nothingInBetween = True
                        print('newPos', newPos)
                        while(checkPos != newPos):
                            checkPos = checkPos + yVect * 8 + xVect
                            if(checkPos == newPos):
                                continue
                            print('checkPos', checkPos)
                            if self.internalChessBoard[checkPos] != "1":
                                nothingInBetween = False
                        if nothingInBetween:
                            if(pos == 0):
                                self.castlingRights = self.castlingRights.replace('Q', '')
                            elif(pos == 63):
                                self.castlingRights = self.castlingRights.replace('k', '')
                            if(pos == 7):
                                self.castlingRights = self.castlingRights.replace('K', '')
                            elif(pos == (63-8)):
                                self.castlingRights = self.castlingRights.replace('q', '')
                            self.internalChessBoard[pos] = "1"
                            return

    def kingMove(self, move, specificCol, specificRow):
        column = move[:1]
        row = move[1:2]
        chessBoardNumber = self.placeOnBoard(row, column)
        piece = 'K' if self.whiteToMove else 'k'
        lostCastleRights = 'Q' if self.whiteToMove else 'q'
        kingPos = [i for i, pos in enumerate(self.internalChessBoard) if pos == piece]
        self.castlingRights = self.castlingRights.replace(piece, '')
        self.castlingRights = self.castlingRights.replace(lostCastleRights, '')
        self.internalChessBoard[chessBoardNumber] = piece
        self.internalChessBoard[kingPos[0]] = '1'


    def bishopMove(self, move, specificCol, specificRow):
        column = move[:1]
        row = move[1:2]
        chessBoardNumber = self.placeOnBoard(row, column)
        piece = 'B' if self.whiteToMove else 'b'
        possibelPositons = [i for i, pos in enumerate(self.internalChessBoard) if pos == piece]
        self.validBishopMoves(possibelPositons, move, specificCol, specificRow)
        self.internalChessBoard[chessBoardNumber] = piece

    def validBishopMoves(self, posistions, move, specificCol, specificRow):
        newColumn = self.columnToInt(move[:1])
        newRow = self.rowToInt(move[1:2])
        newPos = self.placeOnBoard(newRow + 1, move[:1])

        for pos in posistions:
            (existingRow, existingCol) = self.internalChessBoardPlaceToPlaceOnBoard(pos)
            diffRow = int(existingRow - newRow)
            diffCol = int(self.columnToInt(existingCol) - newColumn)
            if diffRow == diffCol or -diffRow == diffCol or diffRow == -diffCol:
                if not specificCol or specificCol == existingCol:
                    if not specificRow or (int(specificRow) -1) == int(existingRow):
                        xVect = 0
                        yVect = 0
                        if abs(diffRow) > abs(diffCol):
                            xVect = -(diffCol / abs(diffRow))
                            yVect = -(diffRow / abs(diffRow))
                        else:
                            xVect = -(diffCol / abs(diffCol))
                            yVect = -(diffRow / abs(diffCol))
                        checkPos = pos
                        nothingInBetween = True
                        print('newPos', newPos)
                        while(checkPos != newPos):
                            checkPos = checkPos + yVect * 8 + xVect
                            if(checkPos == newPos):
                                continue
                            print('checkPos', checkPos)
                            if self.internalChessBoard[checkPos] != "1":
                                nothingInBetween = False
                        if nothingInBetween:
                            self.internalChessBoard[pos] = "1"
                            return

    def knightMove(self, move, specificCol, specificRow):
        column = move[:1]
        row = move[1:2]
        chessBoardNumber = self.placeOnBoard(row, column)
        piece = 'N' if self.whiteToMove else 'n'
        knightPositons = [i for i, pos in enumerate(self.internalChessBoard) if pos == piece]
        self.validKnighMoves(knightPositons, move, specificCol, specificRow)
        self.internalChessBoard[chessBoardNumber] = piece

    def validKnighMoves(self, posistions, move, specificCol, specificRow):
        newColumn = self.columnToInt(move[:1])
        newRow = self.rowToInt(move[1:2])
        for pos in posistions:
            (existingRow, existingCol) = self.internalChessBoardPlaceToPlaceOnBoard(pos)
            validatePos = str(int(existingRow - newRow)) + str(int(self.columnToInt(existingCol) - newColumn))
            if validatePos in ['2-1','21','1-2','12','-1-2','-12','-2-1','-21']:
                if not specificCol or specificCol == existingCol:
                    if not specificRow or (int(specificRow) -1) == int(existingRow):
                        self.internalChessBoard[pos] = "1"
                        return

    def pawnMove(self, toPosition, specificCol, specificRow, takes, promote):
        column = toPosition[:1]
        row = toPosition[1:2]
        chessBoardNumber = self.placeOnBoard(row, column)
        if(promote):
            piece = promote if self.whiteToMove else promote
        else:
            piece = 'P' if self.whiteToMove else 'p'
        self.internalChessBoard[chessBoardNumber] = piece
        if(takes):
            removeFromRow = (int(row) - 1) if self.whiteToMove else (int(row) + 1)
            posistion = self.placeOnBoard(removeFromRow, specificCol)
            piece = self.internalChessBoard[posistion] = '1'
        else:
            #run piece one more time if case of promotion
            piece = 'P' if self.whiteToMove else 'p'
            self.updateOldLinePos(piece,chessBoardNumber)


    def updateOldLinePos(self, char, posistion):
        startPos = posistion
        counter = 0;
        piece = ''
        while(posistion >= 0 and posistion < 64):
            step = 8
            if(piece == char):
                if(abs(posistion - startPos) > 10):
                    (row, column) = self.internalChessBoardPlaceToPlaceOnBoard(startPos)
                    self.enpassant = str(column) + str(int(row)+1)
                else:
                    self.enpassant = '-'
                piece = self.internalChessBoard[posistion] = '1'
                return;
            else:
                if(self.whiteToMove == True):
                    posistion = posistion - step
                else:
                    posistion = posistion + step
                piece = self.internalChessBoard[posistion]


    def placeOnBoard(self, row, column):
        # returns internalChessBoard place
        return 8 * (int(row) - 1) + self.columnToInt(column);

    def internalChessBoardPlaceToPlaceOnBoard(self, chessPos):
        column = int(chessPos) % 8
        row = math.ceil(chessPos/8)
        return (row, self.intToColum(column))

    def rowToInt(self, n):
        return int(n)-1

    def columnToInt(self, char):
        # TODO: char.toLowerCase???
        if(char == 'a'):
            return 0
        elif(char == 'b'):
            return 1
        elif(char == 'c'):
            return 2
        elif(char == 'd'):
            return 3
        elif(char == 'e'):
            return 4
        elif(char == 'f'):
            return 5
        elif(char == 'g'):
            return 6
        elif(char == 'h'):
            return 7

    def intToColum(self, num):
        # TODO: char.toLowerCase???
        if(num == 0):
            return 'a'
        elif(num == 1):
            return 'b'
        elif(num == 2):
            return 'c'
        elif(num == 3):
            return 'd'
        elif(num == 4):
            return 'e'
        elif(num == 5):
            return 'f'
        elif(num == 6):
            return 'g'
        elif(num == 7):
            return 'h'

    def resetBoard(self):
        self.fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        self.whiteToMove = True
        self.enpassant = ''
        self.internalChessBoard = [
            'R','N','B','Q','K','B','N','R',
            'P','P','P','P','P','P','P','P',
            '1','1','1','1','1','1','1','1',
            '1','1','1','1','1','1','1','1',
            '1','1','1','1','1','1','1','1',
            '1','1','1','1','1','1','1','1',
            'p','p','p','p','p','p','p','p',
            'r','n','b','q','k','b','n','r']


if __name__ == "__main__":
    pgnFormat = 'e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3 Nb8 d4 Nbd7 c4 c6 cxb5 axb5 Nc3 Bb7 Bg5 b4 Nb1 h6 Bh4 c5 dxe5 Nxe4 Bxe7 Qxe7 exd6 Qf6 Nbd2 Nxd6 Nc4 Nxc4 Bxc4 Nb6 Ne5 Rae8 Bxf7+ Rxf7 Nxf7 Rxe1+ Qxe1 Kxf7 Qe3 Qg5 Qxg5 hxg5 b3 Ke6 a3 Kd6 axb4 cxb4 Ra5 Nd5 f3 Bc8 Kf2 Bf5 Ra7 g6 Ra6+ Kc5 Ke1 Nf4 g3 Nxh3 Kd2 Kb5 Rd6 Kc5 Ra6 Nf2 g4 Bd3 Re6'
    #pgnFormat = 'e4 e5 Nf3 Nc6 Bb5 a6'
    #final FEN: 8/8/4R1p1/2k3p1/1p4P1/1P1b1P2/3K1n2/8 b - - 2 43
    #TODO: remember to fix R in front.
    converter = PgnToFen()
    converter.pgnToFen(pgnFormat.split(' '))
