import chess
import random
import datetime

def makeMoves( node ):
    moves = []
    for m in iter(node.legal_moves):
        moves = moves + [m]
    return moves

def scorePiece( piece ):
    if (piece == chess.PAWN ) : return 100
    if (piece == chess.KNIGHT ) : return 330
    if (piece == chess.BISHOP ) : return 370
    if (piece == chess.ROOK ) : return 500
    if (piece == chess.QUEEN ) : return 900
    if (piece == chess.KING ) : return 1000   #  this needs to be considered more for uneven stacks
    

def scoreSquare( node, sq ):
    return scorePiece(node.piece_at( sq ))

def opColor( color ):
    return chess.WHITE if (color == chess.BLACK) else chess.BLACK

def attackScore( board, color, sq_value = 6 ):
    op_color = opColor( color )
    my_attacks = []
    op_attacks = []
    for sq in chess.SQUARES: # or use an array?  Right now I'm assuming sq comes in numerical order
        #for attacking_sq in board.attacking_squares(chess.WHITE, sq):
        my_attacks = my_attacks + [len(board.attackers(color, sq))]
        op_attacks = op_attacks + [len(board.attackers(op_color, sq))]
        delta_attacks = map(lambda x,y: sq_value if (x>y) else (-sq_value if (x<y) else (0)), my_attacks, op_attacks)
    return sum(delta_attacks)

# Returns true if opponent would take piece at this square
# Color = person who just moved and is vulnerable to attack
#
# NOTE / TODO:  This returns incorrectly if one of the pieces is blocking a later one
#
def dogPile( board, sq, color ):
    op_color = opColor( color )
    op_pieces = map(scorePiece, map(lambda p: board.piece_at(p).piece_type, board.attackers(op_color, sq)))
#    print "OP", op_pieces
    if (len(op_pieces) == 0):
        return False # No attackers, no take
    list.sort(op_pieces, reverse=True)
    op_pieces = map(lambda x: -x, op_pieces)
    my_pieces = map(scorePiece, map(lambda p: board.piece_at(p).piece_type, board.attackers(color, sq)))
    list.sort(my_pieces, reverse=True)
#    print "MP", my_pieces
    if (len(my_pieces) == 0):
        return True  # No defenders, piece is lost
    # Make ordered list of alternating pieces sorted by value (for each color)
    combination = [scorePiece(board.piece_at(sq).piece_type)]
    while (len(my_pieces)>0 and len(op_pieces) > 0):
#        print "adding"
        combination += [op_pieces.pop(), my_pieces.pop()]
#        print "NC", combination
    #  In theory I add the last op piece if there is one, but then I need to pop one off
    #  So I just pop if there isn't another op piece
    if (len(op_pieces) == 0):
        combination.pop()
#    print "C", combination
    return (reduce(lambda x, y: x+y, combination) > 0)
    
    
def allPieceSquares( node, color ):
    pieces = node.pieces( chess.PAWN, color ).union( node.pieces( chess.KNIGHT, color ))
    pieces = pieces.union( node.pieces( chess.BISHOP, color )).union( node.pieces( chess.ROOK, color ))
    return pieces.union( node.pieces( chess.QUEEN, color ) )
    


def calculateMaterialScore( node, color ):
    def doPiece( p, color ):
        return len(node.pieces( p, color )) * scorePiece( p )
    s = doPiece( chess.PAWN, color )
    s += doPiece( chess.KNIGHT, color )
    s += doPiece( chess.BISHOP, color )
    s += doPiece( chess.ROOK, color )
    s += doPiece( chess.QUEEN, color )
    return s


def calculateNetCover( node, color, op_color, sq ):
    attacks = node.attackers( op_color, sq )
    defenders = node.attackers( color, sq )
    net = 0
    for a in attacks:
        net -= scoreSquare( node, a )
    for d in defenders:
        net += scoreSquare( node, d )
    return net

def naiveShell( boardScorer, node ):    
    moves = makeMoves( node );
    scored_moves = dict()
    best_score = -10000
    # Color is 'my' color for purpose of scoring
    color = node.turn
    for m in moves:
        node.push(m)
        score = boardScorer( node, color )
        scored_moves[m] = score
        if (score >= best_score):
            best_score = score
        node.pop()
    top_moves = {k: v for k, v in scored_moves.iteritems() if v >= best_score - 100}
    if (len(top_moves) == 0 ):
        print "Error - no top moves ", scored_moves
    return list(top_moves)[random.randrange(0,len(top_moves))]

def naivePiggly( node ):
    return naiveShell( piggly, node )

