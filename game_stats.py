from pathlib import Path
import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialise statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset.
        self.path = Path("highscore.json")
        self.load_highscore()

    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
    
    def load_highscore(self):

        if self.path.exists():
            with self.path.open('r') as f:
                self.high_score = json.load(f)
        else:
            self.high_score = 0
    
    def save_highscore(self):
        with self.path.open('w') as f:
            json.dump(self.high_score, f)
