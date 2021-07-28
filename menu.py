import pygame
from option_box import OptionBox

pygame.init()
pygame.font.init()

pygame.display.set_caption("Game Menu")

size_screen = 750
screen = pygame.display.set_mode((size_screen,size_screen))

white = (255,255,255)
screen.fill(white)

menu = pygame.image.load("madera blanco.jpg")
menu = pygame.transform.scale(menu, (size_screen, size_screen))

font_box = pygame.font.Font('IndieFlower.ttf', int(size_screen/38))
font_player = pygame.font.Font('IndieFlower.ttf', int(size_screen/30))
font_game = pygame.font.Font('IndieFlower.ttf', int(size_screen/20))

list1 = OptionBox(size_screen/2, size_screen/2.6, size_screen*0.22, size_screen*0.053, 
    (255, 255, 255), (172, 232, 242), (77, 106, 149), 
    font_box, ["Human Player", "Random Player", "MCTS Player"])

list2 = OptionBox(size_screen/2, size_screen/1.69, size_screen*0.22, size_screen*0.053, 
    (255, 255, 255), (172, 232, 242), (77, 106, 149), 
    font_box, ["Human Player", "Random Player", "MCTS Player"])

player1, player2 = 0,0


start_button = pygame.Rect(200, 200, size_screen*0.22, size_screen*0.053)
input_iter_1 = pygame.Rect(300, 300, size_screen*0.22, size_screen*0.053)
input_iter_2 = pygame.Rect(size_screen/2, size_screen/2, size_screen*0.22, size_screen*0.053)

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                active = True
                print('Click')
            else:
                active = False
    
    chosen_player = list1.update(events)
    if chosen_player >= 0:
        player1 = chosen_player

    chosen_player = list2.update(events)
    if chosen_player >= 0:
        player2 = chosen_player


    screen.blit(menu,(0,0))
    list1.draw(screen)
    list2.draw(screen)

    label = font_game.render("Checkers", 1, (77,106,149))
    screen.blit(label, (size_screen/2.5, size_screen/5))

    label = font_player.render("Player 1:", 1, (77,106,149))
    screen.blit(label, (size_screen/3, size_screen/2.65))

    label = font_player.render("Player 2:", 1, (77,106,149))
    screen.blit(label, (size_screen/3, size_screen/1.72))

    if player1 == 2:
        pygame.draw.rect(screen,'blue', input_iter_1)

    if player2 == 2:
        pygame.draw.rect(screen,'green', input_iter_2)

    pygame.draw.rect(screen,'red',start_button)

    pygame.display.flip()

pygame.quit()
quit()