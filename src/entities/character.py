"""
Base character class for fighting game entities.

This module provides the abstract base for all character implementations.
"""

import pygame
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class Character(ABC):
    """
    Abstract base class for all fighting game characters.
    
    Attributes:
        x (float): Character's X position.
        y (float): Character's Y position.
        x_change (float): Horizontal velocity.
        current_frame (pygame.Surface): Current animation frame.
        frame_index (int): Current frame index in animation sequence.
        frame_counter (int): Frame counter for animation timing.
        is_hit (bool): Whether character is being hit.
        is_falling (bool): Whether character is falling.
    """
    
    # Default sprite dimensions (override in subclasses)
    SPRITE_WIDTH = 133
    SPRITE_HEIGHT = 290
    
    # Movement constants
    MAX_X = None  # Will be set based on screen width
    MIN_X = 0
    
    def __init__(self, x: float, y: float):
        """
        Initialize a character.
        
        Args:
            x (float): Starting X position.
            y (float): Starting Y position.
        """
        self.x = x
        self.y = y
        self.x_change = 0
        
        # Animation states
        self.current_frame = None
        self.frame_index = 0
        self.frame_counter = 0
        
        # Combat states
        self.is_hit = False
        self.is_falling = False
        
        # Frame collections
        self.stance_frames_left: List[pygame.Surface] = []
        self.stance_frames_right: List[pygame.Surface] = []
    
    def update_position(self) -> None:
        """
        Update character position and enforce boundary constraints.
        
        This method should be called each frame to update the character's position
        and ensure they stay within screen boundaries.
        """
        self.x += self.x_change
        
        # Enforce screen boundaries
        self.x = max(self.MIN_X, self.x)
        
        if self.MAX_X is not None:
            self.x = min(self.MAX_X, self.x)
    
    @abstractmethod
    def update_frame(self, target_x: float) -> None:
        """
        Update the current animation frame.
        
        Args:
            target_x (float): Target X position for directional animation.
        """
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the character on the screen.
        
        Args:
            screen (pygame.Surface): The game screen surface.
        """
        pass
    
    def get_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the character.
        
        Returns:
            pygame.Rect: Rectangle representing character's position and size.
        """
        return pygame.Rect(self.x, self.y, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)
    
    def get_position(self) -> Tuple[float, float]:
        """
        Get the character's current position.
        
        Returns:
            Tuple[float, float]: (x, y) position tuple.
        """
        return (self.x, self.y)
    
    def set_position(self, x: float, y: float) -> None:
        """
        Set the character's position.
        
        Args:
            x (float): New X position.
            y (float): New Y position.
        """
        self.x = x
        self.y = y
    
    def get_direction(self, target_x: float) -> str:
        """
        Determine the direction the character should face.
        
        Args:
            target_x (float): Target X position to face towards.
            
        Returns:
            str: "LEFT" or "RIGHT" direction.
        """
        return "LEFT" if self.x < target_x else "RIGHT"
    
    def reset_animation(self) -> None:
        """Reset animation to starting frame."""
        self.frame_index = 0
        self.frame_counter = 0
    
    def is_idle(self) -> bool:
        """
        Check if character is in idle state.
        
        Returns:
            bool: True if character is not performing any action.
        """
        return not any([
            self.is_hit,
            self.is_falling,
            self.x_change != 0
        ])
