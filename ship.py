import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_game): #This will give Ship access to all the game resources defined in AlienInvasion   
        super().__init__()
        self.screen=ai_game.screen
        self.setting=ai_game.setting
        self.screen_rect=ai_game.screen.get_rect()  #We access the screen’s rect attribute using the get_rect() method and      
        self.image=pygame.image.load('images/ship_img.bmp')
        self.rect=self.image.get_rect()#We access the screen’s rect attribute using the get_rect() method and
        self.rect.midbottom=self.screen_rect.midbottom # start each ship with bottom of screen 
        self.x = float(self.rect.x)    # Store a float for the ship's exact horizontal position.
        self.y = float(self.rect.y)    # Store a float for the ship's exact vertical position.
        self.moving_right=False # for continuous movement right
        self.moving_left=False # for continuous movement left
        self.moving_up=False # for continuous movement right
        self.moving_down=False # for continuous movement left
        
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image,self.rect) #blit is a method provided by Pygame's Surface class, which is used to draw one surface onto another
    
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right: # so ship don't go outside edge
            self.x+=self.setting.ship_speed
        if self.moving_left and self.rect.left>0:                        ## so ship don't go outside edge
            self.x-=self.setting.ship_speed
        if self.moving_up and self.rect.top >= self.screen_rect.top:
            self.y-=self.setting.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y+=self.setting.ship_speed  
        self.rect.x=self.x
        self.rect.y=self.y
        
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.y = float(self.rect.y)
            
        
        