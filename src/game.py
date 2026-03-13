"""
Main Game Controller
Demonstrates: Composition, Dependency Injection, Orchestration
SOLID: Single Responsibility (coordination), Dependency Inversion
"""

import random
from src.board import Board
from src.pieces import Tetromino, PieceFactory
from src.renderer import Renderer
from src.input_handler import InputHandler, InputAction
from src.sound_manager import SoundManager
from src.score_manager import ScoreManager
from src.config import (
    BOARD_WIDTH, GAME_MENU, GAME_RUNNING, GAME_PAUSED, GAME_OVER, FPS,
    DIFFICULTY_NORMAL
)


class Game:
    """
    Main game controller
    Composition: Contains Board, Renderer, InputHandler, Pieces
    Dependency Injection: All dependencies injected
    Single Responsibility: Orchestrate game logic
    """
    
    def __init__(self, difficulty: float = DIFFICULTY_NORMAL):
        """
        Initialize game
        
        Args:
            difficulty: Game difficulty multiplier (0.0-1.0, lower = faster)
        """
        # Composition: Inject dependencies
        self._board = Board()
        self._renderer = Renderer()
        self._input_handler = InputHandler()
        self._sound_manager = SoundManager()
        self._score_manager = ScoreManager()
        
        # Game state
        self._state = GAME_MENU
        self._score = 0
        self._lines_cleared = 0
        self._difficulty = difficulty
        
        # Current piece
        self._current_piece: Tetromino = None
        self._fall_time = 0
        self._fall_speed = int(1000 * difficulty)  # milliseconds
        
        self._initialize_game()
    
    def _initialize_game(self) -> None:
        """Initialize game state"""
        self._renderer.init()
        self._sound_manager.init()
    
    def _spawn_new_piece(self) -> None:
        """Spawn new piece at top of board"""
        spawn_x = BOARD_WIDTH // 2 - 1
        spawn_y = 0
        self._current_piece = PieceFactory.get_random_piece(spawn_x, spawn_y)
    
    def _handle_input(self) -> bool:
        """
        Handle user input
        
        Returns:
            True if game should continue, False if should quit
        """
        action = self._input_handler.handle_events()
        
        if action == InputAction.QUIT:
            return False
        
        # Handle menu state
        if self._state == GAME_MENU:
            if action == InputAction.CLICK:
                result = self._renderer.handle_menu_click(self._input_handler.get_mouse_pos())
                if result == 'start':
                    self._start_game()
                    self._sound_manager.play_menu_select()
                elif result == 'exit':
                    return False
            return True
        
        # Handle game over state
        if self._state == GAME_OVER:
            if action == InputAction.CLICK:
                result = self._renderer.handle_game_over_click(self._input_handler.get_mouse_pos())
                if result == 'menu':
                    self._state = GAME_MENU
                    self._sound_manager.play_menu_select()
                elif result == 'exit':
                    return False
            return True
        
        if action == InputAction.PAUSE:
            self._state = GAME_PAUSED if self._state == GAME_RUNNING else GAME_RUNNING
        
        if self._state != GAME_RUNNING:
            return True
        
        # Handle movement actions
        if action == InputAction.MOVE_LEFT:
            self._move_piece(-1, 0)
        elif action == InputAction.MOVE_RIGHT:
            self._move_piece(1, 0)
        elif action == InputAction.MOVE_DOWN:
            self._move_piece(0, 1)
        elif action == InputAction.ROTATE:
            self._rotate_piece()
            self._sound_manager.play_rotate()
        elif action == InputAction.DROP:
            self._drop_piece()
            self._sound_manager.play_drop()
        
        return True
    
    def _start_game(self) -> None:
        """Start a new game"""
        self._board = Board()
        self._score = 0
        self._lines_cleared = 0
        self._fall_time = 0
        self._state = GAME_RUNNING
        self._spawn_new_piece()
    
    def _move_piece(self, dx: int, dy: int) -> None:
        """
        Move current piece
        
        Args:
            dx: Delta x
            dy: Delta y
        """
        self._current_piece.move(dx, dy)
        
        # Check if move is valid
        if not self._board.is_valid_position(self._current_piece):
            # Revert move
            self._current_piece.move(-dx, -dy)
            
            # If moving down and invalid, lock piece
            if dy > 0:
                self._lock_and_spawn()
    
    def _rotate_piece(self) -> None:
        """Rotate current piece"""
        self._current_piece.rotate()
        
        # Check if rotation is valid
        if not self._board.is_valid_position(self._current_piece):
            # Revert rotation
            self._current_piece.rotate()
            self._current_piece.rotate()
            self._current_piece.rotate()
    
    def _drop_piece(self) -> None:
        """Drop piece to bottom"""
        while self._board.is_valid_position(self._current_piece):
            self._current_piece.move(0, 1)
        
        self._current_piece.move(0, -1)
        self._lock_and_spawn()
    
    def _lock_and_spawn(self) -> None:
        """Lock current piece and spawn new one"""
        self._board.lock_piece(self._current_piece)
        
        # Clear completed rows
        rows_cleared = self._board.clear_rows()
        
        # Update score
        if rows_cleared > 0:
            self._lines_cleared += rows_cleared
            self._score += rows_cleared * rows_cleared * 100
            self._sound_manager.play_line_clear()
        
        # Spawn new piece
        self._spawn_new_piece()
        
        # Check game over
        if not self._board.is_valid_position(self._current_piece):
            self._state = GAME_OVER
            self._sound_manager.play_game_over()
            self._score_manager.update_high_score(self._score)
    
    def update(self) -> bool:
        """
        Update game state
        
        Returns:
            True if game should continue, False if should quit
        """
        # Handle input
        if not self._handle_input():
            return False
        
        # Update menu
        if self._state == GAME_MENU:
            self._renderer.update_menu(self._input_handler.get_mouse_pos())
            return True
        
        # Update game over
        if self._state == GAME_OVER:
            self._renderer.update_game_over(self._input_handler.get_mouse_pos())
            return True
        
        # Skip update if paused
        if self._state == GAME_PAUSED:
            return True
        
        # Auto-drop piece
        self._fall_time += 1
        if self._fall_time >= self._fall_speed:
            self._fall_time = 0
            self._move_piece(0, 1)
        
        return True
    
    def render(self) -> None:
        """Render current game state"""
        if self._state == GAME_MENU:
            self._renderer.render_menu()
        elif self._state == GAME_OVER:
            high_score = self._score_manager.get_high_score()
            self._renderer.render_game_over(self._score, self._lines_cleared, high_score)
        else:
            self._renderer.render(
                self._board,
                self._current_piece,
                self._score,
                self._lines_cleared,
                self._state
            )
    
    def run(self) -> None:
        """Main game loop"""
        clock = self._renderer.get_clock()
        running = True
        
        while running:
            running = self.update()
            self.render()
            clock.tick(FPS)
        
        self._sound_manager.quit()
        self._renderer.quit()
    
    @property
    def score(self) -> int:
        """Get current score"""
        return self._score
    
    @property
    def lines_cleared(self) -> int:
        """Get lines cleared"""
        return self._lines_cleared
    
    @property
    def game_state(self) -> int:
        """Get game state"""
        return self._state
