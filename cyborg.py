import networkx as nx
import chess
from operator import itemgetter
import math

# Dummy functions for testing
def dummyBoardScorer( b, c ):
    return 0.5

def dummyProbScorer( results, my_move ):
    sorted(results, key=lambda x:x[0], reverse=not(my_move)) # Biggest first for me, lowest for them
    probs = [0]*len(results)
    probs[0]=0.75
    probs[1]=0.25
    children = zip(*results)[2]
    scores = zip(*results)[0]
    return zip(probs, scores, children)

# Takes list of (score, confidence, board), my_move, and points to invest
# Returns list of (points, board) for investments
def dummyPointAllocator( edgeInfo, my_move, points ):
    if len(edgeInfo) == 0:
        return []
    if len(edgeInfo) < 3:
        return [(points, edgeInfo[0][2])]
    sorted_edgeInfo = sorted(edgeInfo, key=itemgetter(0), reverse=not(my_move))
    investments = [(math.ceil(points/2.0),sorted_edgeInfo[0][2])]
#    investments += [(math.floor(points/4.0),sorted_edgeInfo[1][2])]
#    investments += [(math.floor(points/4.0),sorted_edgeInfo[2][2])]
    return investments


# Shouldn't be dupicated w/ chess_game
def makeMoves( node ):
    moves = []
    for m in iter(node.legal_moves):
        moves = moves + [m]
    return moves

# Returns (score, confidence, child) for each child, combines them to set
# values for the node.  Made to be called recursively starting at the root
# probScorer is a function with input list of (scores, confidences, child) and my_move,
#           returning list of (probabilities, scores, child) for use in updating edges
def scoreChild(cyborg, board_fen, probScorer, my_move):
    children = cyborg.g.successors(board_fen)
    if (len(children) == 0):
        return (cyborg.g.node[board_fen]['score'], cyborg.g.node[board_fen]['conf'], board_fen)
    # Turns alternate as you go up the tree 
    child_results = map(lambda x: scoreChild(cyborg, x, probScorer, not(my_move)), children)
    # Calculate probabilities based on scores and confidences and assign to edges
    probScoreChildList = probScorer(child_results, my_move)
    # Annotate edges with probability
    cyborg.annotateEdges(board_fen, probScoreChildList)
    # Calculate this board's score using child scores and probabilities
    my_score = sum(map(lambda (p,s,c):p*s, probScoreChildList))
    # Sum confidences for children
    my_conf = sum(map(lambda (s, c, b):c, child_results))
    # Return score and confidence
    cyborg.g.node[board_fen]['score'] = my_score
    cyborg.g.node[board_fen]['conf'] = my_conf
    return (my_score, my_conf, board_fen)



# Do we want to have a limit to how far we expand before we re-Score?
# Especially since by default we'll have no probability info (unless I have a default, eg. 1/moves, or leave probability out of the parameters)
# Recursively assigns points up the tree based on pointAllocator
def expandGraph( cyborg, points, board, pointAllocator ):
    if points == 0: return
    # Get list of edges from current board and collect required info for pointAllocator
    nextMoves = cyborg.getMoveEdges(board)
    # If points > 0 and board has no children, call expandNode on the board and dec(points)
    if (len(nextMoves) == 0):
        cyborg.expandNode( board )
        expandGraph( cyborg, points-1, board, pointAllocator)
    # Collect info for pointAllocator - list of (score, confidence, board)
#  NOT including probability since in current model it won't be avaiilable for edges built on the fly
    paInput = []
    my_move = board.turn == cyborg.color
    for (thisBoard_fen,nextBoard_fen,move) in nextMoves:
        print 'expanding from ', thisBoard_fen, ' to ', nextBoard_fen
        paInput += [(cyborg.g.node[nextBoard_fen]['score'], cyborg.g.node[nextBoard_fen]['conf'],nextBoard_fen)]
    # Get back list of (points to invest, board as fen)
    investmentList = cyborg.pointAllocator( paInput, my_move, points )
    # Call expandGraph for calculated number of points on the board from each move
    for (movePoints, board_fen) in investmentList:
        expandGraph( cyborg, movePoints, chess.Board(board_fen), pointAllocator)

class cyborg:
    def __init__(self, board=chess.Board(), color=chess.WHITE, boardScorer=dummyBoardScorer, probScorer=dummyProbScorer, pointAllocator=dummyPointAllocator):
        self.g = nx.DiGraph()
        self.current_board = board
        self.color = color
        self.boardScorer = boardScorer
        self.probScorer = probScorer
        self.pointAllocator = pointAllocator
        self.addNode( (self.current_board, board, 1, 0, None) )
        return


    def addNode(self, (parentBoard, newBoard, c, s, m)):
        self.g.add_node(newBoard.fen(), conf=c, score=s)
        print "added\n", newBoard.fen(), "  data ", self.g.node[newBoard.fen()]
        if (m != None):
            print 'new edge \n', parentBoard.fen(), "\n", newBoard.fen(), m
            self.g.add_edge(parentBoard.fen(), newBoard.fen(), move=m)
        return

    def getMoveEdges(self, board = None ):
        if (board == None):
            board = c.current_board
        return self.g.out_edges(board.fen(), data=True)


    def expandNode(self, board):
        moves = makeMoves( board )
        nodeInfo = []
        for m in moves:
            board.push(m)
            newBoard = board.copy()
            board.pop()
            nodeInfo += [(board, newBoard, 1, self.boardScorer(newBoard, self.color), m)] # Confidence of new board is 1
        map(self.addNode, nodeInfo)
        return

    def Score(self):
        # I had to make scoreChild an external function because I couldn't figure out
        # how to do recursion using methods :(
        scoreChild(self, self.current_board.fen(), self.probScorer, self.current_board.turn == self.color)
        return

    def Build(self, points):
        expandGraph(self, points, self.current_board, self.pointAllocator)
        self.Score()
        print 'Built to ', len(self.g.nodes()), ' nodes'
        return

    # Takes list of triples of (prob,scores,board)
    def annotateEdges( self, from_board, tuples ):
        for psb in tuples:
            self.g.edge[from_board][psb[2]]['prob'] = psb[0]
        return

    # Get scored moves from a board - set up for choosing a move
    def getScoredMoves( self, board = None ):
        if (board == None):
            board = self.current_board
        edges = self.getMoveEdges( board )
        moves = []
        for (cb,nb,data) in edges:
            moves += [(self.g.edge[cb][nb]['move'], self.g.node[nb]['score'])]
        return moves

    # This just gets the next move, but doesn't play it
    def getNextMove( self, board = None ):
        if (board == None):
            board = self.current_board 
        scoredMoves = self.getScoredMoves( board )
        bestMove = max(scoredMoves,key=itemgetter(1))
        return bestMove

    # Designed to be the right function for 'game' to call
    def chooseMove( self, board = None ):
# Need some smarts here that I can't figure out right now
        self.Build( 5 )
        self.Build( 5 )
        m = self.getNextMove()
        print m
        return self.getNextMove()


    def acceptMove( self, move ):
        # This is where we move current board up the graph to other player's move
# Not sure if we should push the move or just set the board...
        print move
        self.current_board.push(move)
        return
         
    def printEdges( self, board = None ):
        edges = self.getMoveEdges( board )
        for e in edges:
            print "from ", e[0], " - to - ", e[1], " via ", e[2]['move']
        return
        
        
            
