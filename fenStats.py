#!/usr/bin/python
from __future__ import print_function
import pgntofen

def main():
    fenVictoryList = {}
    pgnConverter = pgntofen.PgnToFen()
    lines = open('20k-database.txt', 'r')
    loopC = 0
    errorC = 0
    line = True
    while line:
        try:
            line = lines.readline()
            loopC = loopC + 1
            pgnConverter.resetBoard()
            winner = line[0:1]
            moves = line[2:].replace('\r\n', '').replace('#', '').split(' ')
            #print('moves:', moves)
            for move in moves:
                #print(move, end = ' ')
                pgnConverter.move(move)
                fen = pgnConverter.getFullFen()
                #print('fen', fen)
                if fen in fenVictoryList:
                    updateWinningDict(winner, fenVictoryList[fen])
                else:
                    fenVictoryList[fen] = createWinningDict(moves[0])
        except ValueError:
            errorC = errorC + 1
        except ZeroDivisionError:
            errorC = errorC + 1
        except IndexError:
            errorC = errorC + 1
        print('Errors: ' + str(errorC) + '. Processed: ' + str(loopC))
    


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


if __name__ == '__main__':
    main()
