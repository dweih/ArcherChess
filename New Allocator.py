
import math

# Takes [(score, confidence, board)], my_move(the boolean variable expressing whose turn it is)
# and the number points to invest
# Returns list of tuples [(points, board)] for investments
def PointAllocator( edgeInfo, my_move, points ):
# This part just returns empty if there is no information about the edges. Should not happen in practice
    if len(edgeInfo) == 0:
        return []
# Sorts the edges from worst to best, reverses if it is your move
    sorted_edgeInfo = sorted(edgeInfo, key=itemgetter(0), reverse=not(my_move))
#This is a little thing for pulling one piece out of edgeInfo
    edgescore = itemgetter(0)
    edgeconfidence = itemgetter(1)
    justtheboard = itemgetter(2)
# This calculates the mean score/confidence of all edges
    Meanscore = sum(edgescore(edge) for edge in edgeInfo)/len(edgeInfo)
    Meanconfidence = sum(edgeconfidence(edge) for edge in edgeInfo)/len(edgeInfo)
# Instruction for actual assignment of points
# Find moves of above-average score
    Goodmoves = []
    Interestingmoves = []
    Boringmoves = []
    for edge in edgeInfo:
        if edgescore(edge)>=Meanscore:
            Goodmoves.append(justtheboard(edge))
        else:
            if edgeconfidence(edge)<Meanconfidence:
                Interestingmoves.append(justtheboard(edge))
            else:
                Boringmoves.append(justtheboard(edge))
# Find the amount that will be given to each move
    Goodmovepoints = math.floor(0.6*points/len(Goodmoves))
    if len(Interestingmoves)>0:
        Othermovepoints = math.floor(0.4*points/len(Interestingmoves))
    else:
        Othermovepoints = 0
# Build the list
    Finalset = []
    Finalscores = []
    for board in Goodmoves:
        Finalset.append(board)
        Finalscores.append(Goodmovepoints)
    for board in Interestingmoves:
        Finalset.append(board)
        Finalscores.append(Othermovepoints)
    for board in Boringmoves:
        Finalset.append(board)
        Finalscores.append(0)
# Find the total amount of points that were given out
# Hand any leftovers to the top choice
    leftovers = points - sum(Finalscores)
    Finalscores[0] += leftovers
# Return tuples in one giant list comprehension
    return zip(Finalscores, Finalset)
