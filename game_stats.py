class GameStats:
    def __init__(self,ai_game):
        """Initialize statistics."""
        self.setting=ai_game.setting
        self.high_score = 0
        self.reset_stats()
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left =self.setting.ship_limit
        self.score=0
        self.level = 1
        