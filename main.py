import sys
import pygame
from Settings import Settings
from ship import Ship
from bullet import Bullet 
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from scoreboard import Scoreboard
from sound_track import Sound_Track
import threading

class Alien_Invasion:
    def __init__(self):
        pygame.init()
        self.setting=Settings()
        self.screen=pygame.display.set_mode((self.setting.screen_width,self.setting.screen_height)) #window size
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)       #  For full window size but in full screen there is no default quit
        pygame.display.set_caption("Alien Invasion")
        self.clock=pygame.time.Clock() #created a clock
        self.ship=Ship(self) #self is passed automatically Ship(self)
        self.stats = GameStats(self)
        self.score=Scoreboard(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        self.game_active = False
        # Make the Play button.
        self.play_button = Button(self, "Play")
        self.sound=Sound_Track(self)
        self.music_play=False
        
   
    def run_game(self):     
        """Start the main loop for the game."""
        while True:
            self.check_event()
            if self.game_active:
                self.ship.update()
                self._update_bullet()    
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
            
    def _Thread(self):
        self.music_thread = threading.Thread(target=self.sound.play_background_music)
        self.music_thread.daemon = True  # Allow the thread to exit when the main program exits
        self.music_thread.start()
    
    
    def check_event(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN: # if mose button is pressed
                    mouse_pos=pygame.mouse.get_pos() # check postio of mouse
                    self._check_play_button(mouse_pos)  
                elif event.type==pygame.KEYDOWN:# if any key from keyboard is press
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP: #if any key from keyboard is released
                    self._check_keyup_events(event)
                                
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.setting.bg_color) # filled screen with bgcolor
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)  #Pygame's draw module, which provides various drawing functions to draw shapes, lines, and other primitives directly onto a surface.
        self.score.show_score()
        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()  # to filp with first buffer with second buffer 
        
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
         self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up=True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down=True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key== pygame.K_SPACE:
            self._fire_bullet()
        
            
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up=False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down=False
            
    def _fire_bullet(self):
        "Create new bullets and group them together"
        if len(self.bullets)<self.setting.bullet_allowed:
            new_bullets=Bullet(self) 
            self.bullets.add(new_bullets) # adding all bullets objects and grouping them together like list of obj
            self.sound.bullet_sound.play()
            
    def _update_bullet(self):
        self.bullets.update()
            # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
             
    def _check_bullet_alien_collisions(self):
         # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collision=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collision:
            
            for aliens in collision.values():
                self.stats.score+=self.setting.alien_points*len(aliens)
                self.sound.sound_blast.play()
            
            self.score.prep_score()
            self.score.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
             self.bullets.empty()
             self._create_fleet()
             self.setting.increase_speed()
             # Increase level.
             self.stats.level += 1
             self.score.prep_level()
                        
        
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien
        new_alien=Alien(self)
        alien_width, alien_height = new_alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.setting.screen_height - 8* alien_height):
            while current_x < (self.setting.screen_width -  alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2*alien_width
            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
            
    def _create_alien(self, x_position,y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
        
    def  _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1
        
    def _ship_hit(self):
        if self.stats.ships_left>1:
            self.stats.ships_left-=1
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self.ship.center_ship()
            self._create_fleet()
            self.score.prep_ships()
            self.sound.ship_wreck.play()
            # Pause.
            sleep(0.5)
        else:
            self.game_active=False
            self.music_play=False
            #self.sound.background_music()
            # Hide the mouse cursor.
            pygame.mouse.set_visible(True)

    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.setting.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
            
    def _check_play_button(self,mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics.
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)# set mouse curson invisible after play is clicked
            self.stats.reset_stats()
            self.score.prep_score()
            self.score.prep_level()
            self.score.prep_ships()
            self.game_active = True
            self.music_play=True
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            self.setting.initialize_dynamic_settings()
           #self._Thread()
            

        
        
                 
if __name__ == '__main__':  # condition mean run when file is directly run not when module is imported
 # Make a game instance, and run the game.
    ai = Alien_Invasion()
    ai.run_game()
    
"""In Pygame, the origin (0, 0) is at the top-left corner of the screen, and coordinates 
increase as you go down and to the right. On a 1200×800 screen, the origin is at the 
top-left corner, and the bottom-right corner has the coordinates (1200, 800). These 
coordinates refer to the game window, not the physical screen."""
    
    