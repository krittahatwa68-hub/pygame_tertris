"""
Input Behavior System
Implements Delayed Auto Shift (DAS) and Auto Repeat Rate (ARR)
Advanced Tetris mechanics for precise input handling
"""

import config.config as cfg

class DASARRSystem:
    """
    Delayed Auto Shift (DAS) and Auto Repeat Rate (ARR) system
    
    DAS: Delay before continuous movement begins
    ARR: Rate of continuous movement once DAS is triggered
    
    Single Responsibility: Handle advanced movement input timing
    """
    
    def __init__(self):
        """Initialize DAS/ARR system"""
        self._das_counter_left = 0
        self._das_counter_right = 0
        self._arr_counter_left = 0
        self._arr_counter_right = 0
        self._key_pressed_left = False
        self._key_pressed_right = False
    
    def update_left_press(self) -> bool:
        """
        Check if left movement should occur
        Returns True when movement should happen
        """
        if not self._key_pressed_left:
            self._das_counter_left = 0
            self._arr_counter_left = 0
            return False
        
        # Initial press
        if self._das_counter_left == 0:
            self._das_counter_left = 1
            self._arr_counter_left = 0
            return True
        
        self._das_counter_left += 1
        
        # After DAS delay, start ARR
        if self._das_counter_left > cfg.DAS_DELAY:
            self._arr_counter_left += 1
            if self._arr_counter_left >= cfg.ARR:
                self._arr_counter_left = 0
                return True
        
        return False
    
    def update_right_press(self) -> bool:
        """
        Check if right movement should occur
        Returns True when movement should happen
        """
        if not self._key_pressed_right:
            self._das_counter_right = 0
            self._arr_counter_right = 0
            return False
        
        # Initial press
        if self._das_counter_right == 0:
            self._das_counter_right = 1
            self._arr_counter_right = 0
            return True
        
        self._das_counter_right += 1
        
        # After DAS delay, start ARR
        if self._das_counter_right > cfg.DAS_DELAY:
            self._arr_counter_right += 1
            if self._arr_counter_right >= cfg.ARR:
                self._arr_counter_right = 0
                return True
        
        return False
    
    def set_left_pressed(self, pressed: bool) -> None:
        """Set whether left key is currently pressed"""
        self._key_pressed_left = pressed
        if not pressed:
            self._das_counter_left = 0
            self._arr_counter_left = 0
    
    def set_right_pressed(self, pressed: bool) -> None:
        """Set whether right key is currently pressed"""
        self._key_pressed_right = pressed
        if not pressed:
            self._das_counter_right = 0
            self._arr_counter_right = 0
    
    def reset(self) -> None:
        """Reset all counters"""
        self._das_counter_left = 0
        self._das_counter_right = 0
        self._arr_counter_left = 0
        self._arr_counter_right = 0
        self._key_pressed_left = False
        self._key_pressed_right = False
    
    @staticmethod
    def get_das_delay() -> int:
        """Get DAS delay in frames"""
        return cfg.DAS_DELAY
    
    @staticmethod
    def get_arr() -> int:
        """Get ARR in frames"""
        return cfg.ARR
