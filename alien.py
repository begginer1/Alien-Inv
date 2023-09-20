import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.setting
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien_img.bmp')
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width/2.0
        self.rect.y = self.rect.height/2.0
        resized_image = pygame.transform.scale(self.image, (self.rect.x, self.rect.y)) # decrease size of alienship
        self.image=resized_image
        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
            