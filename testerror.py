from CheckersGame import CheckersGame

black = {(0,0):False,(3,5):False,(3,1):False}
white = {(6,2):False,(5,1):False,(6,0):False,(0,2):True}

game = CheckersGame(black_tiles=black,white_tiles=white, next_player=False)
moves = game.generateMoves()

print(0)