"""
Sound Manager
Single Responsibility: Handle all sound effects
Encapsulation: Manages pygame mixer and sound loading
"""

import pygame
from typing import Optional


class SoundManager:
    """
    Manages game sounds and music
    Single Responsibility: All audio handling
    """
    
    def __init__(self):
        """Initialize sound manager"""
        pygame.mixer.init()
        self._sounds = {}
        self._music_volume = 0.3
        self._sfx_volume = 0.2
        self._initialized = False
    
    def init(self) -> None:
        """Initialize sound manager - create placeholder sounds since we don't have audio files"""
        self._initialized = True
        # We'll use generated beep sounds instead of loading files
        self._create_sounds()
    
    def _create_sounds(self) -> None:
        """Create simple beep sounds without loading external files"""
        # Create a simple beep sound effect
        self._sounds['beep'] = self._generate_beep(440, 100)  # A4, 100ms
        self._sounds['rotate'] = self._generate_beep(523, 80)  # C5, 80ms
        self._sounds['drop'] = self._generate_beep(330, 150)  # E4, 150ms
        self._sounds['line_clear'] = self._generate_beep(784, 200)  # G5, 200ms
        self._sounds['game_over'] = self._generate_beep(196, 500)  # G3, 500ms
        self._sounds['menu_select'] = self._generate_beep(623, 100)  # B4, 100ms
    
    def _generate_beep(self, frequency: float, duration_ms: int) -> pygame.mixer.Sound:
        """
        Generate a simple beep sound using pure Python (no numpy required)
        
        Args:
            frequency: Frequency in Hz
            duration_ms: Duration in milliseconds
            
        Returns:
            pygame.mixer.Sound object
        """
        sample_rate = 22050
        duration_samples = int(sample_rate * duration_ms / 1000)
        
        # Generate sine wave using pure Python
        import math
        
        wave = []
        for i in range(duration_samples):
            value = math.sin(2.0 * math.pi * frequency * i / sample_rate)
            sample = int(value * 32767)
            sample = max(-32768, min(32767, sample))  # Clamp to 16-bit range
            wave.append(sample)
        
        # Convert to bytes (16-bit PCM, stereo)
        audio_data = bytearray()
        for sample in wave:
            # Convert to 16-bit little-endian
            audio_data.extend(sample.to_bytes(2, byteorder='little', signed=True))
            audio_data.extend(sample.to_bytes(2, byteorder='little', signed=True))  # Stereo: repeat sample
        
        sound = pygame.mixer.Sound(buffer=bytes(audio_data))
        sound.set_volume(self._sfx_volume)
        return sound
    
    def play_sound(self, sound_name: str) -> None:
        """
        Play a sound effect
        
        Args:
            sound_name: Name of sound to play
        """
        if not self._initialized or sound_name not in self._sounds:
            return
        
        try:
            self._sounds[sound_name].play()
        except Exception:
            pass  # Silently ignore sound errors
    
    def play_rotate(self) -> None:
        """Play rotate sound"""
        self.play_sound('rotate')
    
    def play_drop(self) -> None:
        """Play drop sound"""
        self.play_sound('drop')
    
    def play_line_clear(self) -> None:
        """Play line clear sound"""
        self.play_sound('line_clear')
    
    def play_game_over(self) -> None:
        """Play game over sound"""
        self.play_sound('game_over')
    
    def play_menu_select(self) -> None:
        """Play menu select sound"""
        self.play_sound('menu_select')
    
    def play_beep(self) -> None:
        """Play generic beep sound"""
        self.play_sound('beep')
    
    def set_sound_volume(self, volume: float) -> None:
        """
        Set sound effect volume
        
        Args:
            volume: Volume level (0.0-1.0)
        """
        self._sfx_volume = max(0.0, min(1.0, volume))
        for sound in self._sounds.values():
            if sound:
                sound.set_volume(self._sfx_volume)
    
    def quit(self) -> None:
        """Clean up sound manager"""
        pygame.mixer.stop()
        pygame.mixer.quit()
