import pygame

class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text, x, y, w, h, font, color, bg="black"):
        self.x, self.y = x,y
        self.w, self.h = w,h
        self.font = font
        self.color = color
        self.background_color = bg
        self.rect = pygame.Rect(x, y, w, h)
        self.text = font.render(text, True, color)
 
    def draw(self, screen):
        screen.blit(self.text, (self.x, self.y))
        pygame.draw.rect(screen, self.color, self.rect, 2)
 
    def mouse_click(self, event):
        """ checks if you click the mouse button and then if it's on the button """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.clicked():
                    return 1
                    pass
        return 0
 
    def clicked(self):
        """ checks if the moouse is on the button """
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            return 1
            pass
        return 0