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
        return (cyborg.g.node[board]['score'], cyborg.g.node[board]['conf'], board)

    # Remove parent from list if it's there - not sure if this is good...
 #   children.remove(board)

    child_results = map(lambda x: scoreChild(cyborg, x, board), children)
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

class cyborg:
    def __init__(self, board=chess.Board(), boardScorer=dummyBoardScorer, probScorer=dummyProbScorer):
        self.g = nx.DiGraph()
        self.current_board = board
        self.boardScorer = boardScorer
        self.probScorer = probScorer
        self.addNode( (board, 1, 0, None) )
        return


    def addNode(self, (b, c, s, m)):
        self.g.add_node(b, conf=c, score=s)
        print "added\n", b, "  data ", self.g.node[b]
        print "confirming ", self.g.node[b]
        if (m != None):
            self.g.add_edge(self.current_board, b, move=m)
        return

    def expandNode(self, board):
        def boardClone( board, move ):
            board.push(move)
            copy = board.copy()
            board.pop()
            return copy
        moves = makeMoves( board )
        scores = map(self.boardScorer, moves)
        boards = map(lambda x: boardClone(board, x), moves)
        nodeInfo = zip(boards, [1]*len(boards) , scores, moves) # Confidence of new board is 1
        map(self.addNode, nodeInfo)
        return

    def Score(self):
        # I had to make scoreChild an external function because I couldn't figure out
        # how to do recursion using methods :(
        scoreChild(self, self.current_board, self.probScorer)
        return

    # Takes list of triples of (prob,scores,board)
    def annotateEdges( self, from_board, tuples ):
        for psb in tuples:
            self.g.edge[from_board][psb[2]]['prob'] = psb[0]
        return

        
       
#    def build(self, board, points):
         
    
        
        
            
