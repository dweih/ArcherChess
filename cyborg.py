import networkx as nx
import chess

# Dummy functions for testing
def dummyBoardScorer( b ):
    return 0.5

def dummyProbScorer( results ):
    sorted(results, key=lambda x:x[0], reverse=True)
    probs = [0]*len(results)
    probs[0]=0.75
    probs[1]=0.25
    children = zip(*results)[2]
    scores = zip(*results)[0]
    return zip(probs, scores, children)

# Takes list of (score, confidence, board), and then points to invest
# Returns list of (points, board) for investments
def dummyPointAllocator( edgeInfo, points ):
    points = max(points, len(edgeInfo))
    investments = []
    for (s,c,b) in edgeInfo:
        investments += [(points/len(edgeInfo),b)]
    return investments


# Shouldn't be dupicated w/ chess_game
def makeMoves( node ):
    moves = []
    for m in iter(node.legal_moves):
        moves = moves + [m]
    return moves

# Returns (score, confidence, child) for each child, combines them to set
# values for the node.  Made to be called recursively starting at the root
# probScorer is a function with input list of (scores, confidences, child),
#           returning list of (probabilities, scores, child) for use in updating edges
def scoreChild(cyborg, board, probScorer):
    children = cyborg.g.successors(board)
    if (len(children) == 0):
        print board, cyborg.g.node[board]
        return (cyborg.g.node[board]['score'], cyborg.g.node[board]['conf'], board)

    # Remove parent from list if it's there - not sure if this is good...
 #   children.remove(board)

    child_results = map(lambda x: scoreChild(cyborg, x, probScorer), children)
    # Calculate probabilities based on scores and confidences and assign to edges
    probScoreChildList = probScorer(child_results)
    # Annotate edges with probability
    cyborg.annotateEdges(board, probScoreChildList)
    # Calculate this board's score using child scores and probabilities
    my_score = sum(map(lambda (p,s,c):p*s, probScoreChildList))
    # Sum confidences for children
    my_conf = sum(map(lambda (s, c, b):c, child_results))
    # Return score and confidence
    print "setting info for\n", board, "   Data ", my_score, " ", my_conf
    cyborg.g.node[board]['score'] = my_score
    cyborg.g.node[board]['conf'] = my_conf
    return (my_score, my_conf, board)



# Do we want to have a limit to how far we expand before we re-Score?
# Especially since by default we'll have no probability info (unless I have a default, eg. 1/moves, or leave probability out of the parameters)
# Recursively assigns points up the tree based on pointAllocator
def expandGraph( cyborg, points, board, pointAllocator ):
    if points == 0: return
    # Get list of edges from current board and collect required info for pointAllocator
    nextMoves = cyborg.getMoveEdges(board)
    # If points > 0 and board has no children, call expandNode on the board and dec(points)
    if (len(nextMoves) == 0):
        print "Expanding from ", board
        cyborg.expandNode( board )
        expandGraph( cyborg, points-1, board, pointAllocator)
    # Collect info for pointAllocator - list of (score, confidence, board)
#  NOT including probability since in current model it won't be avaiilable for edges built on the fly
    paInput = []
    for (b,nb) in nextMoves:
        print b
        print nb
        print cyborg.g.node[nb], cyborg.g.node[b]
        paInput += [(cyborg.g.node[nb]['score'], cyborg.g.node[nb]['conf'],nb)]
    # Get back list of (points to invest, board)
    investmentList = cyborg.pointAllocator( paInput, points )
    # Call expandGraph for 'points' on the board from each 'move'
    print "Inv ", investmentList
    for (movePoints, board) in investmentList:
        expandGraph( cyborg, movePoints, board, pointAllocator)

class cyborg:
    def __init__(self, board=chess.Board(), boardScorer=dummyBoardScorer, probScorer=dummyProbScorer, pointAllocator=dummyPointAllocator):
        self.g = nx.DiGraph()
        self.current_board = board
        self.boardScorer = boardScorer
        self.probScorer = probScorer
        self.pointAllocator = pointAllocator
        self.addNode( (self.current_board, board, 1, 0, None) )
        return


    def addNode(self, (parentBoard, newBoard, c, s, m)):
        self.g.add_node(newBoard, conf=c, score=s)
#        print "added\n", newBoard, "  data ", self.g.node[newBoard]
        if (m != None):
            self.g.add_edge(parentBoard, newBoard, move=m)
        return

    def getMoveEdges(self, board):
        return self.g.out_edges(board)

    def expandNode(self, board):
        def boardClone( board, move ):
            board.push(move)
            copy = board.copy()
            board.pop()
            return copy
        moves = makeMoves( board )
        scores = map(self.boardScorer, moves)
        boards = map(lambda x: boardClone(board, x), moves)
        nodeInfo = zip([board]*len(boards), boards, [1]*len(boards) ,scores, moves) # Confidence of new board is 1
        map(self.addNode, nodeInfo)
        return

    def Score(self):
        # I had to make scoreChild an external function because I couldn't figure out
        # how to do recursion using methods :(
        scoreChild(self, self.current_board, self.probScorer)
        return

    def Build(self, points):
        expandGraph(self, points, self.current_board, self.pointAllocator)
        self.Score()
        return

    # Takes list of triples of (prob,scores,board)
    def annotateEdges( self, from_board, tuples ):
        for psb in tuples:
            self.g.edge[from_board][psb[2]]['prob'] = psb[0]
        return



        

        
        
       
#    def build(self, board, points):
         
    
        
        
            
