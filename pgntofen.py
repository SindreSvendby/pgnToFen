#!/bin/python
from __future__ import print_function
from functools import partial
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
    enpassant = '-'
    castlingRights = 'KQkq'

    def getFullFen(self):
        return self.getFen() + ' ' + ('w ' if self.whiteToMove else 'b ') + self.enpassant + ' ' + (self.castlingRights if self.castlingRights else '-')

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
        print(self.getFen())

    def pgnToFen(self, moves):
        loopC = 1
        for move in moves:
            #self.printBoard()
            #print('TO MOVE:', 'w' if self.whiteToMove else 'b')
            #print('MOVE:', move)
            #print('Movenumber',loopC)
            self.move(move)
            #self.printFen()
            loopC = loopC + 1
        return self

    def move(self, move):
        self.handleAllmoves(move)
        if(self.whiteToMove):
            self.whiteToMove = False
        else:
            self.whiteToMove = True
        return self

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
        if(officer != 'P'):
            self.enpassant = '-'
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
                        while(checkPos != newPos):
                            checkPos = checkPos + yVect * 8 + xVect
                            if(checkPos == newPos):
                                continue
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
        newPos = self.placeOnBoard(newRow + 1, move[:1])
        potensialPosisitionsToRemove=[]
        for pos in posistions:
            print('checking posistion', pos)
            (existingRow, existingCol) = self.internalChessBoardPlaceToPlaceOnBoard(pos)
            print('existingRow', existingRow)
            print('existingCol', existingCol)
            diffRow = int(existingRow - newRow)
            diffCol = int(self.columnToInt(existingCol) - newColumn)
            print('diffRow', diffRow)
            print('diffCol', diffCol)
            print('posistion ' + str(pos) + ' (' + str(existingCol) + str(int(existingRow) + 1) + ')')
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
                        while(checkPos != newPos):
                            checkPos = checkPos + yVect * 8 + xVect
                            if(checkPos == newPos):
                                continue
                            if self.internalChessBoard[checkPos] != "1":
                                print('Something in between')
                                nothingInBetween = False
                        if nothingInBetween:
                            print('Nothing in between')
                            potensialPosisitionsToRemove.append(pos)
        if len(potensialPosisitionsToRemove) == 1:
            print("Only one piece valid")
            correctPos = potensialPosisitionsToRemove[0];
        else:
            print("Several valid posisitions")
            if len(potensialPosisitionsToRemove) == 0:
                raise ValueError('Cant find a valid posistion to remove', potensialPosisitionsToRemove)
            notInCheckLineBindNewPos = partial(self.notInCheckLine, self.posOnBoard('K'))
            correctPosToRemove = filter(notInCheckLineBindNewPos, potensialPosisitionsToRemove)
            if len(correctPosToRemove) > 1:
                raise ValueError('Several valid positions to remove from the board')
            correctPos = correctPosToRemove[0]
        if(correctPos == 0):
            self.castlingRights = self.castlingRights.replace('Q', '')
        elif(correctPos == 63):
            self.castlingRights = self.castlingRights.replace('k', '')
        elif(correctPos == 7):
            self.castlingRights = self.castlingRights.replace('K', '')
        elif(correctPos == (63-8)):
            self.castlingRights = self.castlingRights.replace('q', '')
        print('Posistion to remove' + str(correctPos))
        self.internalChessBoard[correctPos] = "1"
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
                        while(checkPos != newPos):
                            checkPos = checkPos + yVect * 8 + xVect
                            if(checkPos == newPos):
                                continue
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
            piece = promote if self.whiteToMove else promote.lower()
        else:
            piece = 'P' if self.whiteToMove else 'p'
        self.internalChessBoard[chessBoardNumber] = piece
        if(takes):
            removeFromRow = (int(row) - 1) if self.whiteToMove else (int(row) + 1)
            posistion = self.placeOnBoard(removeFromRow, specificCol)
            piece = self.internalChessBoard[posistion] = '1'
            if(self.enpassant != '-'):
                enpassantPos = self.placeOnBoard(self.enpassant[1], self.enpassant[0])
                toPositionPos = self.placeOnBoard(toPosition[1], toPosition[0])
                if(self.enpassant == toPosition):
                    if(self.whiteToMove == True):
                        self.internalChessBoard[chessBoardNumber - 8] = '1'
                    else:
                        self.internalChessBoard[chessBoardNumber + 8] = '1'
                        return

        else:
            #run piece one more time if case of promotion
            piece = 'P' if self.whiteToMove else 'p'
            self.updateOldLinePos(piece,chessBoardNumber, toPosition)


    def updateOldLinePos(self, char, posistion, toPosition):
        startPos = posistion
        counter = 0;
        piece = ''
        step = 8
        while(posistion >= 0 and posistion < 64):
            if(piece == char):
                if(abs(posistion - startPos) > 10):
                    (row, column) = self.internalChessBoardPlaceToPlaceOnBoard(startPos)
                    rowAdjustedByColor = -1 if self.whiteToMove else 1
                    enpassant = str(column) + str(int(row) + 1 + rowAdjustedByColor)
                    self.enpassant = enpassant
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
        self.enpassant = '-'
        self.internalChessBoard = [
            'R','N','B','Q','K','B','N','R',
            'P','P','P','P','P','P','P','P',
            '1','1','1','1','1','1','1','1',
            '1','1','1','1','1','1','1','1',
            '1','1','1','1','1','1','1','1',
            '1','1','1','1','1','1','1','1',
            'p','p','p','p','p','p','p','p',
            'r','n','b','q','k','b','n','r']

    def printBoard(self):
        loop = 1
        for i in self.internalChessBoard:
            print(i, end=' ')
            if(loop%8 == 0):
                print()
            loop = loop + 1

    def notInCheckLine(self, kingPos, piecePos):
        """
            Verifies that the piece is not standing in "line of fire" between and enemy piece and your king as the only piece
            :returns: True if the piece can move
        """
        return self.checkLine(kingPos, piecePos)

    def checkLine(self, kingPos, piecePos):
        (kingRowInt, kingColumn) = self.internalChessBoardPlaceToPlaceOnBoard(kingPos)
        kingColumnInt = self.columnToInt(kingColumn)
        (pieceRowInt, pieceColumn) = self.internalChessBoardPlaceToPlaceOnBoard(piecePos);
        pieceColumnInt = self.columnToInt(pieceColumn)

        print('kingPos: column', kingColumnInt)
        print('kingPos: row', kingRowInt)

        print('linePiecePos: column', pieceColumnInt)
        print('linePiecePos: row', pieceRowInt)

        diffRow = int(kingRowInt - pieceRowInt)
        diffCol = int(kingColumnInt - pieceColumnInt)
        xVect = 0
        yVect = 0
        if abs(diffRow) > abs(diffCol):
            xVect = (diffCol / abs(diffRow))
            yVect = -(diffRow / abs(diffRow))
        else:
            xVect = -(diffCol / abs(diffCol))
            yVect = -(diffRow / abs(diffCol))
        print('Direction: ' + str(xVect) + ',' + str(yVect))
        checkPos = kingPos
        nothingInBetween = True
        while(checkPos != piecePos):
            checkPos = checkPos + yVect * 8 + xVect
            print('Checkpos: ', checkPos)
            if(checkPos == piecePos):
                continue
            if self.internalChessBoard[checkPos] != "1":
                print('Something between king and piece, returning a false value')
                # Piece between the king and the piece can not be a self-disvoery-check.
                return True
        # No piece between the king and the piece, need to verify if an enemy piece with the possibily to go that  direction exist
        print('Nothing between king(' + str(kingPos) + ') and piece(' + str(piecePos) + ')')
        print("let's check for a enemy piece between piece(" + str(piecePos) + ") and end of board")
        if(xVect in (1, -1) and yVect == 0):
            columnNr = (piecePos % 8)
            if(xVect == 1):
                endOfBoard = piecePos + 7 - columnNr
            else: # xVect -1
                endOfBoard = piecePos - 7 - columnNr
        elif(yVect in (1, -1) and xVect == 0):
            endOfBoard = 63 # will get smallere then 0 or highere then 63, no need to hande this
        elif(xVect == 0 and yVect == 0):
            raise ValueError('xVect and yVect are both 0...???')
        else:
            columnNr = (piecePos % 8)
            if(xVect == 1):
                columnsLeft = 7- columnNr
            else:
                columnsLeft = columnNr
            posInMove = (yVect * 8) + xVect
            endOfBoard = piecePos + posInMove * columnsLeft


        while checkPos >= 0 and checkPos < 64 and checkPos <= endOfBoard:
            checkPos = checkPos + yVect * 8 + xVect
            if(checkPos < 0 or checkPos > 63 or checkPos > endOfBoard):
                continue
            print('Checkpos: ', checkPos)
            print('endOfBoard', endOfBoard)
            if self.internalChessBoard[checkPos] == "1":
                print('empty space, continue: ', checkPos)
                continue
            elif self.internalChessBoard[checkPos] in self.getOppositePieces(["Q", "R"]) and (xVect == 0 or yVect == 0):
                print('Found a : ', self.internalChessBoard[checkPos], 'on the line')
                return False
            elif self.internalChessBoard[checkPos] in self.getOppositePieces(["Q", "B"]) and True:
                print('Found a : ', self.internalChessBoard[checkPos], 'in the diagonal')
                #TODO: check direction
                return False
            else:
                print('WTF, piece on board is:', self.internalChessBoard[checkPos], checkPos)
        print('Valid piece to move', piecePos)
        return True

    def getOppositePieces(self, pieces):
            """"
                Takes a list of pieces and returns it in uppercase if blacks turn, or lowercase if white.
            """
            return map(lambda p: p.lower() if self.whiteToMove else p.upper(), pieces)


    def posOnBoard(self, piece):
        """
            :param piece: a case _sensitiv_ one letter string. Valid 'K', 'Q', 'N', 'P', 'B', 'R', will be transformed to lowercase if it's black's turn to move
            :return int|[int]: Returns the posistion(s) on the board for a piece, if only one pos, a int is return, else a list of int is returned
        """
        correctPiece = piece if self.whiteToMove else piece.lower()
        posistionsOnBoard = [i for i, pos in enumerate(self.internalChessBoard) if pos == correctPiece]
        if len(posistionsOnBoard) == 1:
            return posistionsOnBoard[0]
        else:
            return posistionsOnBoard

if __name__ == "__main__":
    pgnFormat = 'c4 Nc6 Nc3 e5 Nf3 Nf6 g3 d5 cxd5 Nxd5 Bg2 Nb6 O-O Be7 a3 Be6 b4 a5 b5 Nd4 Nxd4 exd4 Na4 Bd5 Nxb6 cxb6 Bxd5'
    converter = PgnToFen()
    for move in pgnFormat.split(' '):
        converter.move(move)
        print(converter.getFullFen())
