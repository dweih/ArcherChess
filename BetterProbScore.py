
# Takes the scores of the boards and assigns them a pre-normalization amount of points to receive
def probconverter ( edge )
    if edgescore(edge)<-300:
        return 2
    else:
        return (edgescore(edge)+300)/25)+ log(edgeconfidence(edge)


# Takes [(score, confidence, board)], my_move(the boolean variable expressing whose turn it is)
# Returns list of tuples [(probability, board)] for investments
def Betterprobscore ( edgeInfo, my_move )
# This part just returns empty if there is no information about the edges. Should not happen in practice
    if len(edgeInfo) == 0:
        return []
    sorted_edgeInfo = sorted( edgeInfo, key=itemgetter(0), reverse=not(my_move))
    currentconfidence = sum(edgeconfidence(edge))
#This is a little thing for pulling one piece out of edgeInfo
    edgescore = itemgetter(0)
    edgeconfidence = itemgetter (1)
    justtheboard = itemgetter(2)
    probscores = [scoreconverter(edge) for edge in edgeinfo]
    probscores[0] += currentconfidence/2
# Normalization time
# Find the total amount of points that were given out
        totalscores = sum(probscores)
# Normalize using the total
        normalizedscores = [prescore/totalscores for prescore in probscores]
        actualscores = [(normscore) for normscore in normalizedscores]
