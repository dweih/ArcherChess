import networkx as nx
import chess
from operator import itemgetter
import math

def dummyProbScorer( results, color, my_color ):
    results = sorted(results, key=lambda x:x[0], reverse=((color == chess.WHITE)^(my_color != chess.WHITE))) # Scores are now always high = good
    probs = [0]*len(results)
    probs[0]=1
    children = zip(*results)[2]
    scores = zip(*results)[0]
    return zip(probs, scores, children)

# Takes list of (score, confidence, board), color, and points to invest
# Returns list of (points, board) for investments
def dummyPointAllocator( edgeInfo, color, points ):
    if len(edgeInfo) == 0:
        return []
    if len(edgeInfo) < 3:
        return [(points, edgeInfo[0][2])]
    sorted_edgeInfo = sorted(edgeInfo, key=itemgetter(0), reverse=(color == chess.WHITE))
    investments = [(math.ceil(points/2.0),sorted_edgeInfo[0][2])]
    investments += [(math.floor(points/4.0),sorted_edgeInfo[1][2])]
    investments += [(math.floor(points/4.0),sorted_edgeInfo[2][2])]
    return investments


# Shouldn't be dupicated w/ chess_game
def makeMoves( node ):
    moves = []
    for m in iter(node.legal_moves):
        moves = moves + [m]
    return moves

# Returns (score, confidence, child) for each child, combines them to set
# values for the node.  Made to be called recursively starting at the root
# probScorer is a function with input list of (scores, confidences, child) and color of person to move,
#           returning list of (probabilities, scores, child) for use in updating edges
# my_move means this board is being evaluated as a possiblity after I have moved (other after opponent)
def scoreChild(cyborg, board_fen, probScorer, color):
    children = cyborg.g.successors(board_fen)
    if (len(children) == 0):
        return (cyborg.g.node[board_fen]['score'], cyborg.g.node[board_fen]['conf'], board_fen)
    # Turns alternate as you go up the tree
    child_results = []
    for child in children:
        child_results += [scoreChild(cyborg, child, probScorer, opColor(color))]
    # Calculate probabilities based on scores and confidences and assign to edges
    probScoreChildList = probScorer(child_results, color, cyborg.color)
    # Annotate edges with probability
    cyborg.annotateEdges(board_fen, probScoreChildList)
    # Calculate this board's score using child scores and probabilities
    #my_score = sum(map(lambda (p,s,c):p*s, probScoreChildList))
    my_score = 0
    for (p,s,c) in probScoreChildList:
        my_score += p*s
    # Sum confidences for children
    my_conf = sum(map(lambda (s, c, b):c, child_results))
    # Return score and confidenc
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
    my_move = not(board.turn == cyborg.color)
    for (thisBoard_fen,nextBoard_fen,move) in nextMoves:
        paInput += [(cyborg.g.node[nextBoard_fen]['score'], cyborg.g.node[nextBoard_fen]['conf'],nextBoard_fen)]
    # Get back list of (points to invest, board as fen)
    investmentList = cyborg.pointAllocator( paInput, board.turn, points )
    # Call expandGraph for calculated number of points on the board from each move
    for (movePoints, board_fen) in investmentList:
        expandGraph( cyborg, movePoints, chess.Board(board_fen), pointAllocator)

def printChildren( c, board, prefix, depth, line ):
    if depth > 0:
        edges = c.getMoveEdges( board )
        for e in edges:
            if (not(line) or e[2]['prob'] > 0 ):#or c.g.node[e[1]]['conf']==1):
                print prefix, "Move: ", e[2]['move'], " prob ", e[2]['prob'], " score ", c.g.node[e[1]]['score'], " conf ", c.g.node[e[1]]['conf']
                if (line):
                    c.current_board.push(e[2]['move'])
                    print c.current_board
                printChildren( c, chess.Board(e[1]), prefix + "  ", depth-1, line)
    return


class cyborg:
    def __init__(self, boardScorer, board=chess.Board(), color=chess.WHITE, probScorer=dummyProbScorer,
                 pointAllocator=dummyPointAllocator, pointsPerMove = 40):
        self.g = nx.DiGraph()
        self.current_board = board.copy()
        self.color = color
        self.boardScorer = boardScorer
        self.probScorer = probScorer
        self.pointAllocator = pointAllocator
        self.addNode( (self.current_board, board, 1, 0, None) )
        self.pointsPerMove = pointsPerMove
        return


    def addNode(self, (parentBoard, newBoard, c, s, m)):
        self.g.add_node(newBoard.fen(), conf=c, score=s)
        if (m != None):
            self.g.add_edge(parentBoard.fen(), newBoard.fen(), move=m)
        return

    def getMoveEdges(self, board = None ):
        if (board == None):
            board = c.current_board
        return self.g.out_edges(board.fen(), data=True)


    def expandNode(self, board):
        # Set confidence to 1 since we're spending a point
        moves = makeMoves( board )
        nodeInfo = []
        # Penalty for not your move (symmetrical)
        move_polarity = 1 if (board.turn == chess.WHITE) else -1
        for m in moves:
            board.push(m)
            newBoard = board.copy()
            board.pop()
            nodeInfo += [(board, newBoard, 1, self.boardScorer(newBoard, board.turn) + (move_polarity * 15), m)] # Confidence of new board is 1
        map(self.addNode, nodeInfo)
#        self.g.node[board.fen()]['conf']=1
        return

    def Score(self):
        # I had to make scoreChild an external function because I couldn't figure out
        # how to do recursion using methods :(
        scoreChild(self, self.current_board.fen(), self.probScorer, self.current_board.turn == self.color)
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
#        print scoredMoves
        if (self.color == chess.WHITE):
            bestMove = max(scoredMoves,key=itemgetter(1))
        else:
            bestMove = min(scoredMoves,key=itemgetter(1))
        return bestMove[0]

    # Designed to be the right function for 'game' to call
    def chooseMove( self, board = None ):
# Need some smarts here that I can't figure out right now
        for i in range(0,8):
            self.Build( math.ceil(self.pointsPerMove/8))
        print 'Built to ', len(self.g.nodes()), ' nodes'
        return self.getNextMove()

    def acceptMove( self, move ):
        # This is where we move current board up the graph to other player's move
        self.current_board.push(move)
        return

    def printGraph( self, board = None, depth=3, line=False ):
        board = board if (board != None) else self.current_board
        temp = self.current_board.copy()
        printChildren( self, board, "", depth, line)
        self.current_board = temp
        return
        
        
            
