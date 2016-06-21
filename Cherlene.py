import re
Edgesquares = set([0,7,8,15,16,23,24,31,32,39,40,47,48,55,56,63])

def Cherlene ( board, color ):
    FENstring = board.fen()
    # early out if it's checkmate
    if (board.is_checkmate()):
        if color == chess.WHITE:
            return 10000
        else:
            return -10000
    return CherleneEndgameScore(FENchanger(FENstring))


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
        
def CherleneEndgameScore( ModiFENstring ):
    FEN = ModiFENstring
    Endgame = FEN.count('P')*100 + FEN.count('p')*-100
    Endgame += FEN.count('N')*300 + FEN.count('n')*-300
    Endgame += FEN.count('B')*330 + FEN.count('b')*-330
    Endgame += FEN.count('R')*550 + FEN.count('r')*-550
    Endgame += FEN.count('Q')*900 + FEN.count('q')*-900
    for P in re.finditer('P', FEN):
        if P.start() == 35:
            Endgame += 45
        if P.start() == 36:
            Endgame += 45
        if P.start() == 27:
            Endgame += 35
        if P.start() == 28:
            Endgame += 35
        if P.start() <=31 and P.start() >=24:
            Endgame += 20
        if P.start() <=23 and P.start() >=16:
            Endgame += 55
        if P.start() <=15:
            Endgame += 70 
    for p in re.finditer('p', FEN):
        if p.start() == 35:
            Endgame += -35
        if p.start() == 36:
            Endgame += -35
        if p.start() == 27:
            Endgame += -45
        if p.start() == 28:
            Endgame += -45
        if p.start() >=32 and p.start() <=39:
            Endgame += -20
        if p.start() >=40 and p.start() <=47:
            Endgame += -55
        if p.start() >=48:
            Endgame += -70
    for N in re.finditer('N', FEN):
        if N.start() == 57:
            Endgame += -40
        if N.start() == 62:
            Endgame += -40
        if N.start() == 35:
            Endgame += 40
        if N.start() == 36:
            Endgame += 40
        if N.start() == 27:
            Endgame += 40
        if N.start() == 28:
            Endgame += 40
        if N.start() in Edgesquares:
            Endgame += -40
    for n in re.finditer('n', FEN):
        if n.start() == 1:
            Endgame += 40
        if n.start() == 6:
            Endgame += 40
        if n.start() == 35:
            Endgame += -40
        if n.start() == 36:
            Endgame += -40
        if n.start() == 27:
            Endgame += -40
        if n.start() == 28:
            Endgame += -40
        if n.start() in Edgesquares:
            Endgame += 40
    for B in re.finditer('B', FEN):
        if B.start() == 58:
            Endgame += -60
        if B.start() == 61:
            Endgame += -60
    for b in re.finditer('b', FEN):
        if b.start() == 2:
            Endgame += 60
        if b.start() == 5:
            Endgame += 60
    for R in re.finditer('R', FEN):
        if R.start() <=15 and R.start() >=8:
            Endgame += 80
    for r in re.finditer('r', FEN):
        if r.start() <=48 and r.start() >=55:
            Endgame += -80
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
    return Endgame
        
#def KriegerPiece
#if (piece == chess.PAWN ) : return (100, 120, 1)
#if (piece == chess.KNIGHT ) : return (330, 250, 3)
#if (piece == chess.BISHOP ) : return (330, 300, 3)
#if (piece == chess.ROOK ) : return (450, 550, 5)
#if (piece == chess.QUEEN ) : return (960, 840, 9)
#if (piece == chess.KING ) : return (1000, 1000, 16)

#Positions 1-8 are A8-H8
