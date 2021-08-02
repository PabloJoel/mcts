import pygame
import time

def draw_moves(screen, screen_size, game, moves):

    yellow = (255,247,0,100)
    #screen_rect = screen.get_rect()

    #see_through = pygame.Surface((screen_size,screen_size)).convert_alpha()
    #see_through.fill(yellow)
    #see_through_rect = see_through.get_rect(bottomleft=screen_rect.center)

    if moves is not None:
        for move in moves:
            if game.next_player:
                current_tiles = game.black_tiles
                next_tiles = move.black_tiles
            else:
                current_tiles = game.white_tiles
                next_tiles = move.white_tiles
        
        #screen.blit(see_through, see_through_rect)
        #pygame.display.update()
    
        tile_size = screen_size/10

        for tile in next_tiles:
            if not (tile in current_tiles):
                draw_rect_alpha(screen, yellow, (tile_size*(tile[0]+1), tile_size*(tile[1]+1), tile_size, tile_size))
        
        

def draw_rect_alpha(screen, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    screen.blit(shape_surf, rect)
