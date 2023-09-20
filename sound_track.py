# Load a sound file
import pygame 
class Sound_Track:
    def __init__(self,ai_game):
        pygame.mixer.init()
        self.ai_game=ai_game
        self.sound_blast = pygame.mixer.Sound("sounds\mixkit-arcade-game-explosion-2759.wav")
        self.bullet_sound=pygame.mixer.Sound("sounds\\bullet_sound.wav")
        self.background_music=pygame.mixer.Sound("sounds\\background-music.mp3")
        self.ship_wreck=pygame.mixer.Sound("sounds\\ship_destroyed.wav")
        self.game_over=pygame.mixer.Sound("sounds\\game_over.wav")
        
    def play_background_music(self):
        while self.ai_game.music_play:
            self.background_music.play()
            pygame.time.delay(int(self.background_music.get_length() * 1000))  # Delay for the duration of the music


    
