"""
Score Manager
Single Responsibility: Handle score tracking and persistence
Encapsulation: Load and save high scores and levels
"""

import json
import os
from typing import Optional


class ScoreManager:
    """
    Manages game scores including high score and high level persistence
    Single Responsibility: Score and level storage and retrieval
    Encapsulation: Private attributes with public interface methods
    """
    
    def __init__(self, score_file: str = "data/highscore.json"):
        """
        Initialize score manager
        
        Args:
            score_file: File path to store high score and high level
        """
        self._score_file = score_file
        # Ensure data directory exists
        os.makedirs(os.path.dirname(score_file) or '.', exist_ok=True)
        self._high_level = 0
        self._high_score = self._load_high_score()
    
    def _load_high_score(self) -> int:
        """
        Load high score and high level from file
        
        Returns:
            High score value, or 0 if file doesn't exist
        """
        try:
            if os.path.exists(self._score_file):
                with open(self._score_file, 'r') as f:
                    data = json.load(f)
                    self._high_level = data.get('high_level', 0)
                    return data.get('high_score', 0)
        except Exception:
            pass
        
        self._high_level = 0
        return 0
    
    def _save_high_score(self) -> None:
        """Save high score and high level to file"""
        try:
            data = {
                'high_score': self._high_score,
                'high_level': self._high_level
            }
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
    
    def get_high_level(self) -> int:
        """
        Get highest level achieved
        
        Returns:
            High level value
        """
        return self._high_level
    
    def update_high_score(self, score: int, level: int) -> bool:
        """
        Update high score and high level if current values are higher
        
        Args:
            score: Current game score
            level: Current game level
            
        Returns:
            True if high score or high level was updated, False otherwise
        """
        updated = False
        
        if score > self._high_score:
            self._high_score = score
            updated = True
        
        if level > self._high_level:
            self._high_level = level
            updated = True
        
        if updated:
            self._save_high_score()
        
        return updated
    
    def reset_high_score(self) -> None:
        """Reset high score and high level to 0"""
        self._high_score = 0
        self._high_level = 0
        self._save_high_score()
