execfile('cyborg.py')
execfile('chess_game.py')
execfile('Cheryl.py')
execfile('Cherlene.py')
execfile('New Allocator Simpler.py')
execfile('CherylProbScore.py')
execfile('Pam.py')
b = chess.Board('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2')

c = cyborg( boardScorer=Pam, timeLimit = 36.0, color=chess.WHITE,  probScorer=CherylProbScorer, pointAllocator=SimplePointAllocator, loadSize=80, searchWidth = 800)
c1 = cyborg( boardScorer=Pam, timeLimit = 12.0, color=chess.BLACK,  probScorer=CherylProbScorer, pointAllocator=SimplePointAllocator, loadSize=60, searchWidth = 120)


#c.expandNode(c.current_board)

#c.Build(1)

#c.acceptMove(chess.Move.from_uci('e2e4'))
#c.acceptMove(chess.Move.from_uci('e7e5'))
#c.Build(20)
#c.chooseMove()


#Expand Node is creating leaves that don't include history - all just moves from starting board


#c.expandNode(c.current_board)
#c.Score()
#c.Build( 5 )
#c.getScoredMoves()

#c.chooseMove( g.board )

# Status - just fixed error where all nodes were added to the root
# Seems like some things were only working because of it...

#c.Score()

g = game(white='c.chooseMove', black='c1.chooseMove', white_apply=c.acceptMove, black_apply=c1.acceptMove)
#g = game(white='c.chooseMove', black='naivePigglyv3', white_apply=c.acceptMove)
#g = game(black='c.chooseMove', white='naivePigglyv3', black_apply=c.acceptMove)


g.play(pause = False)



def SuperBuild(c):
    for n in range(25):
            CherylBuild(c)
            print "Expected Line #"
            print n
            c.printGraph(depth=99, line=True)
    c.printGraph(depth=1)
    c.printGraph(depth=2)


def CherylBuild(c):
    for n in range(8):
        c.Build(100)
