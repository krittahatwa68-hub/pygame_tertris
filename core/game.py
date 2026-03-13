"""
Game Controller
Coordinates all game systems
"""

import pygame
from core.state_machine import StateMachine
from game.world.board import Board
from game.entities.piece_randomizer import PieceBag
from game.systems.scoring_system import ScoreManager
from game.systems.gravity_system import GravitySystem
from game.systems.collision_system import CollisionSystem
from game.systems.wall_kick_system import WallKickSystem
from rendering.renderer import Renderer
from input.input_handler import InputHandler, InputAction
from audio.sound_manager import SoundManager

from config.config import (
    GAME_MENU,
    GAME_RUNNING,
    GAME_PAUSED,
    GAME_OVER,
    FPS,
    BOARD_WIDTH,
    BOARD_HEIGHT,
    DIFFICULTY_NORMAL,
    LOCK_DELAY_MS,
    MAX_LOCK_RESETS
)


class Game:

    def __init__(self, renderer: Renderer, input_handler: InputHandler, difficulty: float = DIFFICULTY_NORMAL):

        self._renderer = renderer
        self._input = input_handler
        self._difficulty = difficulty

        self._state_machine = StateMachine(GAME_MENU)

        self._board = Board()
        self._scoring = ScoreManager()
        self._sound_manager = SoundManager()
        self._gravity = GravitySystem(difficulty)
        self._piece_bag = PieceBag()

        self._current_piece = None
        self._next_piece = None
        self._held_piece = None
        self._ghost_piece = None
        self._score = 0
        self._lines = 0
        self._can_hold = True
        self._can_rotate = True
        
        # Lock Delay
        self._lock_timer = 0.0
        self._lock_resets = 0

    def start_game(self):
        """Start a new game"""
        self._board.reset()
        self._score = 0
        self._lines = 0
        self._held_piece = None
        self._can_hold = True
        self._gravity.reset()
        self._piece_bag = PieceBag()
        self._lock_timer = 0.0
        self._lock_resets = 0
        
        # Initialize sound on first game start
        if not self._sound_manager._initialized:
            self._sound_manager.init()
        
        self._current_piece = self._piece_bag.get_next_piece(BOARD_WIDTH // 2 - 1, 0)
        self._next_piece = self._piece_bag.get_next_piece(BOARD_WIDTH // 2 - 1, 0)
        self._update_ghost_piece()
        self._state_machine.change_state(GAME_RUNNING)

    def update(self, delta_time: float) -> bool:
        """
        Update game state
        
        Args:
            delta_time: Time elapsed since last frame
            
        Returns:
            False if game should quit, True otherwise
        """
        action = self._input.handle_events()

        if action == InputAction.QUIT:
            return False

        state = self._state_machine.get_state()

        if state == GAME_MENU:
            if not self.update_menu(action):
                return False

        elif state == GAME_RUNNING:
            self.update_gameplay(action, delta_time)

        elif state == GAME_PAUSED:
            if not self.update_paused(action):
                return False

        elif state == GAME_OVER:
            if not self.update_game_over(action):
                return False

        return True

    def update_menu(self, action: InputAction) -> bool:
        """Update menu state. Returns False if user wants to quit."""
        mouse_pos = self._input.get_mouse_pos()
        self._renderer.update_menu(mouse_pos)
        
        if action == InputAction.CLICK:
            result = self._renderer.handle_menu_click(mouse_pos)
            if result == 'start':
                self.start_game()
            elif result == 'exit':
                return False  # Signal to quit
        
        return True  # Continue game

    def update_paused(self, action: InputAction) -> bool:
        """Update paused state. Returns False if user wants to quit."""
        mouse_pos = self._input.get_mouse_pos()
        self._renderer.update_pause(mouse_pos)
        
        # Can still unpause with P key
        if action == InputAction.PAUSE:
            self._state_machine.change_state(GAME_RUNNING)
            return True
            
        if action == InputAction.CLICK:
            result = self._renderer.handle_pause_click(mouse_pos)
            if result == 'resume':
                self._state_machine.change_state(GAME_RUNNING)
            elif result == 'restart':
                self.start_game()
            elif result == 'menu':
                self._state_machine.change_state(GAME_MENU)
            elif result == 'exit':
                return False  # Signal to quit loop
        
        return True

    def update_game_over(self, action: InputAction) -> bool:
        """Update game over state. Returns False if user wants to quit."""
        mouse_pos = self._input.get_mouse_pos()
        self._renderer.update_game_over(mouse_pos)
        
        if action == InputAction.RESTART:
            self.start_game()
        elif action == InputAction.CLICK:
            result = self._renderer.handle_game_over_click(mouse_pos)
            if result == 'menu':
                self._state_machine.change_state(GAME_MENU)
            elif result == 'exit':
                return False  # Signal to quit
        
        return True  # Continue game

    def update_gameplay(self, action: InputAction, delta_time: float) -> None:
        """Update gameplay state"""
        if action == InputAction.PAUSE:
            self._state_machine.change_state(GAME_PAUSED)
            return

        # Handle piece movement with collision detection
        if action == InputAction.MOVE_LEFT:
            if CollisionSystem.can_move_left(self._current_piece, self._board):
                self._current_piece.move(-1, 0)
                self._sound_manager.play_beep()
                self._update_ghost_piece()
                self._reset_lock_delay()

        elif action == InputAction.MOVE_RIGHT:
            if CollisionSystem.can_move_right(self._current_piece, self._board):
                self._current_piece.move(1, 0)
                self._sound_manager.play_beep()
                self._update_ghost_piece()
                self._reset_lock_delay()

        elif action == InputAction.MOVE_DOWN:
            if CollisionSystem.can_move_down(self._current_piece, self._board):
                self._current_piece.move(0, 1)
                self._sound_manager.play_beep()
            # Do NOT lock piece immediately here, let the tick loop handle it

        elif action == InputAction.ROTATE:
            # Try rotation with wall kick
            if WallKickSystem.rotate_clockwise(self._current_piece, self._board, CollisionSystem):
                self._sound_manager.play_rotate()
                self._update_ghost_piece()
                self._reset_lock_delay()

        elif action == InputAction.ROTATE_CCW:
            # Try counter-clockwise rotation with wall kick
            if WallKickSystem.rotate_counterclockwise(self._current_piece, self._board, CollisionSystem):
                self._sound_manager.play_rotate()
                self._update_ghost_piece()
                self._reset_lock_delay()

        elif action == InputAction.DROP:
            # Hard drop
            for _ in range(BOARD_HEIGHT):
                if CollisionSystem.can_move_down(self._current_piece, self._board):
                    self._current_piece.move(0, 1)
                else:
                    break
            self._sound_manager.play_drop()
            self._lock_piece()

        elif action == InputAction.HOLD:
            self._hold_piece()
        
        # Apply gravity
        fall_cells = self._gravity.update(delta_time)
        for _ in range(fall_cells):
            if CollisionSystem.can_move_down(self._current_piece, self._board):
                self._current_piece.move(0, 1)
            else:
                break
        
        self._update_ghost_piece()
        
        # Lock Delay Logic end of tick
        if not CollisionSystem.can_move_down(self._current_piece, self._board):
            self._lock_timer += delta_time * 1000
            if self._lock_timer >= LOCK_DELAY_MS:
                self._lock_piece()
        else:
            self._lock_timer = 0.0

    def _reset_lock_delay(self) -> None:
        """Reset lock delay if the piece was on the ground and limits aren't exceeded"""
        if self._lock_timer > 0 and self._lock_resets < MAX_LOCK_RESETS:
            self._lock_timer = 0.0
            self._lock_resets += 1

    def _lock_piece(self) -> None:
        """Lock current piece in place and spawn new one"""
        self._board.lock_piece(self._current_piece)
        rows_cleared = self._board.clear_rows()
        
        if rows_cleared > 0:
            self._lines += rows_cleared
            self._gravity.add_lines(rows_cleared)
            # Score based on rows cleared
            score_multiplier = {1: 100, 2: 300, 3: 500, 4: 800}
            self._score += score_multiplier.get(rows_cleared, 100)
            self._sound_manager.play_line_clear()

        # Spawn next piece using 7-bag system
        self._current_piece = self._next_piece
        self._next_piece = self._piece_bag.get_next_piece(BOARD_WIDTH // 2 - 1, 0)
        self._can_hold = True
        self._lock_timer = 0.0
        self._lock_resets = 0
        self._update_ghost_piece()

        # Check for game over
        if not CollisionSystem.is_valid_position(self._current_piece, self._board):
            self._state_machine.change_state(GAME_OVER)
            self._scoring.update_high_score(self._score)
            self._sound_manager.play_game_over()

    def _hold_piece(self) -> None:
        """Hold current piece and swap with held piece"""
        if not self._can_hold:
            return
        
        self._sound_manager.play_beep()
        
        if self._held_piece is None:
            self._held_piece = self._current_piece
            self._current_piece = self._next_piece
            self._next_piece = self._piece_bag.get_next_piece(BOARD_WIDTH // 2 - 1, 0)
        else:
            # Swap pieces
            temp = self._current_piece
            self._current_piece = self._held_piece
            self._held_piece = temp
            self._current_piece.set_position(BOARD_WIDTH // 2 - 1, 0)
        
        self._can_hold = False
        self._update_ghost_piece()
    
    def _update_ghost_piece(self) -> None:
        """Update ghost piece preview"""
        if self._current_piece:
            self._ghost_piece = CollisionSystem.get_ghost_piece_blocks(self._current_piece, self._board)

    def render(self) -> None:
        """Render current game state"""
        state = self._state_machine.get_state()

        if state == GAME_MENU:
            self._renderer.render_menu()

        elif state == GAME_RUNNING or state == GAME_PAUSED:
            self._renderer.render(
                self._board,
                self._current_piece,
                self._ghost_piece,
                self._held_piece,
                self._next_piece,
                self._score,
                self._lines,
                self._gravity.get_level(),
                state
            )
            
            # If paused, draw the pause overlay on top of the game!
            if state == GAME_PAUSED:
                self._renderer.render_pause()

        elif state == GAME_OVER:
            self._renderer.render_game_over(
                self._score,
                self._lines,
                self._gravity.get_level(),
                self._scoring.get_high_score()
            )

    def run(self) -> None:

        clock = self._renderer.get_clock()
        running = True

        while running:

            dt = clock.tick(FPS) / 1000.0

            # Process events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                else:
                    self._input.process_event(event)

            # Update game
            running = self.update(dt)

            # Render frame
            self.render()

        self._renderer.quit()