import math

def CherylProbScorer( results, color, my_color ):
    Movelist = []
    probs = []
    for move in results:
        Movelist.append( [move, ConfidenceCombiner ( move, color, my_color )] )
        probs.append(0)
    Movelist = sorted(Movelist, key=itemgetter(1), reverse=(color == chess.WHITE)^(my_color != chess.WHITE))
    Justmoves = [itemgetter(0)(move) for move in Movelist]
    probs[0]=1
    children = [move[2] for move in Justmoves]
    scores = [move[0] for move in Justmoves]
    return zip(probs, scores, children)

def ConfidenceCombiner ( move, color, my_color ):
    conf_polarity = 1 if ((color == chess.WHITE)^(my_color != chess.WHITE)) else -1
    return move[0]+ conf_polarity * math.log(move[1])