def naivePigglyv2( node ):
    return naiveShell( pigglyv2, node )

def naivePigglyv3( node ):
    return naiveShell( pigglyv3, node )

def pigglyv2( node, color ):
    op_color = opColor( color )
    my_mat = calculateMaterialScore( node, color )
    op_mat = calculateMaterialScore( node, op_color )
    # early out if it's checkmate
    if (node.is_checkmate()):
        return 10000
    if (node.is_stalemate() and my_mat > op_mat ):
        return -5000
    my_squares = allPieceSquares(  node, color )
    score = my_mat - op_mat
    return score


def piggly( node, color ):
    op_color = opColor(color)
    my_mat = calculateMaterialScore( node, color )
    op_mat = calculateMaterialScore( node, op_color )
    # early out if it's checkmate
    if (node.is_checkmate()):
        return 10000
    if (node.is_stalemate() and my_mat > op_mat ):
        return -5000
    return my_mat - op_mat


# Piggly always scores up = good for this player
def pigglyv3( node, color ):
    op_color = opColor(color)
    score_polarity = 1
    my_mat = calculateMaterialScore( node, color )
    op_mat = calculateMaterialScore( node, op_color )
    # early out if it's checkmate
    if (node.is_checkmate()):
        return 10000 * score_polarity
    if (node.is_stalemate() and my_mat > op_mat ):
        return -5000 * score_polarity
    score = my_mat - op_mat
    my_squares = allPieceSquares(  node, color )
    for sq in my_squares:
        if (dogPile(node, sq, color)):
            score -= scorePiece( node.piece_at(sq).piece_type )  # Remove 'lost' piece
    score += attackScore( node, color )
    return score * score_polarity


def pigglyv4( node, color ):
    op_color = opColor(color)
    score_polarity = 1 if (color == chess.WHITE) else -1
    my_mat = calculateMaterialScore( node, color )
    op_mat = calculateMaterialScore( node, op_color )
    # early out if it's checkmate
    if (node.is_checkmate()):
        return 10000 * score_polarity
    if (node.is_stalemate() and my_mat > op_mat ):
        return -5000 * score_polarity
    score = my_mat - op_mat
    my_squares = allPieceSquares(  node, color )
    for sq in my_squares:
        if (dogPile(node, sq, color)):
            score -= scorePiece( node.piece_at(sq).piece_type )  # Remove 'lost' piece
    score += attackScore( node, color )
    return score * score_polarity


def rando( node ):
    moves = makeMoves( node );
    return moves[random.randrange(0,len(moves))]

def human( node ):
    while (1):
        m_input = raw_input('Your move (uci): ')
        if (len(m_input) == 4 or len(m_input) == 5):
            m = chess.Move.from_uci(m_input)
            if (m in node.legal_moves):
                return m
        print('Not a legal move')
        print makeMoves( node )


class game:
    def __init__( self, white = 'human', black = 'rando', white_apply = None,
                  black_apply = None, verbose = True ):
        self.board = chess.Board()
        self.white = white
        self.white_apply = white_apply
        self.black = black
        self.black_apply = black_apply
        self.verbose = verbose
#        self.pgn_game = chess.pgn.Game()
#        self.pgn_game.headers['White'] = white
#        self.pgn_game.headers['Black'] = black
#        self.pgn_game.headers['Date'] = datetime.date
 #       self.pgn_handle = open( 'gamelog-' + str(datetime.date.today()), 'w')

    def debug( self, note ):
        if (self.verbose):
            print( note )
            print( self.board ) 

    def apply_move( self, move ):
#  Add PGN logging when you have a chance
#        self.pgn_game.
	self.board.push(move)
        if (self.black_apply != None):
            self.black_apply(move)
        if (self.white_apply != None):
            self.white_apply(move)
        

    def turn( self ):
        exec('w_move = ' + self.white + '(self.board)')
        self.apply_move(w_move)
        self.debug('White moves: ' + str(w_move) )
        if (self.board.is_game_over()):
            return self.board.result()
        exec('b_move = ' + self.black + '(self.board)')
        print(b_move)
        self.apply_move(b_move)
        self.debug('Black moves: ' + str(b_move) )
        if (self.board.is_game_over()):            
            return self.board.result()

    def play( self, pause = True ):
        while ( not(self.board.is_game_over()) ):
            self.turn()
            if (self.board.is_game_over()):
                print "White: ", self.white, " -  Black: ", self.black
                print self.board.result()
                return self.board.result()
            if (pause):
                raw_input('<Enter to continue>\n')
