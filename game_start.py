import pygame
import CheckersGame as cg
from MainMenu import menu
import VisualModel

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

    res = menu(screen, size_screen)
    if isinstance(res, str):
        running = False
    elif isinstance(res, tuple):
        VisualModel.play(screen, size_screen, cg.CheckersGame(), res[0], res[1], res[2], res[3])

pygame.quit()
quit()