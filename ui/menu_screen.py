"""
Menu Screen
Single Responsibility: Handle menu rendering and interactions
Encapsulation: Button management and menu state
"""

import pygame
from typing import Optional, Tuple
from config.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_WHITE, COLOR_BLACK,
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR
)


class Button:
    """Represents a clickable button"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        """
        Initialize button
        
        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Button text
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update button state based on mouse position"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if button is clicked"""
        return self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Draw button on screen
        
        Args:
            screen: Pygame surface to draw on
            font: Font for text rendering
        """
        # Draw button background
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLOR_WHITE, self.rect, 2)
        
        # Draw button text
        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class MenuScreen:
    """
    Menu screen for game
    Single Responsibility: Menu rendering and button management
    """
    
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        """
        Initialize menu screen
        
        Args:
            screen: Pygame surface to draw on
            font: Font for text rendering
        """
        self._screen = screen
        self._font = font
        self._title_font = pygame.font.Font(None, 72)
        self._subtitle_font = pygame.font.Font(None, 36)
        
        # Create buttons
        center_x = WINDOW_WIDTH // 2
        button_y = WINDOW_HEIGHT // 2 + 50
        
        start_x = center_x - BUTTON_WIDTH - 20
        exit_x = center_x + 20
        
        self._start_button = Button(start_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Start")
        self._exit_button = Button(exit_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")
    
    def render(self) -> None:
        """Render menu screen"""
        self._screen.fill(COLOR_BLACK)
        
        # Draw title
        title = self._title_font.render("TETRIS", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self._screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self._subtitle_font.render("ยินดีต้อนรับ", True, (100, 200, 255))
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self._screen.blit(subtitle, subtitle_rect)
        
        # Draw buttons
        self._start_button.draw(self._screen, self._font)
        self._exit_button.draw(self._screen, self._font)
        
    
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update menu state"""
        self._start_button.update(mouse_pos)
        self._exit_button.update(mouse_pos)
    
    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Handle mouse click
        
        Args:
            mouse_pos: Mouse position
            
        Returns:
            'start', 'exit', or None
        """
        if self._start_button.is_clicked(mouse_pos):
            return 'start'
        elif self._exit_button.is_clicked(mouse_pos):
            return 'exit'
        return None


class GameOverScreen:

    def __init__(self, screen, font):

        self._screen = screen
        self._font = font

        self._title_font = pygame.font.Font(None, 72)
        self._subtitle_font = pygame.font.Font(None, 48)

        center_x = WINDOW_WIDTH // 2
        button_y = WINDOW_HEIGHT // 2 + 150

        menu_x = center_x - BUTTON_WIDTH - 20
        exit_x = center_x + 20

        self._menu_button = Button(menu_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Menu")
        self._exit_button = Button(exit_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")

    def render(self, score, lines, level, high_score=0, high_level=0):

        self._screen.fill(COLOR_BLACK)

        mouse_pos = pygame.mouse.get_pos()
        self.update(mouse_pos)

        title = self._title_font.render("GAME OVER", True, (255, 100, 100))
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))

        self._screen.blit(title, title_rect)

        score_text = self._font.render(f"Score: {score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 190))
        self._screen.blit(score_text, score_rect)

        level_text = self._font.render(f"Level: {level}", True, COLOR_WHITE)
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self._screen.blit(level_text, level_rect)

        lines_text = self._font.render(f"Lines: {lines}", True, COLOR_WHITE)
        lines_rect = lines_text.get_rect(center=(WINDOW_WIDTH // 2, 310))
        self._screen.blit(lines_text, lines_rect)

        # Display high score and high level
        high_score_text = self._font.render(f"Best Score: {high_score}", True, (100, 200, 255))
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, 370))
        self._screen.blit(high_score_text, high_score_rect)

        high_level_text = self._font.render(f"Best Level: {high_level}", True, (100, 200, 255))
        high_level_rect = high_level_text.get_rect(center=(WINDOW_WIDTH // 2, 420))
        self._screen.blit(high_level_text, high_level_rect)

        self._menu_button.draw(self._screen, self._font)
        self._exit_button.draw(self._screen, self._font)
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update game over screen state"""
        self._menu_button.update(mouse_pos)
        self._exit_button.update(mouse_pos)
    
    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Handle mouse click
        
        Args:
            mouse_pos: Mouse position
            
        Returns:
            'menu', 'exit', or None
        """
        if self._menu_button.is_clicked(mouse_pos):
            return 'menu'
        elif self._exit_button.is_clicked(mouse_pos):
            return 'exit'
        return None

class PauseScreen:
    """
    Pause screen for game
    Offers options to Resume, Restart, Menu, or Quit.
    """
    
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        self._screen = screen
        self._font = font
        self._title_font = pygame.font.Font(None, 72)
        
        center_x = WINDOW_WIDTH // 2
        
        # Stack 4 buttons vertically
        start_y = WINDOW_HEIGHT // 2 - 80
        spacing = 60
        
        btn_x = center_x - (BUTTON_WIDTH // 2)
        
        self._resume_button = Button(btn_x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Resume")
        self._restart_button = Button(btn_x, start_y + spacing, BUTTON_WIDTH, BUTTON_HEIGHT, "Restart")
        self._menu_button = Button(btn_x, start_y + spacing * 2, BUTTON_WIDTH, BUTTON_HEIGHT, "Menu")
        self._quit_button = Button(btn_x, start_y + spacing * 3, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")

    def render(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)  # Semi-transparent
        overlay.fill(COLOR_BLACK)
        self._screen.blit(overlay, (0, 0))

        # Title
        title = self._title_font.render("PAUSED", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self._screen.blit(title, title_rect)
        
        # Buttons
        self._resume_button.draw(self._screen, self._font)
        self._restart_button.draw(self._screen, self._font)
        self._menu_button.draw(self._screen, self._font)
        self._quit_button.draw(self._screen, self._font)
        
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        self._resume_button.update(mouse_pos)
        self._restart_button.update(mouse_pos)
        self._menu_button.update(mouse_pos)
        self._quit_button.update(mouse_pos)
        
    def handle_click(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        if self._resume_button.is_clicked(mouse_pos):
            return 'resume'
        elif self._restart_button.is_clicked(mouse_pos):
            return 'restart'
        elif self._menu_button.is_clicked(mouse_pos):
            return 'menu'
        elif self._quit_button.is_clicked(mouse_pos):
            return 'exit'
        return None


class GameplayButtons:
    """
    Gameplay buttons for touchscreen and mouse control
    Single Responsibility: Handle button rendering and interaction during gameplay
    """
    
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, small_font: pygame.font.Font):
        """
        Initialize gameplay buttons
        
        Args:
            screen: Pygame surface to draw on
            font: Font for text rendering
            small_font: Smaller font for button text
        """
        self._screen = screen
        self._font = font
        self._small_font = small_font
        
        # Right side button layout
        right_side_x = WINDOW_WIDTH - 180
        
        # Top row: Rotate buttons
        self._rotate_cw_button = Button(right_side_x, 50, 80, 50, "↻")
        self._rotate_ccw_button = Button(right_side_x + 90, 50, 80, 50, "↺")
        
        # Second row: Drop and Hold
        self._drop_button = Button(right_side_x, 110, 80, 50, "DROP")
        self._hold_button = Button(right_side_x + 90, 110, 80, 50, "HOLD")
        
        # Third row: Pause
        self._pause_button = Button(right_side_x + 35, 170, 150, 50, "PAUSE")
        
        # Bottom: D-Pad style controls (left, down, right)
        dpad_x = right_side_x
        dpad_y = 250
        button_size = 50
        
        self._left_button = Button(dpad_x, dpad_y + button_size, button_size, button_size, "◄")
        self._down_button = Button(dpad_x + button_size, dpad_y + button_size, button_size, button_size, "▼")
        self._right_button = Button(dpad_x + button_size * 2, dpad_y + button_size, button_size, button_size, "►")
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update button states based on mouse position"""
        self._rotate_cw_button.update(mouse_pos)
        self._rotate_ccw_button.update(mouse_pos)
        self._drop_button.update(mouse_pos)
        self._hold_button.update(mouse_pos)
        self._pause_button.update(mouse_pos)
        self._left_button.update(mouse_pos)
        self._down_button.update(mouse_pos)
        self._right_button.update(mouse_pos)
    
    def render(self) -> None:
        """Render all gameplay buttons"""
        self._rotate_cw_button.draw(self._screen, self._small_font)
        self._rotate_ccw_button.draw(self._screen, self._small_font)
        self._drop_button.draw(self._screen, self._small_font)
        self._hold_button.draw(self._screen, self._small_font)
        self._pause_button.draw(self._screen, self._small_font)
        self._left_button.draw(self._screen, self._small_font)
        self._down_button.draw(self._screen, self._small_font)
        self._right_button.draw(self._screen, self._small_font)
    
    def get_clicked_action(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Determine which button was clicked
        
        Args:
            mouse_pos: Mouse position
            
        Returns:
            Action string ('rotate_cw', 'rotate_ccw', 'drop', 'hold', 'pause', 'left', 'down', 'right') or None
        """
        if self._rotate_cw_button.is_clicked(mouse_pos):
            return 'rotate_cw'
        elif self._rotate_ccw_button.is_clicked(mouse_pos):
            return 'rotate_ccw'
        elif self._drop_button.is_clicked(mouse_pos):
            return 'drop'
        elif self._hold_button.is_clicked(mouse_pos):
            return 'hold'
        elif self._pause_button.is_clicked(mouse_pos):
            return 'pause'
        elif self._left_button.is_clicked(mouse_pos):
            return 'left'
        elif self._down_button.is_clicked(mouse_pos):
            return 'down'
        elif self._right_button.is_clicked(mouse_pos):
            return 'right'
        return None
