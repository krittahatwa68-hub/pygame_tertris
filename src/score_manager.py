"""
Score Manager
Single Responsibility: Handle score tracking and persistence
Encapsulation: Load and save high scores
"""

import json
import os
from typing import Optional


class ScoreManager:
    """
    Manages game scores including high score persistence
    Single Responsibility: Score storage and retrieval
    """
    
    def __init__(self, score_file: str = "highscore.json"):
        """
        Initialize score manager
        
        Args:
            score_file: File path to store high score
        """
        self._score_file = score_file
        self._high_score = self._load_high_score()
    
    def _load_high_score(self) -> int:
        """
        Load high score from file
        
        Returns:
            High score value, or 0 if file doesn't exist
        """
        try:
            if os.path.exists(self._score_file):
                with open(self._score_file, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except Exception:
            pass
        
        return 0
    
    def _save_high_score(self) -> None:
        """Save high score to file"""
        try:
            data = {'high_score': self._high_score}
            with open(self._score_file, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass  # Silently ignore save errors
    
    def get_high_score(self) -> int:
        """
        Get current high score
        
        Returns:
            High score value
        """
        return self._high_score
    
    def update_high_score(self, score: int) -> bool:
        """
        Update high score if current score is higher
        
        Args:
            score: Current game score
            
        Returns:
            True if high score was updated, False otherwise
        """
        if score > self._high_score:
            self._high_score = score
            self._save_high_score()
            return True
        return False
    
    def reset_high_score(self) -> None:
        """Reset high score to 0"""
        self._high_score = 0
        self._save_high_score()
