"""
Input Handler
Single Responsibility: Handle all user input
Encapsulation: Input state management
Advanced Mechanics: DAS + ARR for professional input handling
"""

import pygame
from enum import Enum
from input.input_behavior import DASARRSystem


class InputAction(Enum):
    """Enumeration of possible input actions"""
    
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    ROTATE = 4
    ROTATE_CCW = 5
    DROP = 6
    HOLD = 7
    PAUSE = 8
    RESTART = 9
    QUIT = 10
    CLICK = 11
    NONE = 12


class InputHandler:

    def __init__(self):
        self._action = InputAction.NONE
        self._mouse_pos = (0, 0)
        self._mouse_clicked = False
        self._quit_requested = False
        
        # Key state tracking for DAS/ARR
        self._keys_pressed = set()
        self._dasarr_system = DASARRSystem()

    def process_event(self, event):

        self._mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_clicked = True
            self._action = InputAction.CLICK

        elif event.type == pygame.QUIT:
            self._quit_requested = True

        elif event.type == pygame.KEYDOWN:
            # Track pressed keys for DAS/ARR
            self._keys_pressed.add(event.key)

            if event.key in (pygame.K_LEFT, pygame.K_a):
                self._dasarr_system.set_left_pressed(True)

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._dasarr_system.set_right_pressed(True)

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._action = InputAction.MOVE_DOWN

            elif event.key in (pygame.K_UP, pygame.K_z):
                self._action = InputAction.ROTATE

            elif event.key in (pygame.K_x,):
                self._action = InputAction.ROTATE_CCW

            elif event.key == pygame.K_q:
                self._action = InputAction.QUIT

            elif event.key in (pygame.K_SPACE, pygame.K_w):
                self._action = InputAction.DROP

            elif event.key == pygame.K_c:
                self._action = InputAction.HOLD

            elif event.key in (pygame.K_p, pygame.K_ESCAPE):
                self._action = InputAction.PAUSE

            elif event.key == pygame.K_r:
                self._action = InputAction.RESTART

        elif event.type == pygame.KEYUP:
            # Track released keys
            if event.key in self._keys_pressed:
                self._keys_pressed.discard(event.key)
            
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self._dasarr_system.set_left_pressed(False)

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._dasarr_system.set_right_pressed(False)

    def handle_events(self):
        """Process all pending pygame events and return the current action"""
        # Process all queued events
        for event in pygame.event.get():
            self.process_event(event)
        
        # Check if quit was requested (from window close or Q key)
        if self._quit_requested:
            action = InputAction.QUIT
            self._quit_requested = False
            self._action = InputAction.NONE
            return action
        
        # Apply DAS/ARR for left/right movement
        if self._dasarr_system.update_left_press():
            action = InputAction.MOVE_LEFT
            self._action = InputAction.NONE
            return action
        
        if self._dasarr_system.update_right_press():
            action = InputAction.MOVE_RIGHT
            self._action = InputAction.NONE
            return action

        action = self._action
        self._action = InputAction.NONE
        return action

    def get_mouse_pos(self):
        return self._mouse_pos

    def is_mouse_clicked(self):
        clicked = self._mouse_clicked
        self._mouse_clicked = False
        return clicked
