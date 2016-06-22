import re
Edgesquares = set([0,7,8,15,16,23,24,31,32,39,40,47,48,55,56,63])
Blackhome = set([0,1,2,3,4,5,6,7])
Whitehome = set([56,57,58,59,60,61,62,63])
Whitebishop = set([25,30,34,37])
Blackbishop = set([26,29,33,38])
Centresquares = set([27,28,35,36])
Afile = set([0,8,16,24,32,40,48,56])
Bfile = set([1,9,17,25,33,41,49,57])
Cfile = set([2,10,18,26,34,42,50,58])
Dfile = set([3,11,19,27,35,43,51,59])
Efile = set([4,12,20,28,36,44,52,60])
Ffile = set([5,13,21,29,37,45,53,61])
Gfile = set([6,14,22,30,38,46,54,62])
Hfile = set([7,15,23,31,39,47,55,63])

def PamPiece( piece ):
    if (piece == chess.PAWN ) : return 100
    if (piece == chess.KNIGHT ) : return 300
    if (piece == chess.BISHOP ) : return 330
    if (piece == chess.ROOK ) : return 550
    if (piece == chess.QUEEN ) : return 900
    if (piece == chess.KING ) : return 1000

def Pam ( board, color ):
    PileScore=0
    score_polarity = 1 if (color == chess.WHITE) else -1
    FENstring = board.fen()
    # early out if it's checkmate
    if (board.is_checkmate()):
            return 10000*score_polarity
    my_squares = allPieceSquares( board, color )
    for sq in my_squares:
        if (dogPile(board, sq, color)):
            PileScore -= score_polarity*PamPiece( board.piece_at(sq).piece_type )
    return PamScore(FENchanger(FENstring))+PileScore


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
        
def PamScore( ModiFENstring ):
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
            Endgame += 80
        if P.start() == 34|37:
            Endgame += 15
        if P.start() == 48|49|50:
            for K in re.finditer('K', FEN):
                if K.start() == 56|57|58:
                    Endgame += 30
        if P.start() == 40|41|42:
            for K in re.finditer('K', FEN):
                if K.start() == 56|57|58:
                    Endgame += 15
        if P.start() == 53|54|55:
            for K in re.finditer('K', FEN):
                if K.start() == 62|63:
                    Endgame += 30
        if P.start() == 45|46|47:
            for K in re.finditer('K', FEN):
                if K.start() == 62|63:
                    Endgame += 15
        if P.start() in Afile:
            Endgame +=20
            for P in re.finditer('P', FEN):
                if P.start() in Afile:
                    Endgame += -20
        if P.start() in Bfile:
            Endgame +=20
            for P in re.finditer('P', FEN):
                if P.start() in Bfile:
                    Endgame += -20
        if P.start() in Cfile:
            Endgame +=20
            for P in re.finditer('P', FEN):
                if P.start() in Cfile:
                    Endgame += -20
        if P.start() in Dfile:
            Endgame +=20
            for P in re.finditer('P', FEN):
                if P.start() in Dfile:
                    Endgame += -20
        if P.start() in Efile:
            Endgame +=20
            for P in re.finditer('P', FEN):
                if P.start() in Efile:
                    Endgame += -20
        if P.start() in Ffile:
            Endgame +=20
            for P in re.finditer('P', FEN):
                if P.start() in Ffile:
                    Endgame += -20
        if P.start() in Gfile:
            Endgame +=20
            for P in re.finditer('P', FEN):
                if P.start() in Gfile:
                    Endgame += -20
        if P.start() in Hfile:
            Endgame +=20
            for P in re.finditer('P', FEN):
                if P.start() in Hfile:
                    Endgame += -20
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
            Endgame += -80
        if p.start() == 26|29:
            Endgame+= -15
        if p.start() == 8|9|10:
            for k in re.finditer('k', FEN):
                if k.start() == 0|1|2:
                    Endgame += -30
        if p.start() == 16|17|18:
            for k in re.finditer('k', FEN):
                if k.start() == 0|1|2:
                    Endgame += -15
        if p.start() == 13|14|15:
            for k in re.finditer('k', FEN):
                if k.start() == 6|7:
                    Endgame += -30
        if p.start() == 21|22|23:
            for k in re.finditer('k', FEN):
                if k.start() == 6|7:
                    Endgame += -15
        if p.start() in Afile:
            Endgame +=-20
            for p in re.finditer('p', FEN):
                if p.start() in Afile:
                    Endgame += 20
        if p.start() in Bfile:
            Endgame +=-20
            for p in re.finditer('p', FEN):
                if p.start() in Bfile:
                    Endgame += 20
        if p.start() in Cfile:
            Endgame +=-20
            for p in re.finditer('p', FEN):
                if p.start() in Cfile:
                    Endgame += 20
        if p.start() in Dfile:
            Endgame +=-20
            for p in re.finditer('p', FEN):
                if p.start() in Dfile:
                    Endgame += 20
        if p.start() in Efile:
            Endgame +=-20
            for p in re.finditer('p', FEN):
                if p.start() in Efile:
                    Endgame += 20
        if p.start() in Ffile:
            Endgame +=-20
            for p in re.finditer('p', FEN):
                if p.start() in Ffile:
                    Endgame += 20
        if p.start() in Gfile:
            Endgame +=-20
            for p in re.finditer('p', FEN):
                if p.start() in Gfile:
                    Endgame += 20
        if p.start() in Hfile:
            Endgame +=-20
            for p in re.finditer('p', FEN):
                if p.start() in Hfile:
                    Endgame += 20
    for N in re.finditer('N', FEN):
        if N.start() in Whitehome:
            Endgame += -30
        if N.start() in Centresquares:
            Endgame += 30
        if N.start() in Edgesquares:
            Endgame += -40
    for n in re.finditer('n', FEN):
        if n.start() in Blackhome:
            Endgame += 30
        if n.start() in Centresquares:
            Endgame += -30
        if n.start() in Edgesquares:
            Endgame += 40
    for B in re.finditer('B', FEN):
        if B.start() in Whitehome:
            Endgame += -30
        if B.start() in Whitebishop:
            Endgame += 25
    for b in re.finditer('b', FEN):
        if b.start() in Blackhome:
            Endgame += 30
        if b.start in Blackbishop:
            Endgame += -25
    for R in re.finditer('R', FEN):
        if R.start() <=15 and R.start() >=8:
            Endgame += 80
        if R.start() == 59|60|61:
            Endgame += 20
    for r in re.finditer('r', FEN):
        if r.start() <=48 and r.start() >=55:
            Endgame += -80
        if r.start() == 3|4|5:
            Endgame += -20
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
    for Q in re.finditer('Q', FEN):
        if Q.start() in Whitehome:
            Endgame += 60
    for q in re.finditer('q', FEN):
        if q.start() in Blackhome:
            Endgame += -60
            
    return Endgame
        
#def KriegerPiece
#if (piece == chess.PAWN ) : return (100, 120, 1)
#if (piece == chess.KNIGHT ) : return (330, 250, 3)
#if (piece == chess.BISHOP ) : return (330, 300, 3)
#if (piece == chess.ROOK ) : return (450, 550, 5)
#if (piece == chess.QUEEN ) : return (960, 840, 9)
#if (piece == chess.KING ) : return (1000, 1000, 16)

#Positions 1-8 are A8-H8
