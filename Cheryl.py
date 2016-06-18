import re

def Cheryl ( board ):
    FENstring = board.FEN
    # early out if it's checkmate
    if (node.is_checkmate()):
        return 10000
    return CherylEndgameScore(FENchanger(FENstring))


def FENchanger ( FENstring ):
    FEN = FENstring
    FEN = FEN.replace('8', '11111111')
    FEN = FEN.replace('7', '1111111')
    FEN = FEN.replace('6', '111111')
    FEN = FEN.replace('5', '11111')
    FEN = FEN.replace('4', '1111')
    FEN = FEN.replace('3', '111')
    FEN = FEN.replace('2', '11')
    FEN = FEN.split(" ")[0]
    FEN = FEN.replace("/", "")
    return FEN
        
def CherylEndgameScore( ModiFENstring ):
    FEN = ModiFENstring
    Endgame = FEN.count('P')*120 + FEN.count('p')*-120
    Endgame += FEN.count('N')*250 + FEN.count('n')*-250
    Endgame += FEN.count('B')*300 + FEN.count('b')*-300
    Endgame += FEN.count('R')*550 + FEN.count('r')*-550
    Endgame += FEN.count('Q')*840 + FEN.count('q')*-840
    for P in re.finditer('P', FEN):
        if P.start() == 35:
            Endgame += 25
        if P.start() == 36:
            Endgame += 25
        if P.start() == 43:
            Endgame += 25
        if P.start() == 44:
            Endgame += 25
    for p in re.finditer('p', FEN):
        if p.start() == 35:
            Endgame += -25
        if p.start() == 36:
            Endgame += -25
        if p.start() == 43:
            Endgame += -25
        if p.start() == 44:
            Endgame += -25
    for N in re.finditer('N', FEN):
        if N.start() == 57:
            Endgame += -20
        if N.start() == 62:
            Endgame += -20
    for n in re.finditer('n', FEN):
        if n.start() == 1:
            Endgame += 20
        if n.start() == 6:
            Endgame += 20
    for B in re.finditer('B', FEN):
        if B.start() == 58:
            Endgame += -20
        if B.start() == 61:
            Endgame += -20
        if B.start() == 49:
            Endgame += 25
        if B.start() == 54:
            Endgame += 25
    for b in re.finditer('b', FEN):
        if b.start() == 2:
            Endgame += 20
        if b.start() == 5:
            Endgame += 20
        if b.start() == 9:
            Endgame += -25
        if b.start() == 14:
            Endgame += -25
    for K in re.finditer('K', FEN):
        if K.start() == 62:
            Endgame += 50
        if K.start() == 58:
            Endgame += 50
    for k in re.finditer('k', FEN):
        if k.start() == 2:
            Endgame += -50
        if k.start() == 6:
            Endgame += -50
    
    print Endgame
        
#def KriegerPiece
#if (piece == chess.PAWN ) : return (100, 120, 1)
#if (piece == chess.KNIGHT ) : return (330, 250, 3)
#if (piece == chess.BISHOP ) : return (330, 300, 3)
#if (piece == chess.ROOK ) : return (450, 550, 5)
#if (piece == chess.QUEEN ) : return (960, 840, 9)
#if (piece == chess.KING ) : return (1000, 1000, 16)

#Positions 1-8 are A8-H8
