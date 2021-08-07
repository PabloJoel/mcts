import pygame
import draw_board as db
import Button as bt

def select_game(screen, screen_size, games):
    pygame.init()

    selected_game = 0

    tile_size = int((screen_size/10))
    right_arrow = pygame.image.load("right_arrow.png")
    right_arrow = pygame.transform.scale(right_arrow, (tile_size, tile_size))

    left_arrow = pygame.image.load("left_arrow.png")
    left_arrow = pygame.transform.scale(left_arrow, (tile_size, tile_size))

    right_arrow_button = screen.blit(right_arrow,(screen_size/1.12, screen_size/2))
    left_arrow_button = screen.blit(left_arrow,(screen_size/90, screen_size/2))

    font_player = pygame.font.Font('IndieFlower.ttf', int(screen_size/30))
    choose_button = bt.Button(' Choose this board  ', screen_size/3.05, screen_size/1.1, screen_size*0.35, screen_size*0.053,font_player,'white',(0,204,102))
        
    running = True
    while(running):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if right_arrow_button.collidepoint(x,y):
                    if selected_game+1 < len(games):
                        selected_game += 1
                    else:
                        selected_game = 0       
                elif left_arrow_button.collidepoint(x,y):
                    if selected_game-1 >= 0:
                        selected_game -= 1
                    else:
                        selected_game = len(games)-1
                
                db.draw_board(screen, screen_size, games[selected_game], f'Board {selected_game}')
                screen.blit(right_arrow,(screen_size/1.12, screen_size/2))
                screen.blit(left_arrow,(screen_size/90, screen_size/2))
                choose_button.draw(screen)
                pygame.display.update()

            if choose_button.mouse_click(event):
                running = False
                return games[selected_game]
                      

