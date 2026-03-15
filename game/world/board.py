"""
Game Board Implementation
Encapsulation: Private board state with public interface
Single Responsibility: Manage board state and collision detection
"""

from typing import List, Tuple, Optional
from config.config import BOARD_WIDTH, BOARD_HEIGHT, COLOR_BLACK
from game.entities.tetromino import Tetromino


class Board:
    """
    Game board for Tetris
    Encapsulation: Private board state (_grid)
    Single Responsibility: Board state management and collision detection
    """
    
    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):
        """
        Initialize game board
        
        Args:
            width: Board width in cells
            height: Board height in cells
        """
        self._width = width
        self._height = height
        self.__grid: List[List[Tuple[int, int, int]]] = [
            [COLOR_BLACK for _ in range(width)] for _ in range(height)
        ]
    
    @property
    def width(self) -> int:
        """Get board width"""
        return self._width
    
    @property
    def height(self) -> int:
        """Get board height"""
        return self._height
    
    def is_valid_position(self, piece: Tetromino) -> bool:
        """
        Check if piece is in valid position
        
        Args:
            piece: Tetromino to check
            
        Returns:
            True if position is valid, False otherwise
        """
        for x, y in piece.get_blocks():
            if x < 0 or x >= self._width or y < 0 or y >= self._height:
                return False
            if y >= 0 and self.__grid[y][x] != COLOR_BLACK:
                return False
        return True
    
    def lock_piece(self, piece: Tetromino) -> None:
        """
        Lock piece in place on board
        
        Args:
            piece: Tetromino to lock
        """
        color = piece.get_color()
        for x, y in piece.get_blocks():
            if 0 <= x < self._width and 0 <= y < self._height:
                self.__grid[y][x] = color
    
    def get_cell(self, x: int, y: int) -> Tuple[int, int, int]:
        """Get color of cell at position"""
        if 0 <= x < self._width and 0 <= y < self._height:
            return self.__grid[y][x]
        return COLOR_BLACK
    
    def clear_rows(self) -> int:
        """
        Clear completed rows
        
        Returns:
            Number of rows cleared
        """
        rows_cleared = 0
        y = self._height - 1
        
        while y >= 0:
            if all(cell != COLOR_BLACK for cell in self.__grid[y]):
                # Remove completed row
                self.__grid.pop(y)
                # Add empty row at top
                self.__grid.insert(0, [COLOR_BLACK for _ in range(self._width)])
                rows_cleared += 1
            else:
                y -= 1
        
        return rows_cleared
    
    def get_grid(self) -> List[List[Tuple[int, int, int]]]:
        """Get board grid (for rendering)"""
        return self.__grid
    
    def reset(self) -> None:
        """Reset board to empty state"""
        self.__grid = [
            [COLOR_BLACK for _ in range(self._width)] 
            for _ in range(self._height)
        ]
    
    def is_game_over(self) -> bool:
        """
        Check if game is over (pieces reach top)
        
        Returns:
            True if any cells in top row are filled
        """
        return any(cell != COLOR_BLACK for cell in self._grid[0])
