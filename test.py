execfile('cyborg.py')
execfile('chess_game.py')
#b = chess.Board()

c = cyborg( boardScorer=pigglyv3, pointsPerMove= 100 )
#c1 = cyborg( boardScorer=pigglyv3, pointsPerMove=20 )


#c.expandNode(c.current_board)

c.Build(4)

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

#g = game(white='c.chooseMove', black='c1.chooseMove', white_apply=c.acceptMove, black_apply=c1.acceptMove)
#g = game(white='c.chooseMove', black='naivePigglyv3', white_apply=c.acceptMove)
#g = game(black='c.chooseMove', white='naivePigglyv3', black_apply=c.acceptMove)

#g.play(pause = False)