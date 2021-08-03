import pygame
from option_box import OptionBox
import InputBox as ib
import Button as bt

import RandomPlayer as rp
import HumanPlayer as hp
import UCTPlayer as up

import CheckersGame as cg

pygame.init()
pygame.font.init()

def menu(screen, size_screen):
    #Caption
    pygame.display.set_caption("Game Menu")

    #Background image
    menu_background = pygame.image.load("madera blanco.jpg")
    menu_background = pygame.transform.scale(menu_background, (size_screen, size_screen))

    #Fonts
    font_box = pygame.font.Font('IndieFlower.ttf', int(size_screen/38))
    font_player = pygame.font.Font('IndieFlower.ttf', int(size_screen/30))
    font_game = pygame.font.Font('IndieFlower.ttf', int(size_screen/20))

    #Option Box to select a player
    list1 = OptionBox(size_screen/2, size_screen/2.6, size_screen*0.22, size_screen*0.053, 
        (255, 255, 255), (172, 232, 242), (77, 106, 149), 
        font_box, ["Human Player", "Random Player", "MCTS Player"])

    list2 = OptionBox(size_screen/2, size_screen/1.69, size_screen*0.22, size_screen*0.053, 
        (255, 255, 255), (172, 232, 242), (77, 106, 149), 
        font_box, ["Human Player", "Random Player", "MCTS Player"])

    #Player choosed
    player1, player2 = 0,0

    #Input box to input number of iterations
    input_box1 = ib.InputBox(size_screen/2, size_screen/2.2, size_screen*0.1, size_screen*0.053, '100')
    input_box2 = ib.InputBox(size_screen/2, size_screen/1.51, size_screen*0.1, size_screen*0.053, '100')
    input_boxes = [input_box1, input_box2]

    #Button to start
    start_button = bt.Button('Start',size_screen/2.3, size_screen/1.11, size_screen*0.1,size_screen*0.053,font_player,(77,106,149),'white')

    #Main loop
    running = True
    while running:
        #Events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            for box in input_boxes: #Events for input box
                box.handle_event(event)
            if start_button.mouse_click(event):
                return create_player(player1, int(input_box1.text), player2, int(input_box2.text))

        #Change player 1 chosen
        chosen_player = list1.update(events)
        if chosen_player >= 0:
            player1 = chosen_player

        #Change player 2 chosen
        chosen_player = list2.update(events)
        if chosen_player >= 0:
            player2 = chosen_player

        #Draw the background
        screen.blit(menu_background,(0,0))

        #Draw the option box again
        list1.draw(screen)
        list2.draw(screen)

        #Draw the button again
        start_button.draw(screen)

        #Checkers title
        label = font_game.render("Checkers", 1, (77,106,149))
        screen.blit(label, (size_screen/2.5, size_screen/5))

        #Player 1 text
        label = font_player.render("Player 1:", 1, (77,106,149))
        screen.blit(label, (size_screen/3, size_screen/2.65))

        #Player 2 text
        label = font_player.render("Player 2:", 1, (77,106,149))
        screen.blit(label, (size_screen/3, size_screen/1.72))

        #Update the info of the input box
        for box in input_boxes:
            box.update()

        #If MCTS Player is chosen the display the input box for the number of iterations
        if player1 == 2:
            label = font_box.render("Number of iterations:", 1, (77,106,149))
            screen.blit(label, (size_screen/5, size_screen/2.2))

            input_box1.draw(screen)

        if player2 == 2:
            label = font_box.render("Number of iterations:", 1, (77,106,149))
            screen.blit(label, (size_screen/5, size_screen/1.51))

            input_box2.draw(screen)

        pygame.display.flip()

    return 'Quit'

def create_player(player1, iter1, player2, iter2):
        if player1 == 0:
            pl1 = hp.HumanPlayer()
        elif player1 == 1:
            pl1 = rp.RandomPlayer(show=False)
        elif player1 == 2:
            pl1 = up.UCTPlayer(game=cg.CheckersGame(), type_game='checkers', iter=iter1)

        if player2 == 0:
            pl2 = hp.HumanPlayer()
        elif player1 == 1:
            pl2 = rp.RandomPlayer(show=False)
        elif player1 == 2:
            pl2 = up.UCTPlayer(game=cg.CheckersGame(), type_game='checkers', iter=iter2)

        return (pl1,pl2)