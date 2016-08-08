#!/bin/python
# coding=utf8
from __future__ import print_function
from functools import partial
import math
import re
import os
import numpy as np

class PgnToFen:
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    whiteToMove = True
    internalChessBoard =  np.array([
        ['R','N','B','Q','K','B','N','R'],
        ['P','P','P','P','P','P','P','P'],
        ['1','1','1','1','1','1','1','1'],
        ['1','1','1','1','1','1','1','1'],
        ['1','1','1','1','1','1','1','1'],
        ['1','1','1','1','1','1','1','1'],
        ['p','p','p','p','p','p','p','p'],
        ['r','n','b','q','k','b','n','r']])
    enpassant = '-'
    castlingRights = 'KQkq'
    DEBUG = False
    lastMove = 'Before first move'
    fens = []
    result = ''

    def getFullFen(self):
        return self.getFen() + ' ' + ('w ' if self.whiteToMove else 'b ') + self.enpassant + ' ' + (self.castlingRights if self.castlingRights else '-')

    def getFen(self):
        fenpos = ''
        for row in reversed(self.internalChessBoard):
            emptyPosLength = 0;
            for i in row:
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

    def moves(self, moves):
        if isinstance(moves, str):
            nrReCompile = re.compile('[0-9]+\.')
            transformedMoves = nrReCompile.sub('', moves)
            pgnMoves = transformedMoves.split(' ')
            # In test/Carlsen.png its two spaces before the result. Not sure if this is accourding to documentations, this could be a very fragile solution
            # print('pgnMoves[-2:]', pgnMoves[-2:])
            validResults = ['1/2-1/2', '1-0', '0-1']
            result = [r for r in pgnMoves[-2:] if r in validResults]
            # print('result', result)
            self.result = result[0]
            pgnMoves = [move for move in pgnMoves[1:-2] if move != '']
            # print('pgnMoves', pgnMoves)
            return self.pgnToFen(pgnMoves)
        else:
            return self.pgnToFen(moves)

    def pgnFile(self, file):
        pgnGames = {
        'failed' : [],
        'succeeded' : [],
        }
        started = False
        game_info = []
        pgnMoves = ''
        for moves in open(file, 'rt').readlines():

            if moves[:1] == '[':
                #print('game_info line: ', moves)
                game_info.append(moves)
                continue
            if moves[:2] == '1.':
                started = True
            if (moves == '\n' or moves == '\r\n') and started:
                # try:
                    #print('Processing ', game_info[0:6])
                pgnToFen = PgnToFen()
                pgnToFen.resetBoard()
                # print('MOVES:', pgnMoves)
                fens = pgnToFen.moves(pgnMoves).getAllFens()
                pgnGames['succeeded'].append((game_info, fens))
                # except ValueError as e:
                #     pgnGames['failed'].append((game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e))
                # except TypeError as e:
                #     pgnGames['failed'].append((game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e))
                # except IndexError as e:
                #     # raise IndexError(game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e)
                #     pgnGames['failed'].append((game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e))
                # except ZeroDivisionError as e:
                #     pgnGames['failed'].append((game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e))
                # finally:
                started = False
                game_info = []
                pgnMoves = ''
            if(started):
                pgnMoves = pgnMoves + ' ' + moves.replace('\n', '').replace('\r', '')
        return pgnGames



    def pgnToFen(self, moves):
        # try:
        loopC = 1
        for move in moves:
            self.lastMove = move
            self.DEBUG and print('=========')
            self.DEBUG and print('Movenumber',loopC)
            self.DEBUG and print('TO MOVE:', 'w' if self.whiteToMove else 'b')
            self.DEBUG and print('MOVE:', move)
            self.move(move)
            self.DEBUG and print('after move:')
            self.DEBUG and print(self.getFullFen())
            self.DEBUG and self.printBoard()
            loopC = loopC + 1
            self.fens.append(self.getFullFen())
        self.sucess = True
        return self
        # except ValueError as e:
        #     print('Converting PGN to FEN failed.', e)
        #     print(e)
        #     print('Move that failed:', self.lastMove)
        #     self.printBoard()
        #     print(self.getFullFen())
        #     self.fens = []
        #     self.sucess = False

    def move(self, move):
        if not move:
            return self
        self.lastMove = move
        self.handleAllmoves(move)
        if(self.whiteToMove):
            self.whiteToMove = False
        else:
            self.whiteToMove = True
        return self

    def getAllFens(self):
        return self.fens

    def handleAllmoves(self, move):
        # print('handleAllmoves', move)
        move = move.replace('+', '')
        move = move.replace('#', '')
        promote = ''
        # Check if last part is a Q,R or N, it's a common mistake to skip the =
        if move[-1] in ('Q', 'R', 'N') and move.find('=') == -1:
            promote = move[-1]
            move = move[:-1]

        if move.find('=') > -1:
            promote = move[-1]
            move = move[:-2]

        if move.find('-O') != -1:
            self.castelingMove(move)
            return;

        toPosition = move[-2:]
        move = move[:-2]
        if len(move) > 0:
            if move[0] in ['R','N','B','Q','K']:
                piece = move[0]
                move = move[1:]
            else:
                piece = 'P'
        else:
            piece = 'P'
        takes = False
        if 'x' in move:
            takes = True
            move = move[:-1]
        specificRow = None
        specificCol = None
        if len(move) > 0:
            if move in ['1','2','3','4','5','6','7','8']:
                specificRow = move
            elif move in ['a','b','c','d','e','f','g','h']:
                specificCol = move
            elif len(move) == 2:
                specificCol = move[0]
                specificRow = move[1]

        if(piece == 'P'):
            self.pawnMove(toPosition, specificCol, specificRow, takes, promote)
            return
        elif(piece != 'P'):
            self.enpassant = '-'

        if(piece == 'K'):
            self.kingMove(toPosition)
            return

        # Only office moves from here on out, Pawns and King are taken care of.
        piece = piece if self.whiteToMove else piece.lower()

        # Update old pos sections
        posistions = self.posOnBoard(piece)
        if not type(posistions) is list:
            correctOldPos = posistions
        else:
            if piece in ['N', 'n']:
                possiblePositionsToMove = self.validKnightPosistions(posistions, toPosition, specificCol, specificRow)
            else:
                ## We use same algo. to detect changes for R, Q and B.
                # print('before possiblePositionsToMove', posistions)
                possiblePositionsToMove = self.findOldPosOfficer(piece, posistions, toPosition, specificCol, specificRow)
            # check for self discovered check.
            # print('before removeSelfCheckMovesAndReturnOnlyLegalPosToUpdate', possiblePositionsToMove)
            correctOldPos = self.removeSelfCheckMovesAndReturnOnlyLegalPosToUpdate(possiblePositionsToMove)
        self.setPieceInternal(correctOldPos, "1")

        # Update new pos, should be done after removing old pos, so the board do not contain to many occurens
        self.setPiece(toPosition,piece)

        # Spesial cases:
        if piece == 'R':
            if(correctOldPos['row'] == 0 and correctOldPos['column'] == 0):
                self.castlingRights = self.castlingRights.replace('Q', '')
            elif(correctOldPos['row'] == 0 and correctOldPos['column'] == 7):
                self.castlingRights = self.castlingRights.replace('K', '')
        elif piece == 'r':
            if(correctOldPos['row'] == 7 and correctOldPos['column'] == 0):
                self.castlingRights = self.castlingRights.replace('k', '')
            elif(correctOldPos['row'] == 7 and correctOldPos['column'] == 7):
                self.castlingRights = self.castlingRights.replace('q', '')

    def castelingMove(self, move):
        if(len(move) == 3): #short castling
            if(self.whiteToMove):
                self.internalChessBoard[0][7] = '1'
                self.internalChessBoard[0][6] = 'K'
                self.internalChessBoard[0][5] = 'R'
                self.internalChessBoard[0][4] = '1'
                self.castlingRights = self.castlingRights.replace('KQ','')
            else:
                self.internalChessBoard[7][7] = '1'
                self.internalChessBoard[7][6] = 'k'
                self.internalChessBoard[7][5] = 'r'
                self.internalChessBoard[7][4] = '1'
                self.castlingRights = self.castlingRights.replace('kq', '')
        else: # long castling
            if(self.whiteToMove):
                self.internalChessBoard[0][0] = '1'
                self.internalChessBoard[0][2] = 'K'
                self.internalChessBoard[0][3] = 'R'
                self.internalChessBoard[0][4] = '1'
                self.castlingRights = self.castlingRights.replace('KQ', '')
            else:
                self.internalChessBoard[7][0] = '1'
                self.internalChessBoard[7][2] = 'k'
                self.internalChessBoard[7][3] = 'r'
                self.internalChessBoard[7][4] = '1'
                self.castlingRights = self.castlingRights.replace('kq', '')

    def findOldPosOfficer(self, piece, posistions, move, specificCol, specificRow):
        if specificCol is not None:
            specificCol = self.__columnToInt(specificCol)
        if specificRow is not None:
            specificRow = self.__rowToInt(specificRow)
        (newColumn, newRow) = self.__getColumnRowFromSquare(move)
        newPos = {'column': newColumn, 'row': newRow}
        potensialPosisitionsToRemove=[]
        for pos in posistions:
            diffRow = int(pos['row'] - newRow)
            diffCol = int(pos['column'] - newColumn)
            if diffRow == 0 or diffCol == 0 or abs(diffRow) == abs(diffCol):
                if piece in ['R', 'r'] and (diffRow != 0 and diffCol != 0):
                    continue
                if piece in ['B', 'b'] and (abs(diffRow) != abs(diffCol)):
                    continue
                if type(specificCol) is int and (pos['column'] is None or specificCol != pos['column']):
                    continue
                if type(specificRow) is int and int(specificRow) != int(pos['row']):
                    continue
                columnVect = 0
                rowVect = 0

                if abs(diffRow) > abs(diffCol):
                    columnVect = -int((diffCol / abs(diffRow)))
                    rowVect = -int((diffRow / abs(diffRow)))
                else:
                    columnVect = -int((diffCol / abs(diffCol)))
                    rowVect = -int((diffRow / abs(diffCol)))
                # Need to copy so we do not change pos later when we change checkPos
                checkPos = pos.copy()
                nothingInBetween = True
                (c, r) = self.__getColumnRowFromSquare(move)
                while nothingInBetween and not self.isSamePos({'column':c, 'row':r}, checkPos):
                    checkPos['column'] += columnVect
                    checkPos['row'] += rowVect
                    if self.isSamePos({'column':c, 'row':r}, checkPos):
                        continue
                    if self.getPieceInternal(checkPos) != '1':
                        nothingInBetween = False
                if nothingInBetween:
                    potensialPosisitionsToRemove.append(pos)
        return potensialPosisitionsToRemove

    def isSamePos(self, pos1, pos2):
        return pos1['row'] == pos2['row'] and pos1['column'] == pos2['column']

    def removeSelfCheckMovesAndReturnOnlyLegalPosToUpdate(self, positions):
        if type(positions) is list and len(positions) == 1:
            return positions[0];
        else:
            if len(positions) == 0:
                raise ValueError('Cant find a valid posistion to remove', positions)
            notInCheckLineBindNewPos = partial(self.notInCheckLine, self.posOnBoard('K'))
            correctPosToRemove = list(filter(notInCheckLineBindNewPos, positions))
            # print(correctPosToRemove)
            if len(correctPosToRemove) > 1:
                raise ValueError('Several valid positions to remove from the board')
            if len(correctPosToRemove) == 0:
                raise ValueError('None valid positions to remove from the board')
            return correctPosToRemove[0]

    def kingMove(self, move):
        piece = 'K' if self.whiteToMove else 'k'
        # Remove the old pos.
        kingPos = self.posOnBoard(piece)
        self.setPieceInternal(kingPos, '1')

        # Update the postions the king is going to
        self.setPiece(move, piece)


        # Adjust castling premissions
        lostCastleRights = 'Q' if self.whiteToMove else 'q'
        self.castlingRights = self.castlingRights.replace(piece, '')
        self.castlingRights = self.castlingRights.replace(lostCastleRights, '')

    def validKnightPosistions(self, posistions, move, specificCol, specificRow):
        newColumn = self.__columnToInt(move[0])
        newRow = self.__rowToInt(move[1])
        potensialPosisitionsToRemove = []
        for pos in posistions:
            knightOnColum = self.intToColum(pos['column'])
            validatePos = str(int(pos['row']) - newRow) + str(pos['column'] - newColumn)
            if validatePos in ['2-1','21','1-2','12','-1-2','-12','-2-1','-21']:
                if not specificCol or specificCol == knightOnColum:
                    if not specificRow or (int(specificRow) -1) == int(pos['row']):
                            potensialPosisitionsToRemove.append(pos)
        return potensialPosisitionsToRemove

    def pawnMove(self, move, specificCol, specificRow, takes, promote):
        # Update new place with correct piece.
        if(promote):
            piece = promote if self.whiteToMove else promote.lower()
        else:
            piece = 'P' if self.whiteToMove else 'p'
        self.setPiece(move, piece)

        # Remove correct piece
        if(takes):
            #row is not from 0-7
            (column, row) = self.__getColumnRowFromSquare(move)
            removeFromRow = (row - 1) if self.whiteToMove else (row + 1)
            self.setPieceInternal({'row': removeFromRow, 'column': self.__columnToInt(specificCol)}, '1')

            # Check if it is a enpassant move, and remove the piece if it is
            if(self.enpassant != '-'):
                # print('enpassant move', self.enpassant, move)
                if(self.enpassant == move):
                    if(self.whiteToMove == True):
                        (c, r) = self.__getColumnRowFromSquare(move)
                        self.setPieceInternal({'row': r-1, 'column': c}, '1')
                    else:
                        (c, r) = self.__getColumnRowFromSquare(move)
                        self.setPieceInternal({'row': r+1, 'column': c}, '1')

        else:
            #Update old place if just a normal line move
            piece = 'P' if self.whiteToMove else 'p'
            self.updatePawnPos(piece, move)


    def updatePawnPos(self, char, toPosition):
        """
            Finds the old posistion to the Pawn, and sets it to blank.
            Can not be used by pawns that has takken a piece. Only works in a straight line
        """
        column, row = self.__getColumnRowFromSquare(toPosition);
        oneStep = -1 if self.whiteToMove else 1
        sqaureBehind = {'row': row + oneStep , 'column' : column }
        if self.getPieceInternal(sqaureBehind) == '1':
            self.enpassant = self.getSqaureFromPos(sqaureBehind)
            enpassant = {'row': row + oneStep*2 , 'column' : column }
            self.setPieceInternal(enpassant, '1')
        else:
            self.enpassant = '-'
            self.setPieceInternal(sqaureBehind, piece = '1')

    def setPiece(self, square, piece = '1'):
        """
            :param square: string: the square, eg. 'a1' to 'h8'
            :param piece: string: a valid piece 'K'|'Q'|'R'|'N'|'B'|'P' or a black counter-part, if you set 1 or just leave it blank and if will use the default parameter
        """
        # print('square:', square)
        # print('square[0]', square[0])
        # print('square[1]', square[1])
        column = self.__columnToInt(square[0])
        row = self.__rowToInt(square[1])
        self.internalChessBoard[row][column] = piece


    def setPieceInternal(self, pos, piece):
        """
            :param pos: a dict with row and column
            :param piece: string: a valid piece 'K'|'Q'|'R'|'N'|'B'|'P' or a black counter-part or '1'  (blank field)
        """
        self.internalChessBoard[pos['row']][pos['column']] = piece


    def getPieceInternal(self, pos):
        """
            :param pos: an object with row and column
            :return string the piece on the board, or 1 if blank.
        """
        return self.internalChessBoard[pos['row']][pos['column']]

    def getPiece(self, square):
        """
            :param square: string: the square, eg. 'a1' to 'h8'
            :return string the piece on the board, or 1 if blank.
        """
        (column, row) = self.__getColumnRowFromSquare(square)
        return self.internalChessBoard[row][column]

    def __getColumnRowFromSquare(self, square):
        """
            :param square: string: the square, eg. 'a1' to 'h8'
        """
        column = self.__columnToInt(square[0])
        row = self.__rowToInt(square[1])
        return (column, row)

    def getSqaureFromPos(self, pos):
        """
            :param pos: a dict with row and column
            :return :square: a int like a1 to e8
        """
        columnLetter = self.intToColum(pos['column'])
        return columnLetter + str(pos['row'] +1)

    def __rowToInt(self, n):
        return int(n)-1

    def __columnToInt(self, char):
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
        self.internalChessBoard =  [
            ['R','N','B','Q','K','B','N','R'],
            ['P','P','P','P','P','P','P','P'],
            ['1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1'],
            ['p','p','p','p','p','p','p','p'],
            ['r','n','b','q','k','b','n','r']]
        self.result = ''

    def printBoard(self):
        loop = 1
        for i in reversed(self.internalChessBoard):
            print(i)

    def notInCheckLine(self, kingPos, piecePos):
        """
            Verifies that the piece is not standing in "line of fire" between and enemy piece and your king as the only piece
            :returns: True if the piece can move
        """
        diffRow = kingPos['row'] - piecePos['row']
        diffCol = kingPos['column'] - piecePos['column']
        if (abs(diffRow) !=  abs(diffCol)) and diffRow != 0 and diffCol != 0:
            return True
        if abs(diffRow) > abs(diffCol):
            columnVect = int((diffCol / abs(diffRow)))
            rowVect = -int((diffRow / abs(diffRow)))
        else:
            columnVect = -int((diffCol / abs(diffCol)))
            rowVect = -int((diffRow / abs(diffCol)))
        checkPos = kingPos.copy()
        nothingInBetween = True
        while not self.isSamePos(checkPos, piecePos):
            checkPos['column'] += columnVect
            checkPos['row'] += rowVect
            if(checkPos == piecePos):
                continue
            if self.getPieceInternal(checkPos) != "1":
                # Piece between the king and the piece can not be a self-disvoery-check.
                return True

        # No piece between the king and the piece, need to verify if an enemy piece is found along the extended vertical until a piece is found or we are no longer on the board.
        # TODO: a bug here now, should look more into this
        checkPos['row'] = checkPos['row'] + rowVect
        checkPos['column'] = checkPos['column'] + columnVect
        while self.onBoard(checkPos):
            if self.getPieceInternal(checkPos) in self.getOppositePieces(["Q", "R"]) and (columnVect == 0 or rowVect == 0):
                return False
            elif self.getPieceInternal(checkPos) in self.getOppositePieces(["Q", "B"]) and columnVect in (1,-1) and rowVect in (-1, 1):
                return False
            if self.getPieceInternal(checkPos) != '1':
                return True;
            checkPos['row'] = checkPos['row'] + rowVect
            checkPos['column'] = checkPos['column'] + columnVect
        return True

    def onBoard(self, position):
        """
        :param :position :{row, column}
        : return :Boolean True it the position is on board
        """
        return position['row'] < 8 and position['row'] >= 0 and position['column'] < 8 and position['column'] >= 0

    def getOppositePieces(self, pieces):
        """"
            Takes a list of pieces and returns it in uppercase if blacks turn, or lowercase if white.
        """
        return map(lambda p: p.lower() if self.whiteToMove else p.upper(), pieces)


    def posOnBoard(self, piece):
        """
            :param piece: a case _sensitiv_ one letter string. Valid 'K', 'Q', 'N', 'P', 'B', 'R', will be transformed to lowercase if it's black's turn to move
            :return {row,column}|[{row,column}]: Returns the posistion(s) on the board for a piece, if only one pos, an object with row and column is returned else a list of objects is returned
        """
        correctPiece = piece if self.whiteToMove else piece.lower()
        posistionsOnBoard = []
        for rowPos, row  in enumerate(self.internalChessBoard):
            for columnPos, pieceInPos in enumerate(self.internalChessBoard[rowPos]):
                if pieceInPos == correctPiece:
                    posistionsOnBoard.append({'row': rowPos, 'column': columnPos})
        if len(posistionsOnBoard) == 1:
            return posistionsOnBoard[0]
        else:
            return posistionsOnBoard
