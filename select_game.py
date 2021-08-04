import pygame

def draw_moves(screen, screen_size, game, moves):
    pygame.init()

        
        running = True
        while(running):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                   
                                

