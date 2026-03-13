"""
7-Bag Randomizer System
Ensures all 7 piece types appear before repeating
Follows Tetris Guideline standards
"""

import random
from typing import List
from game.entities.tetromino import PieceFactory


class PieceBag:
    """
    7-Bag Randomizer
    Maintains a bag of all 7 piece types and ensures even distribution
    """
    
    PIECE_TYPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
    
    def __init__(self):
        """Initialize piece bag"""
        self._current_bag: List[str] = []
        self._next_bag: List[str] = []
        self._refill_bag()
    
    def _refill_bag(self) -> None:
        """Refill bag with all 7 pieces and shuffle"""
        self._current_bag = self.PIECE_TYPES.copy()
        random.shuffle(self._current_bag)
    
    def get_next_piece(self, start_x: int, start_y: int):
        """
        Get next piece from bag
        
        Args:
            start_x: Starting X position
            start_y: Starting Y position
            
        Returns:
            Next Tetromino piece
        """
        if not self._current_bag:
            self._refill_bag()
        
        piece_type = self._current_bag.pop(0)
        return PieceFactory.create_piece(piece_type, start_x, start_y)
    
    def peek_next_piece(self, start_x: int = 0, start_y: int = 0):
        """
        Peek at next piece without removing from bag
        
        Args:
            start_x: Starting X position for preview
            start_y: Starting Y position for preview
            
        Returns:
            Preview of next Tetromino piece
        """
        if not self._current_bag:
            temp_bag = self.PIECE_TYPES.copy()
            random.shuffle(temp_bag)
            piece_type = temp_bag[0]
        else:
            piece_type = self._current_bag[0]
        
        return PieceFactory.create_piece(piece_type, start_x, start_y)
    
    def get_bag_status(self) -> str:
        """Get current bag status for debugging"""
        return f"Bag: {len(self._current_bag)} pieces remaining"
