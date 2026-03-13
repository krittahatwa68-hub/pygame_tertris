"""
Input Handler
Single Responsibility: Handle all user input
Encapsulation: Input state management
"""

import pygame
from enum import Enum


class InputAction(Enum):
    """Enumeration of possible input actions"""
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    ROTATE = 4
    DROP = 5
    PAUSE = 6
    QUIT = 7
    NONE = 8


class InputHandler:
    """
    Handles user input
    Single Responsibility: Converting events to actions
    """
    
    def __init__(self):
        """Initialize input handler"""
        self._last_move_time = 0
        self._move_delay = 100  # milliseconds
    
    def handle_events(self) -> InputAction:
        """
        Handle pygame events and return action
        
        Returns:
            InputAction representing player's input
        """
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return InputAction.QUIT
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return InputAction.MOVE_LEFT
                elif event.key == pygame.K_RIGHT:
                    return InputAction.MOVE_RIGHT
                elif event.key == pygame.K_DOWN:
                    return InputAction.MOVE_DOWN
                elif event.key == pygame.K_z:
                    return InputAction.ROTATE
                elif event.key == pygame.K_SPACE:
                    return InputAction.DROP
                elif event.key == pygame.K_p:
                    return InputAction.PAUSE
        
        return InputAction.NONE
