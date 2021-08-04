import pygame

def draw_moves(screen, screen_size, game, moves):
    pygame.init()

    yellow_marks = dict()

    if moves is not None:
        for move in moves:
            if game.next_player:
                current_tiles = game.black_tiles
                next_tiles = move.black_tiles
            else:
                current_tiles = game.white_tiles
                next_tiles = move.white_tiles

            for tile in next_tiles:
                if not (tile in current_tiles):
                    col = (50*tile[1])+50+2.5
                    row = (50*(tile[0]+1))+50+2.5
                    mark = create_yellow(screen_size)
                    rect = screen.blit(mark,(col,row))#col,row
                    if tuple(rect) in yellow_marks:
                        yellow_marks[tuple(rect)].append(move)
                    else:
                        aux = list()
                        aux.append(move)
                        yellow_marks.update({tuple(rect):aux})
                   
        
            pygame.display.update()
        
        running = True
        while(running):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for rect in yellow_marks:
                        aux_rect = pygame.Rect((rect[0], rect[1]),(rect[2], rect[3]))
                        if aux_rect.collidepoint(x,y):
                            print(f'clicked on image: ')
                            for game in yellow_marks[rect]:
                                print(rect,game)
                                

def create_yellow(screen_size):
    tile_size = int((screen_size/10)-2.5)
    yellow = pygame.image.load("yellow_mark.png")
    yellow = pygame.transform.scale(yellow, (tile_size, tile_size))
    return yellow