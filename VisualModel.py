#import utilities
import time
import pygame
import draw_game as dg
import UCTPlayer as up
import HumanPlayer as hp

def play(screen, screen_size, game, player1, player2):
    """ Play the game
    """
    pygame.init()

    current_game = game
    turn1 = current_game.next_player
    all_moves = dict()

    dg.draw_game(screen, screen_size, current_game)

    running = True
    while(running):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                
        msg = None
        print('Hola')

        if turn1:
            player_color = 'Black'
        else:
            player_color = 'White'

        moves = current_game.generateMoves()
        
        if not moves:
            running = False
            msg = f'{player_color} has lost'
            dg.draw_game(screen, screen_size, current_game, msg) 
        else:
            if (turn1 and isinstance(player1, hp.HumanPlayer)) or (not turn1 and isinstance(player2, hp.HumanPlayer)):
                chosen = dg.draw_game(screen, screen_size, game=current_game, moves=moves)
            else:
                chosen = dg.draw_game(screen, screen_size, game=current_game, moves=moves)
            
            start = time.time()
            if turn1:
                if isinstance(player1, up.UCTPlayer):
                    chosen = player1.chooseMove(current_game)
                elif not isinstance(player1, hp.HumanPlayer):
                    chosen = player1.chooseMove(moves)
            else:
                if isinstance(player2, up.UCTPlayer):
                    chosen = player2.chooseMove(current_game)
                elif not isinstance(player2, hp.HumanPlayer):
                    chosen = player2.chooseMove(moves)
            end = time.time()

            dif = end - start
            if dif < 3:
                time.sleep(3-dif)

            #Repeat position
            if current_game in all_moves:
                all_moves[current_game] += 1
            else:
                all_moves.update({current_game:1})

            # Draw because of definition 1.32.1
            if all_moves[current_game] > 2:
                msg = 'Draw because of condition 1.32.1'
                running = False

            # Draw because of definition 1.32.2
            if current_game.cond1 > 40 and current_game.cond2 > 40:
                msg = 'Draw because of condition 1.32.2'
                running = False
            
            current_game = chosen
            dg.draw_game(screen, screen_size, game=current_game, msg=msg)
            turn1 = current_game.next_player
    

