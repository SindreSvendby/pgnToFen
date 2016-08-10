#!/bin/python
# coding=utf8
from __future__ import print_function
from __future__ import division
from functools import partial
import math
import re
import os


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
    DEBUG = False
    lastMove = 'Before first move'
    fens = []
    result = ''

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

    def moves(self, moves):
        if isinstance(moves, str):
            nrReCompile = re.compile('[0-9]+\.')
            transformedMoves = nrReCompile.sub('', moves)
            pgnMoves = transformedMoves.replace('  ', ' ').split(' ')
            result = pgnMoves[-1:][0]
            if(result in ['1/2-1/2', '1-0', '0-1']):
                self.result = result
                pgnMoves = pgnMoves[:-1]
            print('pgnMoves')
            print(pgnMoves)
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
                try:
                    #print('Processing ', game_info[0:6])
                    pgnToFen = PgnToFen()
                    pgnToFen.resetBoard()
                    fens = pgnToFen.moves(pgnMoves).getAllFens()
                    pgnGames['succeeded'].append((game_info, fens))
                except ValueError as e:
                    pgnGames['failed'].append((game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e))
                except TypeError as e:
                    pgnGames['failed'].append((game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e))
                except IndexError as e:
                    raise IndexError(game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e)
                    pgnGames['failed'].append((game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e))
                except ZeroDivisionError as e:
                    pgnGames['failed'].append((game_info, '"' + pgnToFen.lastMove + '"', pgnToFen.getFullFen(), e))
                finally:
                    started = False
                    game_info = []
                    pgnMoves = ''
            if(started):
                pgnMoves = pgnMoves + ' ' + moves.replace('\n', '').replace('\r', '')
        return pgnGames

    def pgnToFen(self, moves):
        try:
            loopC = 1
            for move in moves:
                self.lastMove = move
                self.DEBUG and print('=========')
                self.DEBUG and print('Movenumber',loopC)
                self.DEBUG and print('TO MOVE:', 'w' if self.whiteToMove else 'b')
                self.DEBUG and print('MOVE:', move)
                self.move(move)
                self.DEBUG and print('after move:')
                self.DEBUG and self.printBoard()
                loopC = loopC + 1
                self.fens.append(self.getFullFen())
            self.sucess = True
            return self
        except ValueError:
            print('Converting PGN to FEN failed.')
            print('Move that failed:', self.lastMove)
            self.printBoard()
            print(self.getFullFen())
            self.fens = []
            self.sucess = False



    def move(self, move):
        try:
            self.lastMove = move
            self.handleAllmoves(move)
            if(self.whiteToMove):
                self.whiteToMove = False
            else:
                self.whiteToMove = True
            return self
        except ValueError:
            self.DEBUG and print('Converting PGN to FEN failed.')
            self.DEBUG and print('Move that failed:', self.lastMove)
            self.DEBUG and self.printBoard()
            self.DEBUG and print('FEN:', self.getFullFen())

    def getAllFens(self):
        return self.fens

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
        self.internalChessBoard[chessBoardNumber] = piece
        self.validQueenMoves(possibelPositons, move, specificCol, specificRow)
        
    def validQueenMoves(self, posistions, move, specificCol, specificRow):
        newColumn = self.columnToInt(move[:1])
        newRow = self.rowToInt(move[1:2])
        newPos = self.placeOnBoard(newRow + 1, move[:1])
        potensialPosisitionsToRemove=[]
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
                            checkPos = int(checkPos + yVect * 8 + xVect)
                            if(checkPos == newPos):
                                continue
                            if self.internalChessBoard[checkPos] != "1":
                                nothingInBetween = False
                        if nothingInBetween:
                            potensialPosisitionsToRemove.append(pos)
        if len(potensialPosisitionsToRemove) == 1:
            correctPos = potensialPosisitionsToRemove[0];
        else:
            if len(potensialPosisitionsToRemove) == 0:
                raise ValueError('Cant find a valid posistion to remove', potensialPosisitionsToRemove)
            notInCheckLineBindNewPos = partial(self.notInCheckLine, self.posOnBoard('K'))
            correctPosToRemove = list(filter(notInCheckLineBindNewPos, potensialPosisitionsToRemove))
            if len(correctPosToRemove) > 1:
                raise ValueError('Several valid positions to remove from the board')
            if len(correctPosToRemove) == 0:
                raise ValueError('None valid positions to remove from the board')
            correctPos = correctPosToRemove[0]
        self.internalChessBoard[correctPos] = "1"
        return


    def rookMove(self, move, specificCol, specificRow):
        column = move[:1]
        row = move[1:2]
        chessBoardNumber = self.placeOnBoard(row, column)
        piece = 'R' if self.whiteToMove else 'r'
        possibelPositons = [i for i, pos in enumerate(self.internalChessBoard) if pos == piece]
        self.internalChessBoard[chessBoardNumber] = piece
        self.validRookMoves(possibelPositons, move, specificCol, specificRow)

    def validRookMoves(self, posistions, move, specificCol, specificRow):
        newColumn = self.columnToInt(move[:1])
        newRow = self.rowToInt(move[1:2])
        newPos = self.placeOnBoard(newRow + 1, move[:1])
        potensialPosisitionsToRemove=[]
        if(len(posistions) == 1):
            self.internalChessBoard[posistions[0]] = "1"
            return
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
                        while(checkPos != newPos):
                            checkPos = int(checkPos + yVect * 8 + xVect)
                            if(checkPos == newPos):
                                continue
                            if self.internalChessBoard[checkPos] != "1":
                                nothingInBetween = False
                        if nothingInBetween:
                            potensialPosisitionsToRemove.append(pos)
        if len(potensialPosisitionsToRemove) == 1:
            correctPos = potensialPosisitionsToRemove[0];
        else:
            if len(potensialPosisitionsToRemove) == 0:
                raise ValueError('Cant find a valid posistion to remove', potensialPosisitionsToRemove)
            notInCheckLineBindNewPos = partial(self.notInCheckLine, self.posOnBoard('K'))
            correctPosToRemove = list(filter(notInCheckLineBindNewPos, potensialPosisitionsToRemove))
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
        self.internalChessBoard[chessBoardNumber] = piece
        self.validBishopMoves(possibelPositons, move, specificCol, specificRow)

    def validBishopMoves(self, posistions, move, specificCol, specificRow):
        newColumn = self.columnToInt(move[:1])
        newRow = self.rowToInt(move[1:2])
        newPos = self.placeOnBoard(newRow + 1, move[:1])
        potensialPosisitionsToRemove = []
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
                            checkPos = int(checkPos + yVect * 8 + xVect)
                            if(checkPos == newPos):
                                continue
                            if self.internalChessBoard[checkPos] != "1":
                                nothingInBetween = False
                        if nothingInBetween:
                            potensialPosisitionsToRemove.append(pos)
        if len(potensialPosisitionsToRemove) == 1:
            correctPos = potensialPosisitionsToRemove[0];
        else:
            if len(potensialPosisitionsToRemove) == 0:
                raise ValueError('Cant find a valid posistion to remove', potensialPosisitionsToRemove)
            notInCheckLineBindNewPos = partial(self.notInCheckLine, self.posOnBoard('K'))
            correctPosToRemove = list(filter(notInCheckLineBindNewPos, potensialPosisitionsToRemove))
            if len(correctPosToRemove) > 1:
                raise ValueError('Several valid positions to remove from the board')
            correctPos = correctPosToRemove[0]
        self.internalChessBoard[correctPos] = "1"

    def knightMove(self, move, specificCol, specificRow):
        column = move[:1]
        row = move[1:2]
        chessBoardNumber = self.placeOnBoard(row, column)
        piece = 'N' if self.whiteToMove else 'n'
        knightPositons = [i for i, pos in enumerate(self.internalChessBoard) if pos == piece]
        self.internalChessBoard[chessBoardNumber] = piece
        self.validKnighMoves(knightPositons, move, specificCol, specificRow)

    def validKnighMoves(self, posistions, move, specificCol, specificRow):
        newColumn = self.columnToInt(move[:1])
        newRow = self.rowToInt(move[1:2])
        potensialPosisitionsToRemove = []
        for pos in posistions:
            (existingRow, existingCol) = self.internalChessBoardPlaceToPlaceOnBoard(pos)
            validatePos = str(int(existingRow - newRow)) + str(int(self.columnToInt(existingCol) - newColumn))
            if validatePos in ['2-1','21','1-2','12','-1-2','-12','-2-1','-21']:
                if not specificCol or specificCol == existingCol:
                    if not specificRow or (int(specificRow) -1) == int(existingRow):
                            potensialPosisitionsToRemove.append(pos)
        if len(potensialPosisitionsToRemove) == 1:
            correctPos = potensialPosisitionsToRemove[0];
        else:
            if len(potensialPosisitionsToRemove) == 0:
                raise ValueError('Cant find a valid posistion to remove', potensialPosisitionsToRemove)
            notInCheckLineBindNewPos = partial(self.notInCheckLine, self.posOnBoard('K'))
            correctPosToRemove = list(filter(notInCheckLineBindNewPos, potensialPosisitionsToRemove))
            if len(correctPosToRemove) > 1:
                raise ValueError('Several valid positions to remove from the board')
            if len(correctPosToRemove) == 0:
                raise ValueError('None valid positions to remove from the board')
            correctPos = correctPosToRemove[0]
        self.internalChessBoard[correctPos] = "1"
        return
    def pawnMove(self, toPosition, specificCol, specificRow, takes, promote):
        column = toPosition[:1]
        row = toPosition[1:2]
        prevEnpassant = self.enpassant
        self.enpassant = '-'
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
            if(prevEnpassant != '-'):
                enpassantPos = self.placeOnBoard(prevEnpassant[1], prevEnpassant[0])
                toPositionPos = self.placeOnBoard(toPosition[1], toPosition[0])
                if(prevEnpassant == toPosition):
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
                    self.enpassant = '-'
                else:
                    posistion = posistion + step
                    self.enpassant = '-'
                piece = self.internalChessBoard[posistion]


    def placeOnBoard(self, row, column):
        # returns internalChessBoard place
        return 8 * (int(row) - 1) + self.columnToInt(column);

    def internalChessBoardPlaceToPlaceOnBoard(self, chessPos):
        column = int(chessPos) % 8
        row = math.floor(chessPos/8)
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
        self.result = ''

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

        diffRow = int(kingRowInt - pieceRowInt)
        diffCol = int(kingColumnInt - pieceColumnInt)
        if (abs(diffRow) !=  abs(diffCol)) and diffRow != 0 and diffCol != 0:
            return True
        if abs(diffRow) > abs(diffCol):
            xVect = (diffCol / abs(diffRow))
            yVect = -(diffRow / abs(diffRow))
        else:
            xVect = -(diffCol / abs(diffCol))
            yVect = -(diffRow / abs(diffCol))

        checkPos = kingPos
        nothingInBetween = True
        while checkPos != piecePos and (checkPos < 64 and checkPos >= 0):
            checkPos = int(checkPos + yVect * 8 + xVect)

            if(checkPos == piecePos):
                continue
            if self.internalChessBoard[checkPos] != "1":
                #print('Something between king and piece, returning a false value')
                # Piece between the king and the piece can not be a self-disvoery-check.
                return True
        #print('No piece between the king and the piece, need to verify if an enemy piece with the possibily to go that  direction exist')
        # No piece between the king and the piece, need to verify if an enemy piece with the possibily to go that  direction exist

        columnNr = (piecePos % 8)
        searchRow = pieceRowInt
        
        if(xVect == 1):
            columnsLeft = 7- columnNr
        else:
            columnsLeft = columnNr
        posInMove = (yVect * 8) + xVect

        while checkPos >= 0 and checkPos < 64 and columnsLeft > -1:
            columnsLeft = columnsLeft - abs(xVect)
            checkPos = int(checkPos + posInMove)
            currentRow = math.floor(checkPos/8)

            if(checkPos < 0 or checkPos > 63):
                continue
            if self.internalChessBoard[checkPos] in self.getOppositePieces(["Q", "R"]) and xVect == 0:
                return False
            elif self.internalChessBoard[checkPos] in self.getOppositePieces(["Q", "R"]) and yVect == 0 and searchRow == currentRow:
                return False
            elif self.internalChessBoard[checkPos] in self.getOppositePieces(["Q", "B"]) and (abs(xVect) == abs(yVect)):
                return False
            elif self.internalChessBoard[checkPos] != "1":
                return True

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
    f = open("1999.txt", "r")
    g = open("production.txt", "w")
    h = open("fails.txt", "w")

    for line in f:
    
        pgnFormat = line[2:-1]
        winner = line[0]
        if winner == "W":
            win_text = " 1 0 0"
        elif winner == "R":
            win_text = " 0 1 0"
        elif winner == "B":
            win_text = " 0 0 1"
        else:
            print("error")

        converter = PgnToFen()
        
        converter.resetBoard()

        mid_liste = []

        try:
        
            for move in pgnFormat.split(' '):
                converter.move(move)
                mid_liste.append(converter.getFullFen() + win_text)

            for unit in mid_liste:
                g.write(unit + "\n")

        except:

            h.write(line)

    f.close()
    g.close()
    h.close()
