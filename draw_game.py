import pygame
from draw_board import draw_board
from CheckersGame import CheckersGame

pygame.init()
pygame.font.init()

#caption
pygame.display.set_caption("Checkers Game")

#beginning of logic
gameExit = False

#Draw board 
draw_board(CheckersGame())

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

#quit from pygame & python
pygame.quit()
quit()