

def scoreTest( boardScorer = pigglyv3 ):
    b = chess.Board('rnbqkbnr/pppppppp/8/7Q/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1')
    print b
    print "White +squares (w)", boardScorer( b, chess.WHITE )
    print "White +squares (b)", boardScorer( b, chess.BLACK )
    b = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1')
    print b
    print "White down Q (w)", boardScorer( b, chess.WHITE )
    print "White down Q (b)", boardScorer( b, chess.BLACK )
    b = chess.Board('rn1q1rk1/pp2ppbp/2p2np1/3p4/3PP1b1/2N1BN2/PPPQBPPP/R4RK1 w - - 0 6')
    print b
    print "(w) ", boardScorer( b, chess.WHITE )
    print "(b) ", boardScorer( b, chess.BLACK )




def dogPileTests():
    wp = chess.Piece(chess.PAWN, chess.WHITE)
    bp = chess.Piece(chess.PAWN, chess.BLACK)
    wb = chess.Piece(chess.BISHOP, chess.WHITE)
    bb = chess.Piece(chess.BISHOP, chess.BLACK)
    wr = chess.Piece(chess.ROOK, chess.WHITE)
    br = chess.Piece(chess.ROOK, chess.BLACK)
    wq = chess.Piece(chess.QUEEN, chess.WHITE)
    bq = chess.Piece(chess.QUEEN, chess.BLACK)
    wn = chess.Piece(chess.KNIGHT, chess.WHITE)
    bn = chess.Piece(chess.KNIGHT, chess.BLACK)
    wk = chess.Piece(chess.KING, chess.WHITE)
    e = chess.Board()
    e.clear()
    e.set_piece_at(chess.E5, bp)
    e.set_piece_at(chess.D4, wp)
    print str(dogPile(e, chess.D4, chess.WHITE)), " should be True"
    e.set_piece_at(chess.E3, wp)
    print str(dogPile(e, chess.D4, chess.WHITE)), "Expect False (no fair exchange)"
    e.clear()
    e.set_piece_at(chess.C3, bb)
    e.set_piece_at(chess.E5, bb)
    e.set_piece_at(chess.G5, wr)
    e.set_piece_at(chess.E7, wr)
    print dogPile(e, chess.E5, chess.BLACK), "Expect True"
    print dogPile(e, chess.A1, chess.WHITE), "Expect no error"
    e.clear()
    e.set_piece_at(chess.D3, wq)
    e.set_piece_at(chess.C4, wp)
    e.set_piece_at(chess.G5, wr)
    e.set_piece_at(chess.D5, bp)
    e.set_piece_at(chess.D7, bb)
    e.set_piece_at(chess.F7, bq)
    print e.fen()
    print dogPile(e, chess.D5, chess.BLACK), "Expect True"
    e.set_piece_at(chess.D7, br)
    print e
    print dogPile(e, chess.D5, chess.BLACK), "Expect True - but should be False (blocking piece)"
    e.clear()
    e.set_piece_at(chess.D2, bq)
    e.set_piece_at(chess.D1, wq)
    e.set_piece_at(chess.C1, wb)
    e.set_piece_at(chess.E1, wk)
    e.set_piece_at(chess.B1, wn)
    print dogPile(e, chess.D2, chess.BLACK), "Expect True"
    e.Board('rn1q1rk1/pp2ppbp/2p2np1/3p4/3PP1b1/2N1BN2/PPPQBPPP/R4RK1 w - - 0 6')

    
