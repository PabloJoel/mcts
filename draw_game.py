import pygame
from draw_board import draw_board
from draw_moves import draw_moves
from CheckersGame import CheckersGame

def draw_game(screen, size_screen, game, msg=None, moves=None):
    pygame.init()
    pygame.font.init()

    #caption
    pygame.display.set_caption("Checkers Game")

    #Draw board
    draw_board(screen, size_screen, game, msg)

    draw_moves(screen, size_screen, game, moves)

    