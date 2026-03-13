"""
Super Rotation System (SRS) with Wall Kick
Implements Tetris Guideline standard rotation
"""

from typing import List, Tuple


class WallKickSystem:
    """
    Super Rotation System (SRS) with wall kick support
    Allows pieces to "kick" off walls when rotating
    """
    
    # Wall kick data for I-piece (different offsets)
    I_WALL_KICK_DATA = [
        # 0->1, 1->2, 2->3, 3->0
        [(0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)],    # 0->1
        [(0, 0), (2, 0), (-1, 0), (2, 0), (-1, 0)],    # 1->2
        [(0, 0), (1, 0), (-2, 0), (1, 0), (-2, 0)],    # 2->3
        [(0, 0), (-2, 0), (1, 0), (-2, 0), (1, 0)],    # 3->0
    ]
    
    # Wall kick data for other pieces (standard JLSTZ)
    STANDARD_WALL_KICK_DATA = [
        # 0->1, 1->2, 2->3, 3->0
        [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],    # 0->1
        [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],        # 1->2
        [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],       # 2->3
        [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],     # 3->0
    ]
    
    @staticmethod
    def get_wall_kick_data(piece_type: str, from_rotation: int) -> List[Tuple[int, int]]:
        """
        Get wall kick offset data for piece rotation
        
        Args:
            piece_type: Type of piece ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
            from_rotation: Current rotation state (0-3)
            
        Returns:
            List of (dx, dy) offset tuples to test
        """
        if piece_type == 'I':
            return WallKickSystem.I_WALL_KICK_DATA[from_rotation % 4]
        elif piece_type == 'O':
            # O-piece never wall kicks
            return [(0, 0)]
        else:
            # T, S, Z, J, L all use standard wall kick
            return WallKickSystem.STANDARD_WALL_KICK_DATA[from_rotation % 4]
    
    @staticmethod
    def try_rotate_with_kick(piece, board, collision_checker) -> bool:
        """
        Try to rotate piece with wall kick support
        
        Args:
            piece: Tetromino piece to rotate
            board: Game board
            collision_checker: Collision system to use
            
        Returns:
            True if rotation succeeded, False otherwise
        """
        if piece.__class__.__name__ == 'OPiece':
            # O-piece cannot rotate
            return False
        
        # Get current rotation
        current_rotation = piece.rotation
        
        # Rotate piece
        piece.rotate()
        
        # Get piece type for wall kick data
        piece_type = piece.__class__.__name__[0]  # 'I', 'O', 'T', etc.
        
        # Get wall kick offsets to test
        kick_offsets = WallKickSystem.get_wall_kick_data(piece_type, current_rotation)
        
        # Test each offset
        for offset_x, offset_y in kick_offsets:
            # Test this offset
            test_x = piece.x + offset_x
            test_y = piece.y + offset_y
            
            # Save current position
            orig_x, orig_y = piece.x, piece.y
            piece.set_position(test_x, test_y)
            
            # Check if this position is valid
            if collision_checker.is_valid_position(piece, board):
                # Success! Keep this position
                return True
            
            # Restore position and try next offset
            piece.set_position(orig_x, orig_y)
        
        # No valid rotation found, revert rotation
        piece.rotate()
        piece.rotate()
        piece.rotate()
        return False
    
    @staticmethod
    def rotate_clockwise(piece, board, collision_checker) -> bool:
        """
        Rotate piece clockwise with wall kick
        
        Args:
            piece: Tetromino piece
            board: Game board
            collision_checker: Collision system
            
        Returns:
            True if rotation succeeded, False otherwise
        """
        return WallKickSystem.try_rotate_with_kick(piece, board, collision_checker)
    
    @staticmethod
    def rotate_counterclockwise(piece, board, collision_checker) -> bool:
        """
        Rotate piece counter-clockwise with wall kick
        
        Args:
            piece: Tetromino piece
            board: Game board
            collision_checker: Collision system
            
        Returns:
            True if rotation succeeded, False otherwise
        """
        # Rotate 3 times clockwise = 1 time counter-clockwise
        piece.rotate()
        piece.rotate()
        piece.rotate()
        
        # Now try wall kick
        current_rotation = (piece.rotation - 1) % 4
        piece_type = piece.__class__.__name__[0]
        kick_offsets = WallKickSystem.get_wall_kick_data(piece_type, current_rotation)
        
        # Test each offset
        for offset_x, offset_y in kick_offsets:
            orig_x, orig_y = piece.x, piece.y
            piece.set_position(orig_x + offset_x, orig_y + offset_y)
            
            if collision_checker.is_valid_position(piece, board):
                return True
            
            piece.set_position(orig_x, orig_y)
        
        # Revert rotation
        piece.rotate()
        return False
