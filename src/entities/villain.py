"""
Villain/Enemy character implementation.

This module defines the AI-controlled enemy character for the fighting game.
"""

import pygame
import random
from typing import List
from src.entities.character import Character
from src.utils.sprite_utils import SpriteSheet


class Villain(Character):
    """
    The AI-controlled villain character (Sonya).
    
    Inherits from Character and implements AI behavior with random decision-making
    and combat actions.
    """
    
    # Sprite dimensions for different actions
    SPRITE_WIDTH_WALKING = 135
    SPRITE_HEIGHT_WALKING = 290
    SPRITE_WIDTH_STANCE = 133
    SPRITE_HEIGHT_STANCE = 290
    SPRITE_WIDTH_HIT = 133
    SPRITE_HEIGHT_HIT = 290
    SPRITE_WIDTH_FALLING = 195
    SPRITE_HEIGHT_FALLING = 290
    SPRITE_WIDTH_PUNCH = 183
    SPRITE_HEIGHT_PUNCH = 290
    SPRITE_WIDTH_KICK = 190
    SPRITE_HEIGHT_KICK = 290
    
    # AI constants
    ATTACK_RANGE = 100
    WALK_RANGE = 200
    
    def __init__(self, x: float, y: float, sprites_dir: str = "assets/sprites/sonya"):
        """
        Initialize the villain character.
        
        Args:
            x (float): Starting X position.
            y (float): Starting Y position.
            sprites_dir (str): Directory containing character sprites.
        """
        super().__init__(x, y)
        
        self.sprites_dir = sprites_dir
        
        # Action flags
        self.is_falling_down = False
        self.is_getting_up = False
        self.is_double_punching = False
        self.is_kicking = False
        
        # AI state
        self.state = "IDLE"
        self.direction = "LEFT"
        self.current_action = None
        self.behavior_timer = 0
        
        # Load all sprite frames
        self._load_sprites()
        
        # Set initial frame
        if self.stance_frames_left:
            self.current_frame = self.stance_frames_left[0]
        else:
            self.current_frame = pygame.Surface((self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE))
    
    def _load_sprites(self) -> None:
        """Load all sprite animations from sprite sheets."""
        try:
            # Load walking sprites
            walking_sheet = SpriteSheet(f"{self.sprites_dir}/Swalking.png")
            self.walking_frames_right = walking_sheet.get_frames(0, 9, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING)
            self.walking_frames_left = walking_sheet.get_frames(1, 9, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING)
            
            # Load stance sprites
            stance_sheet = SpriteSheet(f"{self.sprites_dir}/stance1.png")
            self.stance_frames_left = stance_sheet.get_frames(0, 7, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE)
            self.stance_frames_right = stance_sheet.get_frames(1, 7, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE)
            
            # Load hit sprites
            hit_sheet = SpriteSheet(f"{self.sprites_dir}/smallhit.png")
            self.hit_frames_left = hit_sheet.get_frames(0, 3, self.SPRITE_WIDTH_HIT, self.SPRITE_HEIGHT_HIT)
            self.hit_frames_right = hit_sheet.get_frames(1, 3, self.SPRITE_WIDTH_HIT, self.SPRITE_HEIGHT_HIT)
            
            # Load falling sprites
            falling_sheet = SpriteSheet(f"{self.sprites_dir}/falingdown.png")
            self.falling_frames_left = falling_sheet.get_frames(1, 7, self.SPRITE_WIDTH_FALLING, self.SPRITE_HEIGHT_FALLING)
            self.falling_frames_right = falling_sheet.get_frames(0, 7, self.SPRITE_WIDTH_FALLING, self.SPRITE_HEIGHT_FALLING)
            
            # Load getup sprites
            getup_sheet = SpriteSheet(f"{self.sprites_dir}/getup.png")
            self.getup_frames_left = getup_sheet.get_frames(1, 2, 145, self.SPRITE_HEIGHT_STANCE)
            self.getup_frames_right = getup_sheet.get_frames(0, 2, 145, self.SPRITE_HEIGHT_STANCE)
            
            # Load double punch sprites
            punch_sheet = SpriteSheet(f"{self.sprites_dir}/doublepunching.png")
            self.punch_frames_left = punch_sheet.get_frames(0, 7, self.SPRITE_WIDTH_PUNCH, self.SPRITE_HEIGHT_PUNCH)
            self.punch_frames_right = punch_sheet.get_frames(1, 7, self.SPRITE_WIDTH_PUNCH, self.SPRITE_HEIGHT_PUNCH)
            
            # Load kick sprites
            kick_sheet = SpriteSheet(f"{self.sprites_dir}/kick.png")
            self.kick_frames_left = kick_sheet.get_frames(0, 6, self.SPRITE_WIDTH_KICK, self.SPRITE_HEIGHT_KICK)
            self.kick_frames_right = kick_sheet.get_frames(1, 6, self.SPRITE_WIDTH_KICK, self.SPRITE_HEIGHT_KICK)
            
        except FileNotFoundError as e:
            print(f"Warning: Could not load some villain sprites: {e}")
    
    def update_position(self, target_x: float) -> None:
        """
        Update villain position based on current state and target position.
        
        Args:
            target_x (float): Player's X position.
        """
        if self.state == "WALK":
            if self.x < target_x - 10:
                self.x_change = 1
                self.direction = "RIGHT"
            elif self.x > target_x + self.ATTACK_RANGE:
                self.x_change = -1
                self.direction = "LEFT"
            else:
                self.x_change = 0
        else:
            self.x_change = 0
        
        self.x += self.x_change
    
    def update_frame(self, target_x: float) -> None:
        """
        Update the current animation frame based on villain state.
        
        Args:
            target_x (float): Player's X position for directional animation.
        """
        self.frame_counter += 1
        
        # Priority-based animation updates
        if self.is_falling_down:
            self._update_falling_frame(target_x)
        elif self.is_getting_up:
            self._update_getup_frame(target_x)
        elif self.is_hit:
            self._update_hit_frame(target_x)
        elif self.is_double_punching:
            self._update_punch_frame(target_x)
        elif self.is_kicking:
            self._update_kick_frame(target_x)
        elif self.state == "WALK" and self.x_change != 0:
            self._update_walking_frame(target_x)
        else:
            self._update_stance_frame(target_x)
    
    def _update_stance_frame(self, target_x: float) -> None:
        """Update stance animation frame."""
        if not self.stance_frames_left:
            return
        
        if self.frame_counter % 6 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.stance_frames_left)
        
        frames = self.stance_frames_left if self.x < target_x else self.stance_frames_right
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_walking_frame(self, target_x: float) -> None:
        """Update walking animation frame."""
        frames = self.walking_frames_left if self.x < target_x else self.walking_frames_right
        
        if not frames:
            return
        
        if self.frame_counter % 6 == 0:
            self.frame_index = (self.frame_index + 1) % len(frames)
        
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_hit_frame(self, target_x: float) -> None:
        """Update hit animation frame."""
        frames = self.hit_frames_left if self.x < target_x else self.hit_frames_right
        
        if not frames:
            return
        
        if self.frame_counter % 6 == 0:
            self.frame_index = (self.frame_index + 1) % len(frames)
            if self.frame_index == 0:
                self.is_hit = False
                self.state = "IDLE"
        
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_falling_frame(self, target_x: float) -> None:
        """Update falling animation frame."""
        frames = self.falling_frames_left if self.x < target_x else self.falling_frames_right
        
        if not frames:
            return
        
        if self.frame_counter % 6 == 0:
            if self.frame_index < len(frames) - 1:
                self.frame_index += 1
            else:
                self.is_falling_down = False
                self.is_getting_up = True
                self.frame_index = 0
        
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_getup_frame(self, target_x: float) -> None:
        """Update getup animation frame."""
        frames = self.getup_frames_left if self.x < target_x else self.getup_frames_right
        
        if not frames:
            return
        
        if self.frame_counter % 6 == 0:
            self.frame_index = (self.frame_index + 1) % len(frames)
            if self.frame_index == 0:
                self.is_getting_up = False
                self.state = "IDLE"
        
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_punch_frame(self, target_x: float) -> None:
        """Update punch animation frame."""
        frames = self.punch_frames_left if self.x < target_x else self.punch_frames_right
        
        if not frames:
            return
        
        if self.frame_counter % 8 == 0:
            self.frame_index = (self.frame_index + 1) % len(frames)
            if self.frame_index == 0:
                self.is_double_punching = False
                self.state = "IDLE"
        
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_kick_frame(self, target_x: float) -> None:
        """Update kick animation frame."""
        frames = self.kick_frames_left if self.x < target_x else self.kick_frames_right
        
        if not frames:
            return
        
        if self.frame_counter % 8 == 0:
            self.frame_index = (self.frame_index + 1) % len(frames)
            if self.frame_index == 0:
                self.is_kicking = False
                self.state = "IDLE"
        
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the villain on the screen.
        
        Args:
            screen (pygame.Surface): The game screen surface.
        """
        if self.current_frame:
            screen.blit(self.current_frame, (self.x, self.y))
    
    def get_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the villain.
        
        Returns:
            pygame.Rect: Rectangle representing villain's position and size.
        """
        return pygame.Rect(self.x, self.y, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING)
    
    def random_behavior(self, player_x: float) -> None:
        """
        Execute random AI behavior based on distance to player.
        
        Args:
            player_x (float): Player's X position.
        """
        distance = abs(self.x - player_x)
        
        if distance < self.ATTACK_RANGE:
            # Player is in attack range
            self.state = random.choice(["IDLE", "DOUBLE_PUNCH", "KICK"])
            
            if self.state == "DOUBLE_PUNCH":
                self.is_double_punching = True
                self.frame_index = 0
                self.frame_counter = 0
            elif self.state == "KICK":
                self.is_kicking = True
                self.frame_index = 0
                self.frame_counter = 0
        else:
            # Player is too far, approach them
            self.state = "WALK"
    
    def get_current_action(self) -> str:
        """
        Get the villain's current action.
        
        Returns:
            str: Description of current action.
        """
        if self.is_double_punching:
            return "punching"
        elif self.is_kicking:
            return "kicking"
        elif self.is_hit:
            return "hit"
        elif self.is_falling_down:
            return "falling"
        elif self.is_getting_up:
            return "getting_up"
        elif self.state == "WALK":
            return "walking"
        else:
            return "idle"
