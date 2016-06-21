
import math

# Takes [(score, confidence, board)], my_move(the boolean variable expressing whose turn it is)
# and the number points to invest
# Returns list of tuples [(points, board)] for investments
def SimplePointAllocator( edgeInfo, color, points ):
# This part just returns empty if there is no information about the edges. Should not happen in practice
    if len(edgeInfo) == 0:
        return []
#This is a little thing for pulling one piece out of edgeInfo
    edgescore = itemgetter(0)
    edgeconfidence = itemgetter(1)
    justtheboard = itemgetter(2)
# This calculates the mean score/confidence of all edges
    Scores = [edgescore(edge) for edge in edgeInfo]
    Scores = sorted(Scores, reverse=True)
    Confidences = [edgeconfidence(edge) for edge in edgeInfo]
    Confidences = sorted(Confidences)
    Meanscore = sum(edgescore(edge) for edge in edgeInfo)/len(edgeInfo)
    Acceptablescore = Meanscore/4 + 3*Scores[0]/4
    Meanconfidence = sum(edgeconfidence(edge) for edge in edgeInfo)/len(edgeInfo)
# Instruction for actual assignment of points
# Find moves of above-average score
    Goodmoves = []
    Interestingmoves = []
    Boringmoves = []
    if(color == chess.WHITE):
        for edge in edgeInfo:
            if edgescore(edge)>=Acceptablescore:
                Goodmoves.append(edge)
            else:
                if edgeconfidence(edge)<=Meanconfidence:
                    Interestingmoves.append(edge)
                else:
                    Boringmoves.append(edge)
    if(color == chess.BLACK):
        for edge in edgeInfo:
            if edgescore(edge)<=Acceptablescore:
                Goodmoves.append(edge)
            else:
                if edgeconfidence(edge)<=Meanconfidence:
                    Interestingmoves.append(edge)
                else:
                    Boringmoves.append(edge)
# Find the amount that will be given to each move
    if Confidences[0] < 300:
        if len(Goodmoves)>0:
            Goodmovepoints = math.floor(0.2*points/len(Goodmoves))
        if len(Interestingmoves)>0:
            Othermovepoints = math.floor(0.8*points/len(Interestingmoves))
        else:
            Othermovepoints = 0
    else:
        if len(Goodmoves)>0:
            Goodmovepoints = math.floor(points/len(Goodmoves))
        if len(Interestingmoves)>0:
            Othermovepoints = 0
        else:
            Othermovepoints = 0
        
# Build the list
    Finalset = []
    Finalscores = []
    Goodmoves = sorted(Goodmoves, key=itemgetter(0), reverse=(color == chess.WHITE))
    for board in Goodmoves:
        Finalset.append(justtheboard(board))
        Finalscores.append(Goodmovepoints)
    for board in Interestingmoves:
        Finalset.append(justtheboard(board))
        Finalscores.append(Othermovepoints)
    for board in Boringmoves:
        Finalset.append(justtheboard(board))
        Finalscores.append(0)
# Find the total amount of points that were given out
# Hand any leftovers to the top choice
    leftovers = points - sum(Finalscores)
    Finalscores[0] += leftovers   
# Return tuples in one giant list comprehension
##    print Interestingmoves
##    print Goodmoves
##    print Meanconfidence
##    print Meanscore
##    print Acceptablescore
##    print ( edgeInfo )
    return zip (Finalscores, Finalset)
