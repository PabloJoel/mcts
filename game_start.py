import pygame

import sys
sys.path.append("..")

import games.CheckersGame as cg
from visual.MainMenu import menu
import visual.VisualModel as vm

pygame.init()
pygame.font.init()

#Screen creation
size_screen = 500
screen = pygame.display.set_mode((size_screen,size_screen))

#Main loop
running = True
while running:
    #Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    #Menu to select type of players
    res = menu(screen, size_screen)

    if isinstance(res, str):
        running = False
    elif isinstance(res, tuple):
        #Play the game
        vm.play(screen, size_screen, cg.CheckersGame(), res[0], res[1], res[2], res[3])

pygame.quit()
quit()