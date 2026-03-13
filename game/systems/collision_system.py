"""
Collision System
Advanced collision detection and validation
"""

from typing import List, Tuple
from config.config import COLOR_BLACK, BOARD_WIDTH, BOARD_HEIGHT


class CollisionSystem:
    """
    Handles all collision detection for pieces
    Checks boundaries, locked pieces, and movement validity
    """
    
    @staticmethod
    def check_collision(piece, board, dx: int = 0, dy: int = 0) -> bool:
        """
        Check if piece would collide at new position
        
        Args:
            piece: Tetromino piece to check
            board: Game board
            dx: Delta X movement
            dy: Delta Y movement
            
        Returns:
            True if collision detected, False otherwise
        """
        # Save original position
        orig_x, orig_y = piece.x, piece.y
        
        # Move piece to test position
        piece.move(dx, dy)
        
        # Check collision
        collision = False
        for x, y in piece.get_blocks():
            # Check boundaries
            if x < 0 or x >= BOARD_WIDTH:
                collision = True
                break
            
            # Check bottom boundary
            if y >= BOARD_HEIGHT:
                collision = True
                break
            
            # Check collision with locked pieces (allow negative Y for spawn area)
            if y >= 0 and board.get_cell(x, y) != COLOR_BLACK:
                collision = True
                break
        
        # Restore original position
        piece.set_position(orig_x, orig_y)
        
        return collision
    
    @staticmethod
    def get_landing_position(piece, board) -> int:
        """
        Get Y position where piece will land
        
        Args:
            piece: Tetromino piece
            board: Game board
            
        Returns:
            Y position where piece will land
        """
        test_y = piece.y
        max_attempts = BOARD_HEIGHT + 10
        attempts = 0
        
        while attempts < max_attempts:
            if CollisionSystem.check_collision(piece, board, 0, 1):
                break
            test_y += 1
            attempts += 1
        
        return test_y
    
    @staticmethod
    def get_ghost_piece_blocks(piece, board) -> List[Tuple[int, int]]:
        """
        Get blocks for ghost piece preview
        
        Args:
            piece: Current falling piece
            board: Game board
            
        Returns:
            List of (x, y) coordinates for ghost piece
        """
        landing_y = CollisionSystem.get_landing_position(piece, board)
        dy = landing_y - piece.y
        
        # Get blocks at landing position
        ghost_blocks = []
        for x, y in piece.get_blocks():
            ghost_blocks.append((x, y + dy))
        
        return ghost_blocks
    
    @staticmethod
    def is_valid_position(piece, board) -> bool:
        """
        Check if piece is in valid position on board
        
        Args:
            piece: Tetromino piece
            board: Game board
            
        Returns:
            True if position is valid, False otherwise
        """
        is_valid = True
        for x, y in piece.get_blocks():
            # Negative Y is allowed (spawn area above board)
            if y < 0:
                continue
            
            # Check boundaries
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                is_valid = False
                break
            
            # Check collision with locked pieces
            if board.get_cell(x, y) != COLOR_BLACK:
                is_valid = False
                break
        
        return is_valid
    
    @staticmethod
    def can_move_down(piece, board) -> bool:
        """Check if piece can move down"""
        return not CollisionSystem.check_collision(piece, board, 0, 1)
    
    @staticmethod
    def can_move_left(piece, board) -> bool:
        """Check if piece can move left"""
        return not CollisionSystem.check_collision(piece, board, -1, 0)
    
    @staticmethod
    def can_move_right(piece, board) -> bool:
        """Check if piece can move right"""
        return not CollisionSystem.check_collision(piece, board, 1, 0)
