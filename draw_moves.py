import pygame
import time

def draw_moves(screen, screen_size, game, moves):
    pygame.init()

    if moves is not None:
        for move in moves:
            if game.next_player:
                current_tiles = game.black_tiles
                next_tiles = move.black_tiles
            else:
                current_tiles = game.white_tiles
                next_tiles = move.white_tiles
        
            tile_size = int((screen_size/10)-2.5)
            yellow = pygame.image.load("yellow_mark.png")
            yellow = pygame.transform.scale(yellow, (tile_size, tile_size))

            for tile in next_tiles:
                if not (tile in current_tiles):
                    col = (50*tile[1])+50+2.5
                    row = (50*(tile[0]+1))+50+2.5
                    screen.blit(yellow,(col,row))#col,row
        
            pygame.display.update()
        
        running = True
        while(running):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

def draw_rect_alpha(screen, color, rect):

    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    screen.blit(shape_surf, rect)
    pygame.display.update()
