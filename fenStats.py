#!/usr/bin/python
# coding=utf8
from __future__ import print_function
import pgntofen
import chess

def main(lib):
    fenVictoryList = {}
    pgnConverter = pgntofen.PgnToFen()
    lines = open('test/20k-database.txt', 'r')
    loopC = 0
    errorC = 0
    line = True
    while line:
        line = lines.readline()
        loopC = loopC + 1
        board = chess.Board()
        pgnConverter.resetBoard()
        winner = line[0:1]
        moves = line[2:].replace('\r\n', '').replace('#', '').split(' ')
        try:
            for move in moves:
                if lib == 'pgntofen':
                    pgnConverter.move(move)
                elif lib == 'chess-python':
                    board.push_san(move)
                else:
                    raise NotImplementedError('Unexpected input arg:' + lib + '. Only pgntofen and chess-python valid options')
                fen = pgnConverter.getFullFen()
                if fen in fenVictoryList:
                    updateWinningDict(winner, fenVictoryList[fen])
                else:
                    fenVictoryList[fen] = createWinningDict(moves[0])
        except(IndexError, ValueError, ZeroDivisionError) as e:
            print('ERROR:', e)
            errorC = errorC + 1
            errorC = errorC + 1

        printProgress(loopC, 20000, 'Processed', 'games', 0, 40)
    print('Processed: ' + str(loopC))
    print('Error: ' + str(errorC))

def updateWinningDict(winner, winlist):
    if winner == 'W':
        winlist[0] = winlist[0] + 1
    elif winner == 'R':
        winlist[1] = winlist[1] + 1
    else:
        winlist[2] = winlist[2] + 1

def createWinningDict(winner):
    if winner == 'W':
        return [1,0,0]
    elif winner == 'B':
        return [0,0,1]
    else:
        return [0,1,0]


import sys

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

if __name__ == '__main__':
    main(sys.argv[1])
