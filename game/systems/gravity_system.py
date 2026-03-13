"""
Gravity System
Manages piece falling speed based on game progress
"""


class GravitySystem:
    """
    Manages gravity and piece falling speed
    Uses adjustable gravity based on level/lines cleared
    """
    
    # Gravity values (cells per frame) at different levels
    # Lower values = faster gravity
    GRAVITY_LEVELS = {
        0: 0.016667,   # Level 0: ~1 cell per 60 frames (1/60)
        1: 0.02,       # Level 1
        5: 0.035,      # Level 5
        10: 0.05,      # Level 10
        15: 0.065,     # Level 15
        20: 0.1,       # Level 20
        30: 0.15,      # Level 30+
    }
    
    # Lock delay: frames to wait before locking piece after bottom contact
    LOCK_DELAY = 30  # ~0.5 seconds at 60 FPS
    
    def __init__(self, difficulty: float = 0.7):
        """
        Initialize gravity system
        
        Args:
            difficulty: 0.4 (hard), 0.7 (normal), 1.0 (easy)
        """
        self._difficulty = difficulty
        self._level = 0
        self._lines_cleared = 0
        self._gravity = self._calculate_gravity()
        self._fall_accumulator = 0.0
        self._lock_delay = 0
        self._on_ground = False
    
    def _calculate_gravity(self) -> float:
        """
        Calculate gravity based on level
        
        Returns:
            Gravity value (cells per frame)
        """
        # Get appropriate gravity level
        for level_threshold in sorted(self.GRAVITY_LEVELS.keys(), reverse=True):
            if self._level >= level_threshold:
                base_gravity = self.GRAVITY_LEVELS[level_threshold]
                break
        else:
            base_gravity = self.GRAVITY_LEVELS[0]
        
        # Apply difficulty multiplier
        return base_gravity * self._difficulty
    
    def update(self, delta_time: float) -> int:
        """
        Update gravity and return cells to move down
        
        Args:
            delta_time: Time elapsed since last frame (seconds)
            
        Returns:
            Number of cells to move piece down
        """
        self._fall_accumulator += delta_time * self._gravity * 60  # Convert to cells
        
        cells_to_move = int(self._fall_accumulator)
        self._fall_accumulator -= cells_to_move
        
        return cells_to_move
    
    def on_piece_lock(self) -> None:
        """Called when a piece is locked"""
        self._lock_delay = 0
        self._on_ground = False
    
    def on_ground_contact(self) -> None:
        """Called when piece touches ground"""
        self._on_ground = True
    
    def add_lines(self, lines_cleared: int) -> None:
        """
        Add cleared lines and update level
        
        Args:
            lines_cleared: Number of lines cleared
        """
        self._lines_cleared += lines_cleared
        self._level = self._lines_cleared // 10
        self._gravity = self._calculate_gravity()
    
    def get_level(self) -> int:
        """Get current level (0-based)"""
        return self._level
    
    def get_lines(self) -> int:
        """Get total lines cleared"""
        return self._lines_cleared
    
    def get_gravity(self) -> float:
        """Get current gravity value"""
        return self._gravity
    
    def reset(self) -> None:
        """Reset gravity system"""
        self._level = 0
        self._lines_cleared = 0
        self._gravity = self._calculate_gravity()
        self._fall_accumulator = 0.0
        self._lock_delay = 0
        self._on_ground = False
