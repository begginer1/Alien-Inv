import pygame.font
class Button:
    """A class to build buttons for the game."""
    def __init__(self,ai_game,msg):
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width,self.height=(200,50)
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48) #reates a font object using the default system font with a font size of 48 point
    
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height) #setting rectange at 0,0
        self.rect.center = self.screen_rect.center # placing retangke at center
        # The button message needs to be prepped only once.
        self._prep_msg(msg)
        
    def _prep_msg(self,msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color) #The call to font.render() turns the text stored in msg into an image,take msg,self  Boolean value to turn antialiasing on or off (antialiasing makes the edges of the text smoother),text color,bg color
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center
        
    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)    #We call screen.fill() to draw the rectangular portion of the button
        self.screen.blit(self.msg_image,self.msg_image_rect) #. Then we call screen.blit() to draw the text image to the screen, passing it an image and the rect object associated with the image