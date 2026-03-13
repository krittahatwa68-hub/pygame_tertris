"""
Menu Screen
Single Responsibility: Handle menu rendering and interactions
Encapsulation: Button management and menu state
"""

import pygame
from typing import Optional, Tuple
from src.config import (
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
        
        pygame.display.flip()
    
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
    """
    Game over screen
    Single Responsibility: Game over rendering and button management
    """
    
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        """
        Initialize game over screen
        
        Args:
            screen: Pygame surface to draw on
            font: Font for text rendering
        """
        self._screen = screen
        self._font = font
        self._title_font = pygame.font.Font(None, 72)
        self._subtitle_font = pygame.font.Font(None, 48)
        
        # Create buttons
        center_x = WINDOW_WIDTH // 2
        button_y = WINDOW_HEIGHT // 2 + 150
        
        menu_x = center_x - BUTTON_WIDTH - 20
        exit_x = center_x + 20
        
        self._menu_button = Button(menu_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Start")
        self._exit_button = Button(exit_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")
    
    def render(self, score: int, lines: int, high_score: int = 0) -> None:
        """
        Render game over screen
        
        Args:
            score: Final score
            lines: Lines cleared
            high_score: Highest score ever
        """
        self._screen.fill(COLOR_BLACK)
        
        # Draw title
        title = self._title_font.render("แพ้แล้ว!", True, (255, 100, 100))
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self._screen.blit(title, title_rect)
        
        # Draw game over text
        game_over_text = self._subtitle_font.render("GAME OVER", True, COLOR_WHITE)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 160))
        self._screen.blit(game_over_text, game_over_rect)
        
        # Draw current score
        score_text = self._font.render(f"Score: {score}", True, (0, 255, 100))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 240))
        self._screen.blit(score_text, score_rect)
        
        # Draw lines cleared
        lines_text = self._font.render(f"Lines: {lines}", True, (100, 150, 255))
        lines_rect = lines_text.get_rect(center=(WINDOW_WIDTH // 2, 290))
        self._screen.blit(lines_text, lines_rect)
        
        # Draw high score
        high_score_text = self._font.render(f"High Score: {high_score}", True, (255, 200, 0))
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, 340))
        self._screen.blit(high_score_text, high_score_rect)
        
        # Draw buttons
        self._menu_button.draw(self._screen, self._font)
        self._exit_button.draw(self._screen, self._font)
        
        pygame.display.flip()
    
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
