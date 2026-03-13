"""
Game Renderer
Single Responsibility: All rendering logic
Dependency Injection: Receives pygame and board/game state
"""

import pygame
from typing import Optional
from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, BOARD_X, BOARD_Y,
    COLOR_BLACK, COLOR_WHITE, COLOR_LIGHT_GRAY, BOARD_WIDTH, BOARD_HEIGHT
)
from src.board import Board
from src.pieces import Tetromino
from src.menu_screen import MenuScreen, GameOverScreen


class Renderer:
    """
    Handles all rendering of the game
    Encapsulation: Private pygame objects and assets
    """
    
    def __init__(self, width: int = WINDOW_WIDTH, height: int = WINDOW_HEIGHT):
        """
        Initialize renderer
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        self._width = width
        self._height = height
        self._screen: Optional[pygame.Surface] = None
        self._clock: Optional[pygame.time.Clock] = None
        self._font: Optional[pygame.font.Font] = None
        self._small_font: Optional[pygame.font.Font] = None
        self._menu_screen: Optional[MenuScreen] = None
        self._game_over_screen: Optional[GameOverScreen] = None
    
    def init(self) -> None:
        """Initialize pygame and create window"""
        pygame.init()
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Tetris - OOP & SOLID Principles Demo")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.Font(None, 36)
        self._small_font = pygame.font.Font(None, 24)
        self._menu_screen = MenuScreen(self._screen, self._font)
        self._game_over_screen = GameOverScreen(self._screen, self._font)
    
    def render(self, board: Board, current_piece: Optional[Tetromino], 
               score: int, lines: int, game_state: int) -> None:
        """
        Render entire game state
        Composition: Uses board and piece objects
        
        Args:
            board: Game board
            current_piece: Current falling piece
            score: Current score
            lines: Lines cleared
            game_state: Current game state
        """
        self._screen.fill(COLOR_BLACK)
        
        # Draw board
        self._draw_board(board)
        
        # Draw grid
        self._draw_grid()
        
        # Draw current piece
        if current_piece:
            self._draw_piece(current_piece)
        
        # Draw UI
        self._draw_ui(score, lines, game_state)
        
        pygame.display.flip()
    
    def _draw_board(self, board: Board) -> None:
        """Draw locked pieces on board"""
        grid = board.get_grid()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                color = grid[y][x]
                if color != COLOR_BLACK:
                    self._draw_cell(x, y, color)
    
    def _draw_piece(self, piece: Tetromino) -> None:
        """Draw current falling piece"""
        color = piece.get_color()
        for x, y in piece.get_blocks():
            if 0 <= y < BOARD_HEIGHT:
                self._draw_cell(x, y, color)
    
    def _draw_cell(self, x: int, y: int, color: tuple) -> None:
        """
        Draw single cell
        
        Args:
            x: Column
            y: Row
            color: RGB color tuple
        """
        pixel_x = BOARD_X + x * CELL_SIZE
        pixel_y = BOARD_Y + y * CELL_SIZE
        
        rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self._screen, color, rect)
        pygame.draw.rect(self._screen, COLOR_LIGHT_GRAY, rect, 1)
    
    def _draw_grid(self) -> None:
        """Draw board grid lines"""
        # Vertical lines
        for x in range(BOARD_WIDTH + 1):
            start_pos = (BOARD_X + x * CELL_SIZE, BOARD_Y)
            end_pos = (BOARD_X + x * CELL_SIZE, BOARD_Y + BOARD_HEIGHT * CELL_SIZE)
            pygame.draw.line(self._screen, COLOR_LIGHT_GRAY, start_pos, end_pos)
        
        # Horizontal lines
        for y in range(BOARD_HEIGHT + 1):
            start_pos = (BOARD_X, BOARD_Y + y * CELL_SIZE)
            end_pos = (BOARD_X + BOARD_WIDTH * CELL_SIZE, BOARD_Y + y * CELL_SIZE)
            pygame.draw.line(self._screen, COLOR_LIGHT_GRAY, start_pos, end_pos)
    
    def _draw_ui(self, score: int, lines: int, game_state: int) -> None:
        """
        Draw UI elements (score, lines, game state)
        
        Args:
            score: Current score
            lines: Lines cleared
            game_state: Current game state
        """
        ui_x = BOARD_X + BOARD_WIDTH * CELL_SIZE + 50
        
        # Score
        score_text = self._font.render(f"Score: {score}", True, COLOR_WHITE)
        self._screen.blit(score_text, (ui_x, 50))
        
        # Lines
        lines_text = self._small_font.render(f"Lines: {lines}", True, COLOR_WHITE)
        self._screen.blit(lines_text, (ui_x, 100))
        
        # Instructions
        inst_y = 150
        instructions = [
            "Arrow Keys: Move",
            "Z: Rotate",
            "Space: Drop",
            "P: Pause",
        ]
        
        for i, instruction in enumerate(instructions):
            text = self._small_font.render(instruction, True, COLOR_WHITE)
            self._screen.blit(text, (ui_x, inst_y + i * 30))
    
    def get_clock(self) -> pygame.time.Clock:
        """Get pygame clock"""
        return self._clock
    
    def render_menu(self) -> None:
        """Render menu screen"""
        if self._menu_screen:
            self._menu_screen.render()
    
    def update_menu(self, mouse_pos: tuple) -> None:
        """Update menu state"""
        if self._menu_screen:
            self._menu_screen.update(mouse_pos)
    
    def handle_menu_click(self, mouse_pos: tuple) -> Optional[str]:
        """
        Handle menu click
        
        Args:
            mouse_pos: Mouse position
            
        Returns:
            'start', 'exit', or None
        """
        if self._menu_screen:
            return self._menu_screen.handle_click(mouse_pos)
        return None
    
    def render_game_over(self, score: int, lines: int, high_score: int = 0) -> None:
        """Render game over screen"""
        if self._game_over_screen:
            self._game_over_screen.render(score, lines, high_score)
    
    def update_game_over(self, mouse_pos: tuple) -> None:
        """Update game over screen state"""
        if self._game_over_screen:
            self._game_over_screen.update(mouse_pos)
    
    def handle_game_over_click(self, mouse_pos: tuple) -> Optional[str]:
        """
        Handle game over screen click
        
        Args:
            mouse_pos: Mouse position
            
        Returns:
            'menu', 'exit', or None
        """
        if self._game_over_screen:
            return self._game_over_screen.handle_click(mouse_pos)
        return None
    
    def quit(self) -> None:
        """Clean up and quit pygame"""
        pygame.quit()
