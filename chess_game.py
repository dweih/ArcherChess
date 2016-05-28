import chess
import random

def makeMoves( node ):
    moves = []
    for m in iter(node.legal_moves):
        moves = moves + [m]
    return moves

def scoreSquare( node, sq ):
    piece = node.piece_at( sq )
    if (piece == chess.PAWN ) : return 100
    if (piece == chess.KNIGHT ) : return 330
    if (piece == chess.BISHOP ) : return 370
    if (piece == chess.QUEEN ) : return 900
    if (piece == chess.KING ) : return 1000   #  this needs to be considered more for uneven stacks
    return 0
    

def allPieceSquares( node, color ):
    pieces = node.pieces( chess.PAWN, color ).union( node.pieces( chess.KNIGHT, color ))
    pieces = pieces.union( node.pieces( chess.BISHOP, color )).union( node.pieces( chess.ROOK, color ))
    return picees.union( node.pieces( chess.QUEEN, color ) )
    


def calculateMaterialScore( node, color, values = [1,3,3,5,9] ):
    s = len(node.pieces( chess.PAWN, color )) * values[0]    
    s += len(node.pieces( chess.KNIGHT, color )) * values[1]
    s += len(node.pieces( chess.BISHOP, color )) * values[2]
    s += len(node.pieces( chess.ROOK, color )) * values[3]
    s += len(node.pieces( chess.QUEEN, color )) * values[4]
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


def piggyv2( node ):
    color = node.turn
    op_color = chess.WHITE if (color == chess.BLACK) else chess.BLACK
    moves = makeMoves( node );
    scored_moves = dict()
    best_score = -100
    for m in moves:
        node.push(m)


def pigscore( node, color, op_color ):
    my_squares = allPieceSquares( color )
    for sq in my_squares:
        




    s = 0
    bsq = node.pieces( chess.BISHOP, color )
    s += len(bsq) * 370
    if (len(bsq) => 2): s += 30
    s+= len(bsq.intersection({chess.B2, chess.G2, chess.B7, chess.G7})) * 25
    s-= len(bsq.intersection({chess.C1, chess.C8, chess.F1, chess.F8})) * 25
    # closed...
    ksq = node.pieces( chess.BISHOP, color )
    s += len(bsq) * 330
    s-= len(ksq.intersection({chess.B1, chess.B8, chess.G1, chess.G8})) * 25
    s-= len(ksq.intersection({chess.BB_FILE_A, chess.BB_FILE_H})) * 50
    s += len(node.pieces( chess.ROOK, color )) * 500
    s += len(node.pieces( chess.QUEEN, color )) * 900


        

        






        
        my_mat = calculateMaterialScore( node, color )
        op_mat = calculateMaterialScore( node, op_color )
        # early out if it's checkmate
        if (node.is_checkmate()):
            node.pop()
            return m
        score = my_mat - op_mat
#        print str(m), " score ", score
        scored_moves[m] = score
        if (score >= best_score):
            best_score = score
        node.pop()
    top_moves = {k: v for k, v in scored_moves.iteritems() if v >= best_score - 0.5}
    return list(top_moves)[random.randrange(0,len(top_moves))]


def piggly( node ):
    color = node.turn
    op_color = chess.WHITE if (color == chess.BLACK) else chess.BLACK
    moves = makeMoves( node );
    scored_moves = dict()
    best_score = -100
    for m in moves:
        node.push(m)
        my_mat = calculateMaterialScore( node, color )
        op_mat = calculateMaterialScore( node, op_color )
        # early out if it's checkmate
        if (node.is_checkmate()):
            node.pop()
            return m
        score = my_mat - op_mat
#        print str(m), " score ", score
        scored_moves[m] = score
        if (score >= best_score):
            best_score = score
        node.pop()
    top_moves = {k: v for k, v in scored_moves.iteritems() if v >= best_score - 0.5}
    return list(top_moves)[random.randrange(0,len(top_moves))]
        

def getAttacks( color ):
    op_color = chess.WHITE if (color == chess.BLACK) else chess.BLACK
    my_attacks = []
    their_attacks = []
    net_points = []
    for sq in chess.SQUARES: # or use an array?  Right now I'm assuming sq comes in numerical order
        #for attacking_sq in board.attacking_squares(chess.WHITE, sq):
        my_attacks = my_attacks + [len(board.attackers(color, sq))]
        their_attacks = their_attacks + [len(board.attackers(op_color, sq))]
        delta_attacks = map(lambda x,y:x-y, wh_attacks, bl_attacks)
        #net = 
    return (my_attacks, their_attacks, delta_attacks)


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
    def __init__( self, white = 'human', black = 'rando', verbose = True ):
        self.board = chess.Board()
        self.white = white
        self.black = black
        self.verbose = verbose

    def debug( self, note ):
        if (self.verbose):
            print( note )
            print( self.board )        

    def turn( self ):
        exec('w_move = ' + self.white + '(self.board)')
#        print(w_move)
        self.board.push(w_move)
        self.debug('White moves: ' + str(w_move) )
        if (self.board.is_game_over()):
            return self.board.result()
        exec('b_move = ' + self.black + '(self.board)')
#        print(b_move)
        self.board.push(b_move);
        self.debug('Black moves: ' + str(b_move) )
        if (self.board.is_game_over()):
            return self.board.result()

    def play( self, pause = True ):
        while ( not(self.board.is_game_over()) ):
            self.turn()
            if (self.board.is_game_over()):
                return self.board.result()
            if (pause):
                raw_input('<Enter to continue>\n')
        print self.board.result()
        
        
                  
                  
