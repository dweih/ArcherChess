
# Takes the scores of the boards and assigns them a pre-normalization amount of points to receive
def scoreconverter ( edge )
    if edgescore(edge)<-300:
        return 2
    else:
        return floor((edgescore(edge)+300)/25) + 2

# Takes [(score, confidence, board)], my_move(the boolean variable expressing whose turn it is)
# and the number points to invest
# Returns list of tuples [(points, board)] for investments
def dummyPointAllocator( edgeInfo, my_move, points ):
# This part just returns empty if there is no information about the edges. Should not happen in practice
    if len(edgeInfo) == 0:
        return []
# Sorts the edges from worst to best, reverses if it is your move
    sorted_edgeInfo = sorted(edgeInfo, key=itemgetter(0), reverse=not(my_move))
#This is a little thing for pulling the score off a board
    edgescore = itemgetter(0)
    justtheboard = itemgetter(2)
# Early out if we have less than 30 points to assign
    if points < 30:
        return [ (
    else:
# Instruction for actual assignment of points
# Assign un-normalized values which will be converted to the portions of points to be assigned
        allocatorscores = [scoreconverter(edge) for edge in edgeinfo]
# Normalization time
# Find the total amount of points that were given out
        totalscores = sum(allocatorscores)
# Normalize using the total
        normalizedscores = [prescore/totalscores for prescore in allocatorscores]
        actualscores = [floor(normscore*points) for normscore in normalizedscores]
# Hand any leftovers to the top choice
        leftovers = points - sum(actualscores)
# Seems like a big problem but this is what I want to do!
        actualscores[0] = actualscores[0] + leftovers
# Return tuples in one giant list comprehension
        return [ (actscore for actscore in actualscores) (justtheboard(edge) for edge in edgeInfo) ]
