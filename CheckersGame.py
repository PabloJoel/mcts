import copy
import numpy as np
from numpy.lib.function_base import blackman
from GameInterface import GameInterface

class CheckersGame(GameInterface):
    
    def __init__(self, black_tiles=None, white_tiles=None, next_player=True, matrix=None, cond1=0, cond2=0):
        """Constructor: it can take the parameters to create an specific board (black tiles and white tiles) or a numpy matrix
            (the board) or no parameters to create the default board
        """
        if matrix is not None:
            black_tiles = {}
            white_tiles = {}
            it = np.nditer(matrix, flags=['multi_index'])
            for x in it:
                position = it.multi_index
                position_final = (7-position[0], position[1])
                if x == 1:
                    black_tiles.update({position_final:False})
                elif x == 11:
                    black_tiles.update({position_final:True})
                elif x == 2:
                    white_tiles.update({position_final:False})
                elif x == 22:
                    white_tiles.update({position_final:True})
                elif x != 0:
                    raise ValueError('Incorrect data')
            self.black_tiles = black_tiles
            self.white_tiles = white_tiles
        elif black_tiles is not None and white_tiles is not None:
            #Create game with existing values
            self.black_tiles = black_tiles
            self.white_tiles = white_tiles
        else:
            #Create new game
            self.black_tiles, self.white_tiles = self.generateBoard()
        self.next_player = next_player
        self.cond1 = cond1 #First condition for draw: neither player has advanced an uncrowned piece towards the king-row in 40 moves
        self.cond2 = cond2 #Second condition for draw: no pieces had been eaten in 40 moves

    def generateBoard(self):
        """Generate the board in 2 parts, the black and the white tiles
        """
        black_tiles = CheckersGame.__generate_tiles([0,1,2])
        white_tiles = CheckersGame.__generate_tiles([5,6,7])
        return (black_tiles,white_tiles)

    def __generate_tiles(rows):
        """Internal function to create the black or white tiles
        """
        tiles = dict()
        for row in rows:
            if row%2==0:
                tile_offset = 0
            else:
                tile_offset = 1

            for col in range(4):
                position = (row,tile_offset)
                tiles.update({position: False})
                tile_offset += 2
        return tiles

    def generateMoves(self):
        """Generate all the posible moves, they are return as a list of boards
        """
        jump = self.generateJumpMoves()
        if not jump:
            simple = self.generateSimpleMoves()
            if not simple:
                return list()
            else:
                return simple
        else:
            return jump

    def generateSimpleMoves(self):
        """Returns all the posible simple moves of my board
        """
        result = list()

        if self.next_player:
            team_list = self.black_tiles
        else:
            team_list = self.white_tiles

        #Iterate over every tile of my colour
        for current_position, rank in team_list.items():
            result.extend(self.__generateSimpleMoves1Tile(current_position, rank))
        return result 
    
    def __generateSimpleMoves1Tile(self, tile_position, rank):
        """Generate simple moves of 1 specific tile
        """
        result = list()

        if self.next_player:
            team_list = self.black_tiles
            enemy_list = self.white_tiles
        else:
            team_list = self.white_tiles
            enemy_list = self.black_tiles

        result.extend(CheckersGame.__generateSimpleUpMoves(enemy_list, team_list, self.next_player, rank, tile_position, self.cond1, self.cond2))
        result.extend(CheckersGame.__generateSimpleDownMoves(enemy_list, team_list, self.next_player, rank, tile_position, self.cond1, self.cond2))
        return result 

    def __generateSimpleUpMoves(enemy_list, team_list, color, rank, current_position, cond1, cond2):
        """Return the diferent new positions that can be achieved through a simple up move
        """
        moves = list()
        if color or rank:
            #Black peon/queen or white queen
            if current_position[0] < 7:
                
                #Left
                final_position = (current_position[0]+1, current_position[1]-1)
                if current_position[1] > 0 and not(final_position in enemy_list or final_position in team_list):
                    moves.append(CheckersGame.__new_move(enemy_list, team_list, final_position, current_position, color, rank, cond1, cond2))
            
                #Right
                final_position = (current_position[0]+1, current_position[1]+1)
                if current_position[1] < 7 and not(final_position in enemy_list or final_position in team_list):
                    moves.append(CheckersGame.__new_move(enemy_list, team_list, final_position, current_position, color, rank, cond1, cond2))
        return moves    

    def __generateSimpleDownMoves(enemy_list, team_list, color, rank, current_position, cond1, cond2):
        """Return the diferent new positions that can be achieved through a simple down move
        """
        moves = list()
        if not color or rank:
            #White peon/queen or black queen
            if current_position[0] > 0:
                
                #Left
                final_position = (current_position[0]-1, current_position[1]-1)
                if current_position[1] > 0 and not(final_position in enemy_list or final_position in team_list):
                    moves.append(CheckersGame.__new_move(enemy_list, team_list, final_position, current_position, color, rank, cond1, cond2))

                #Right
                final_position = (current_position[0]-1, current_position[1]+1)
                if current_position[1] < 7 and not(final_position in enemy_list or final_position in team_list):
                    moves.append(CheckersGame.__new_move(enemy_list, team_list, final_position, current_position, color, rank, cond1, cond2))
        return moves

    def generateJumpMoves(self):
        """Returns all the posible jump moves of my board
        """
        result = list()

        if self.next_player:
            team_list = self.black_tiles
        else:
            team_list = self.white_tiles

        #Iterate over every tile of my colour
        for current_position, rank in team_list.items():
            result.extend(self.__generateJumpMoves1Tile(current_position, rank))
        return result
            
    def __generateJumpMoves1Tile(self, tile_position, rank):
        """Generate simple moves of 1 specific tile, recursively
        """
        result = list()

        if self.next_player:
            team_list = self.black_tiles
            enemy_list = self.white_tiles
        else:
            team_list = self.white_tiles
            enemy_list = self.black_tiles

        eatup   = CheckersGame.__generateJumpUpMoves(enemy_list, team_list, self.next_player, rank, tile_position, self.cond1, self.cond2)
        eatdown = CheckersGame.__generateJumpDownMoves(enemy_list, team_list, self.next_player, rank, tile_position, self.cond1, self.cond2)
        eatup.extend(eatdown)

        #Empty, no moves
        if not eatup:
            res = list()
            return res
        else:
            #There are more moves
            for move in eatup:
                queen = False
                if not team_list.get(tile_position):  #If the tile was not a queen
                    if move[0].next_player: #Black tile
                        if move[0].black_tiles.get(move[1]):  #It is now a Queen
                            queen = True
                    else: #White tile
                        if move[0].white_tiles.get(move[1]): #It is now a Queen
                            queen = True

                if queen: #Transformation into a queen, recursive search stops
                    extended_moves = list()
                else:
                    extended_moves = move[0].__generateJumpMoves1Tile(move[1], rank)

                if not extended_moves:
                    #empty list, no more movements or queen transformation
                    extended_moves = list()
                    move[0].next_player = not move[0].next_player
                    extended_moves.append(move[0])
                result.extend(extended_moves)
            return result 
                    

    def __generateJumpUpMoves(enemy_list, team_list, color, rank, current_position, cond1, cond2):
        """Return the diferent new positions that can be achieved through an eating up move
        """
        moves = list()
        if color or rank:
            #Black peon/queen or white queen
            if current_position[0] < 6:
                
                #Left
                enemy = (current_position[0]+1, current_position[1]-1)
                final_position = (current_position[0]+2, current_position[1]-2)
                if current_position[1] > 1 and enemy in enemy_list and not(final_position in enemy_list or final_position in team_list):
                    moves.append( (CheckersGame.__new_move(enemy_list, team_list, final_position, current_position, color, rank, cond1, cond2, enemy), final_position) )
            
                #Right
                enemy = (current_position[0]+1, current_position[1]+1)
                final_position = (current_position[0]+2, current_position[1]+2)
                if current_position[1] < 6 and enemy in enemy_list and not(final_position in enemy_list or final_position in team_list):
                    moves.append( (CheckersGame.__new_move(enemy_list, team_list, final_position, current_position, color, rank, cond1, cond2, enemy), final_position) )
        return moves    

    def __generateJumpDownMoves(enemy_list, team_list, color, rank, current_position, cond1, cond2):
        """Return the diferent new positions that can be achieved through an eating down move
        """
        moves = list()
        if not color or rank:
            #White peon/queen or black queen
            if current_position[0] > 1:
                
                #Left
                enemy = (current_position[0]-1, current_position[1]-1)
                final_position = (current_position[0]-2, current_position[1]-2)
                if current_position[1] > 1 and enemy in enemy_list and not(final_position in enemy_list or final_position in team_list):
                    moves.append( (CheckersGame.__new_move(enemy_list, team_list, final_position, current_position, color, rank, cond1, cond2, enemy), final_position) )

                #Right
                enemy = (current_position[0]-1, current_position[1]+1)
                final_position = (current_position[0]-2, current_position[1]+2)
                if current_position[1] < 6 and enemy in enemy_list and not(final_position in enemy_list or final_position in team_list):
                    moves.append( (CheckersGame.__new_move(enemy_list, team_list, final_position, current_position, color, rank, cond1, cond2, enemy), final_position) )
        return moves
    
    def __new_move(enemy_list, team_list, final_position, current_position, color, rank, cond1, cond2, enemy_position=None):
        """Internal function to copy a board and change it according to the final position and enemy position (if used)
        """
        #current position is modified but there should be any problem
        rank = copy.deepcopy(rank)

        cond1 += 1
        cond2 += 1
        #Checking reset of condition 1 for a draw
        if color and not rank and final_position[0] > current_position[0]:
            cond1 = 0
        elif not color and not rank and final_position[0] < current_position[0]:
            cond1 = 0

        #Checking reset for condition 2 for a draw
        if enemy_position is not None:
            cond2 = 0
          
        #Transformation into a queen
        if color and not rank and final_position[0]==7:
            rank = True
        elif not color and not rank and final_position[0]==0:
            rank = True

        enemy_copy = copy.deepcopy(enemy_list)
        team_copy = copy.deepcopy(team_list)

        if enemy_position is not None:
            enemy_copy.pop(enemy_position)      #Remove enemy killed
        team_copy.pop(current_position)         #Remove my old position
        team_copy.update({final_position:rank}) #Add my new position
        
        #Change player (only simple moves because jump is recursive)
        if enemy_position is None:
            next_color = not color
        else:
            next_color = color

        if color:
            return CheckersGame(team_copy, enemy_copy, next_color)
        else:
            return CheckersGame(enemy_copy, team_copy, next_color)

    def is_finished(self):
        # Draw because of definition 1.32.2
        if self.cond1 > 40 and self.cond2 > 40:
            return (True,0)

        #One player has lost
        if not self.black_tiles:
            return (True,False)
        elif not self.white_tiles:
            return (True,True)

        if not self.generateMoves():
            if self.next_player:
                return (True,True)
            else:
                return (True,False)

        return (False,-1)

    def __eq__(self, other):
        """Equals function to compare two CheckersGame to know if they are the same game
        """
        if self.next_player == other.next_player and self.black_tiles == other.black_tiles and self.white_tiles == other.white_tiles:
            return True
        else:
            return False
    
    def same_board(self, other):
        if self.black_tiles == other.black_tiles and self.white_tiles == other.white_tiles:
            return True
        else:
            return False

    def __hash__(self):
        return hash( (hash(tuple(self.black_tiles)), tuple(self.white_tiles), hash(self.next_player)) )

    def heuristic_eval(self):
        eval = 0

        if self.next_player:
            mult = -1
        else:
            mult = 1

        for tile in self.black_tiles:
            #Queen or peon
            if self.black_tiles.get(tile):
                eval += mult*(3)
            else:
                eval += mult*(1.5)

            """
            if not self.black_tiles.get(tile):
                if tile[0] > 2:
                    dif = tile[0]-5
                    eval += mult*(dif*0.2)
            """


        mult *= -1
        for tile in self.white_tiles:
            #Queen or peon
            if self.white_tiles.get(tile):
                eval += mult*(3)
            else:
                eval += mult*(1.5)
            """
            if not self.black_tiles.get(tile):
                if tile[0] > 2:
                    dif = 7-tile[0]-2
                    eval += mult*(dif*0.2)
             """
        
        return eval
            

    def __str__(self):
        """To string function of the board
        """
        result = '|'
        for row in range(7,-1,-1):
            for col in range(0,8):
                position = (row,col)
                if position in self.black_tiles:
                    if self.black_tiles.get(position):
                        result += 'X|'
                    else:
                        result += 'x|'
                elif position in self.white_tiles:
                    if self.white_tiles.get(position):
                        result += 'O|'
                    else:
                        result += 'o|'
                else:
                    result += ' |'
            result +='\n|'
        return result[:-1]

