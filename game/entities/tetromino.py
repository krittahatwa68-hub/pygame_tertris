"""
Tetromino Pieces Implementation
Demonstrates: Inheritance, Polymorphism, Encapsulation
SOLID: Open/Closed Principle, Liskov Substitution Principle
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from config.config import TETROMINO_COLORS


class Tetromino(ABC):
    """
    Abstract Base Class for all Tetromino pieces
    Encapsulation: Private attributes with property decorators
    Open/Closed Principle: Open for extension, closed for modification
    """
    
    def __init__(self, x: int, y: int):
        """
        Initialize Tetromino at given position
        
        Args:
            x: Starting column position
            y: Starting row position
        """
        self._x = x
        self._y = y
        self._rotation = 0
        self._blocks = self._define_blocks()
    
    @property
    def x(self) -> int:
        """Get x position"""
        return self._x
    
    @property
    def y(self) -> int:
        """Get y position"""
        return self._y
    
    @property
    def rotation(self) -> int:
        """Get current rotation state"""
        return self._rotation
    
    @property
    def piece_type(self) -> str:
        """Get piece type (I, O, T, S, Z, J, L)"""
        return self.__class__.__name__[0]
    
    @property
    def shape(self) -> List[List[Tuple[int, int]]]:
        """Get all rotation shapes for this piece"""
        return self._blocks
    
    def move(self, dx: int, dy: int) -> None:
        """Move piece by delta"""
        self._x += dx
        self._y += dy
    
    def set_position(self, x: int, y: int) -> None:
        """Set absolute position"""
        self._x = x
        self._y = y
    
    def rotate(self) -> None:
        """Rotate piece - Polymorphism: each piece has own rotation logic"""
        self._rotation = (self._rotation + 1) % len(self._blocks)
    
    @abstractmethod
    def _define_blocks(self) -> List[List[Tuple[int, int]]]:
        """
        Define all rotation states for this piece
        Abstract method: must be implemented by subclasses
        
        Returns:
            List of rotation states, each containing block positions
        """
        pass
    
    def get_blocks(self) -> List[Tuple[int, int]]:
        """
        Get current block positions (Polymorphism)
        
        Returns:
            List of (relative_x, relative_y) for each block
        """
        return [(self._x + bx, self._y + by) 
                for bx, by in self._blocks[self._rotation]]
    
    @abstractmethod
    def get_color(self) -> Tuple[int, int, int]:
        """Get piece color"""
        pass


class IPiece(Tetromino):
    """I-Tetromino (Cyan) - Inheritance from Tetromino"""
    
    def _define_blocks(self) -> List[List[Tuple[int, int]]]:
        """Define I-piece rotations"""
        return [
            [(0, 0), (1, 0), (2, 0), (3, 0)],  # Horizontal
            [(0, 0), (0, 1), (0, 2), (0, 3)],  # Vertical
            [(0, 0), (1, 0), (2, 0), (3, 0)],  # Horizontal
            [(0, 0), (0, 1), (0, 2), (0, 3)],  # Vertical
        ]
    
    def get_color(self) -> Tuple[int, int, int]:
        return TETROMINO_COLORS['I']


class OPiece(Tetromino):
    """O-Tetromino (Yellow) - Inheritance from Tetromino"""
    
    def _define_blocks(self) -> List[List[Tuple[int, int]]]:
        """Define O-piece rotations (same in all rotations)"""
        rotation = [(0, 0), (1, 0), (0, 1), (1, 1)]
        return [rotation] * 4
    
    def get_color(self) -> Tuple[int, int, int]:
        return TETROMINO_COLORS['O']


class TPiece(Tetromino):
    """T-Tetromino (Magenta) - Inheritance from Tetromino"""
    
    def _define_blocks(self) -> List[List[Tuple[int, int]]]:
        """Define T-piece rotations"""
        return [
            [(0, 0), (1, 0), (2, 0), (1, 1)],  # Up
            [(0, 0), (0, 1), (1, 1), (0, 2)],  # Right
            [(1, 0), (0, 1), (1, 1), (2, 1)],  # Down
            [(1, 0), (0, 1), (1, 1), (1, 2)],  # Left
        ]
    
    def get_color(self) -> Tuple[int, int, int]:
        return TETROMINO_COLORS['T']


class SPiece(Tetromino):
    """S-Tetromino (Green) - Inheritance from Tetromino"""
    
    def _define_blocks(self) -> List[List[Tuple[int, int]]]:
        """Define S-piece rotations"""
        return [
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
        ]
    
    def get_color(self) -> Tuple[int, int, int]:
        return TETROMINO_COLORS['S']


class ZPiece(Tetromino):
    """Z-Tetromino (Red) - Inheritance from Tetromino"""
    
    def _define_blocks(self) -> List[List[Tuple[int, int]]]:
        """Define Z-piece rotations"""
        return [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
        ]
    
    def get_color(self) -> Tuple[int, int, int]:
        return TETROMINO_COLORS['Z']


class JPiece(Tetromino):
    """J-Tetromino (Blue) - Inheritance from Tetromino"""
    
    def _define_blocks(self) -> List[List[Tuple[int, int]]]:
        """Define J-piece rotations"""
        return [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 0), (1, 0), (0, 1), (0, 2)],
            [(0, 0), (1, 0), (2, 0), (2, 1)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ]
    
    def get_color(self) -> Tuple[int, int, int]:
        return TETROMINO_COLORS['J']


class LPiece(Tetromino):
    """L-Tetromino (Orange) - Inheritance from Tetromino"""
    
    def _define_blocks(self) -> List[List[Tuple[int, int]]]:
        """Define L-piece rotations"""
        return [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 0), (0, 1), (1, 1), (0, 2)],
            [(0, 0), (1, 0), (2, 0), (0, 1)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ]
    
    def get_color(self) -> Tuple[int, int, int]:
        return TETROMINO_COLORS['L']


class PieceFactory:
    """
    Factory Pattern: Dependency Inversion Principle
    Creates Tetromino instances
    """
    
    _pieces = {
        'I': IPiece,
        'O': OPiece,
        'T': TPiece,
        'S': SPiece,
        'Z': ZPiece,
        'J': JPiece,
        'L': LPiece,
    }
    
    @staticmethod
    def create_piece(piece_type: str, x: int, y: int) -> Tetromino:
        """
        Create a piece of given type
        
        Args:
            piece_type: Type of piece ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
            x: Starting x position
            y: Starting y position
            
        Returns:
            Tetromino instance
        """
        if piece_type not in PieceFactory._pieces:
            raise ValueError(f"Unknown piece type: {piece_type}")
        
        piece_class = PieceFactory._pieces[piece_type]
        return piece_class(x, y)
    
    @staticmethod
    def get_random_piece(x: int, y: int) -> Tetromino:
        """Create a random Tetromino"""
        import random
        piece_type = random.choice(list(PieceFactory._pieces.keys()))
        return PieceFactory.create_piece(piece_type, x, y)
