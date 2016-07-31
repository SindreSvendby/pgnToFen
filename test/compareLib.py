import chess
import pgntofen
import re
zfe = 'ZeroDivisonError.txt'
ve = 'ValueError.txt'
ie = 'IndexError.txt'

def main():
    zfeH = open(zfe, 'w')
    ieH = open(ie, 'w')
    veH = open(ve, 'w')
    started = False
    pgnMoves = ''
    loopC = 1
    faledC = 0
    okC = 0
    errorC = 0
    #for moves in open(ve, 'r').readlines():
    for moves in open('test/Carlsen.pgn', 'r').readlines():
        info = ()
        if(moves[:1] == '['):
            #print('skipping line: ', moves)
            info = moves
            continue
        if(moves[:2] == '1.'):
            started = True
        if((moves == '\r\n' or moves == '\n') and started):
            started = False
            try:
                if handleCompleteLine(pgnMoves):
                    okC = okC + 1
                else:
                    faledC = faledC + 1
            except ZeroDivisionError:
                print('FALED HARD ZeroDivisionError')
                zfeH.write(pgnMoves)
                errorC = errorC + 1
                #raise RuntimeError('Lets look into this')
            except ValueError:
                print('FALED HARD ValueError')
                veH.write(pgnMoves)
                errorC = errorC + 1
                #raise RuntimeError('Lets look into this')
            except IndexError:
                print('FALED HARD IndexError')
                ieH.write(pgnMoves)
                errorC = errorC + 1
                #raise RuntimeError('Lets look into this')
            print('ok:', str(okC))
            print('failed:', str(faledC))
            print('errorC:', str(errorC))
            print ('loop' + str(loopC))
            loopC = loopC+1
            pgnMoves = ''
        if(started):
            pgnMoves = pgnMoves + moves

def handleCompleteLine(line):
    moves = convertToKarFormat(line)
    pgnConverter = pgntofen.PgnToFen()
    board = chess.Board()
    pgnConverter.resetBoard()
    pgnConverter.pgnToFen(moves.split(' '))
    fenPosA = pgnConverter.getFullFen()
    for move in moves.split(' '):
        board.push_san(move)
    fenHash = toFENhash(board.fen())
    fenHash =''
    fenPosA=''
    if(fenPosA[:fenPosA.find(' ')] == fenHash[:fenHash.find(' ')]):
        print("Equal ")
        return True
    else:
        print("Not Equal")
        print ('Var: ', fenPosA)
        print ('python-chess lib: ', fenHash)
        return False

def convertToKarFormat(moves):
    #TODO: handle better ' 1-0\r\n'
    finalString = moves.replace('\r\n', ' ').replace('\n', ' ').replace('  1/2-1/2', '').replace('  0-1', '').replace('  1-0', '')[:-1]
    #print('finalString DEBUG:', finalString)
    movesArray = finalString.split(' ')
    #print('MOVES movesArray:', movesArray)
    karFormat = ''
    for move in movesArray:
        dotIndex = move.find('.')
        if(dotIndex > -1):
            karFormat = karFormat + ' ' + move[dotIndex+1:]
        else:
            karFormat = karFormat + ' ' + move
    return karFormat[1:]

def toFENhash(fen):
    """ Removes the two last parts of the FEN notation
    """
    return ' '.join(fen.split(" ")[:-2])

if __name__ == '__main__':
    main()
