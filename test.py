execfile('cyborg.py')
execfile('chess_game.py')
execfile('BetterProbScore.py')
execfile('New Allocator.py')

#b = chess.Board()

c = cyborg( boardScorer=pigglyv3, pointsPerMove= 10, pointAllocator=PointAllocator)#, probScorer = Betterprobscore )
c1 = cyborg( boardScorer=pigglyv3, pointsPerMove= 100, color=chess.BLACK )

c.Build(1)
c1.Build(1)

#c1.acceptMove(chess.Move.from_uci('e2e4'))

#c1.Build(1)

#c.expandNode(c.current_board)

#c.Build(100)

#c.acceptMove(chess.Move.from_uci('e2e4'))
#c.acceptMove(chess.Move.from_uci('e7e5'))
#c.Build(20)
#c.chooseMove()


#c.expandNode(c.current_board)
#c.Score()
#c.Build( 5 )
#c.getScoredMoves()

#c.chooseMove( g.board )


#g = game(white='naivePigglyv2', black='naivePigglyv3' )
g = game(white='c.chooseMove', black='c1.chooseMove', white_apply=c.acceptMove, black_apply=c1.acceptMove)
#g = game(white='naivePigglyv3', black='c1.chooseMove', black_apply=c1.acceptMove)

g.play(pause = False)

