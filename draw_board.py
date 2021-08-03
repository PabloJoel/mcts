import pygame

def draw_board(screen, size_screen, game, msg):
    #set color with rgb
    white,green = (255,255,255),(0,204,102)

    #Size of squares
    size = size_screen/10

    #board length, must be even
    boardLength = 8
    screen.fill(white)

    cnt = 0
    for i in range(1,boardLength+1):
        for z in range(1,boardLength+1):
            #check if current loop value is even
            if cnt % 2 == 0:
                pygame.draw.rect(screen, white,[size*z,size*i,size,size])
            else:
                pygame.draw.rect(screen, green, [size*z,size*i,size,size])
            cnt +=1
        #since theres an even number of squares go back one value
        cnt-=1
    #Add a nice boarder
    pygame.draw.rect(screen,green,[size,size,boardLength*size,boardLength*size],1)

    #Draw tiles
    tile_size = int(size - 5)
    white = pygame.image.load("ficha blanca.png")
    white = pygame.transform.scale(white, (tile_size, tile_size))

    white_queen = pygame.image.load("reina blanca.png")
    white_queen = pygame.transform.scale(white_queen, (tile_size, tile_size))

    red = pygame.image.load("ficha roja.png")
    red = pygame.transform.scale(red, (tile_size, tile_size))

    red_queen = pygame.image.load("reina roja.png")
    red_queen = pygame.transform.scale(red_queen, (tile_size, tile_size))

    for row in range(7,-1,-1):
            for col in range(0,8):
                position = (row,col)
                if position in game.black_tiles:
                    if game.black_tiles.get(position):
                        screen.blit(red_queen,((size*(col+1))+2.5,(size*(7-row+1))+2.5))#col,row
                    else:
                        screen.blit(red,((size*(col+1))+2.5,(size*(7-row+1))+2.5))#col,row
                elif position in game.white_tiles:
                    if game.black_tiles.get(position):
                        screen.blit(white_queen,((size*(col+1))+2.5,(size*(7-row+1))+2.5))#col,row
                    else:
                        screen.blit(white,((size*(col+1))+2.5,(size*(7-row+1))+2.5))#col,row

    myfont = pygame.font.SysFont("cambria",20)

    if msg is not None:
        label = myfont.render(msg, False, (0,0,0))
    elif game.next_player:
        label = myfont.render("Red Player's Turn", False, (0,0,0))
    else:
        label = myfont.render("White Player's Turn", False, (0,0,0))

    screen.blit(label, (size_screen/2.7, tile_size/3))

    pygame.display.update()
