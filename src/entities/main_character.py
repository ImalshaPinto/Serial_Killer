"""
Main player character implementation.

This module defines the player-controlled character for the fighting game.
"""

import pygame
from typing import List
from src.entities.character import Character
from src.utils.sprite_utils import SpriteSheet


class MainCharacter(Character):
    """
    The main player-controlled character (Scorpion).
    
    Inherits from Character and implements player-specific behavior including
    movement, attacks, and defensive actions.
    """
    
    # Sprite dimensions for different actions
    SPRITE_WIDTH_STANCE = 133
    SPRITE_HEIGHT_STANCE = 290
    SPRITE_WIDTH_RUNNING = 132
    SPRITE_HEIGHT_RUNNING = 300
    SPRITE_WIDTH_PUNCH = 183
    SPRITE_HEIGHT_PUNCH = 290
    SPRITE_WIDTH_KICK = 185
    SPRITE_HEIGHT_KICK = 290
    SPRITE_WIDTH_HIT = 183
    SPRITE_HEIGHT_HIT = 290
    SPRITE_WIDTH_FALL = 183
    SPRITE_HEIGHT_FALL = 290
    SPRITE_WIDTH_JUMP = 133
    SPRITE_HEIGHT_JUMP = 290
    SPRITE_WIDTH_BLOCK = 133
    SPRITE_HEIGHT_BLOCK = 290
    SPRITE_WIDTH_CROUCH = 133
    SPRITE_HEIGHT_CROUCH = 200
    
    def __init__(self, x: float, y: float, sprites_dir: str = "assets/sprites/Scorpian"):
        """
        Initialize the main character.
        
        Args:
            x (float): Starting X position.
            y (float): Starting Y position.
            sprites_dir (str): Directory containing character sprites.
        """
        super().__init__(x, y)
        
        self.sprites_dir = sprites_dir
        
        # Action flags
        self.is_ducking = False
        self.is_getting_up = False
        self.is_jumping_directional = False
        self.is_jumping_vertical = False
        self.is_double_punching = False
        self.is_punching = False
        self.is_kicking = False
        self.is_und_kicking = False
        
        # Timing
        self.last_a_press_time = 0
        self.last_down_press_time = 0
        self.is_movement_in_progress = False
        self.current_action = None
        
        # Load all sprite frames
        self._load_sprites()
        
        # Set initial frame
        if self.stance_frames_left:
            self.current_frame = self.stance_frames_left[0]
        else:
            self.current_frame = pygame.Surface((self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE))
        
        # Set max X based on screen width
        self.MAX_X = pygame.display.get_surface().get_width() - self.SPRITE_WIDTH_STANCE if pygame.display.get_surface() else None
    
    def _load_sprites(self) -> None:
        """Load all sprite animations from sprite sheets."""
        try:
            # Load stance sprites
            stance_sheet = SpriteSheet(f"{self.sprites_dir}/Sstance1.png")
            self.stance_frames_left = stance_sheet.get_frames(0, 8, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE)
            self.stance_frames_right = stance_sheet.get_frames(1, 8, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE)
            
            # Load running sprites
            running_sheet = SpriteSheet(f"{self.sprites_dir}/Srunning.png")
            self.running_frames_left = running_sheet.get_frames(1, 12, self.SPRITE_WIDTH_RUNNING, self.SPRITE_HEIGHT_RUNNING)
            self.running_frames_right = running_sheet.get_frames(0, 12, self.SPRITE_WIDTH_RUNNING, self.SPRITE_HEIGHT_RUNNING)
            
            # Load punch sprites
            punch_sheet = SpriteSheet(f"{self.sprites_dir}/punch.png")
            self.punch_frames_left = punch_sheet.get_frames(0, 3, self.SPRITE_WIDTH_PUNCH, self.SPRITE_HEIGHT_PUNCH)
            self.punch_frames_right = punch_sheet.get_frames(1, 3, self.SPRITE_WIDTH_PUNCH, self.SPRITE_HEIGHT_PUNCH)
            
            # Load double punch sprites
            double_punch_sheet = SpriteSheet(f"{self.sprites_dir}/Dpunch.png")
            self.double_punch_frames_left = double_punch_sheet.get_frames(0, 6, self.SPRITE_WIDTH_PUNCH, self.SPRITE_HEIGHT_PUNCH)
            self.double_punch_frames_right = double_punch_sheet.get_frames(1, 6, self.SPRITE_WIDTH_PUNCH, self.SPRITE_HEIGHT_PUNCH)
            
            # Load kick sprites
            kick_sheet = SpriteSheet(f"{self.sprites_dir}/bBkick.png")
            self.kick_frames_left = kick_sheet.get_frames(0, 8, self.SPRITE_WIDTH_KICK, self.SPRITE_HEIGHT_KICK)
            self.kick_frames_right = kick_sheet.get_frames(1, 8, self.SPRITE_WIDTH_KICK, self.SPRITE_HEIGHT_KICK)
            
            # Load hit sprites
            hit_sheet = SpriteSheet(f"{self.sprites_dir}/smallhit.png")
            self.hit_frames_left = hit_sheet.get_frames(0, 3, self.SPRITE_WIDTH_HIT, self.SPRITE_HEIGHT_HIT)
            self.hit_frames_right = hit_sheet.get_frames(1, 3, self.SPRITE_WIDTH_HIT, self.SPRITE_HEIGHT_HIT)
            
            # Load fall sprites
            fall_sheet = SpriteSheet(f"{self.sprites_dir}/falling1.png")
            self.fall_frames_left = fall_sheet.get_frames(0, 7, self.SPRITE_WIDTH_FALL, self.SPRITE_HEIGHT_FALL)
            self.fall_frames_right = fall_sheet.get_frames(1, 7, self.SPRITE_WIDTH_FALL, self.SPRITE_HEIGHT_FALL)
            
        except FileNotFoundError as e:
            print(f"Warning: Could not load some sprites: {e}")
    
    def update_frame(self, target_x: float) -> None:
        """
        Update the current animation frame based on character state.
        
        Args:
            target_x (float): Target X position for directional animation.
        """
        self.frame_counter += 1
        
        # Priority-based action updates
        if self.is_double_punching:
            self._update_double_punch_frame(target_x)
        elif self.is_punching:
            self._update_punch_frame(target_x)
        elif self.is_kicking:
            self._update_kick_frame(target_x)
        elif self.is_hit:
            self._update_hit_frame()
        elif self.is_falling:
            self._update_fall_frame()
        elif self.x_change > 0:
            self._update_running_right_frame()
        elif self.x_change < 0:
            self._update_running_left_frame()
        else:
            self._update_stance_frame(target_x)
    
    def _update_stance_frame(self, target_x: float) -> None:
        """Update stance animation frame."""
        if not self.stance_frames_left:
            return
        
        if self.frame_counter % 7 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.stance_frames_left)
        
        frames = self.stance_frames_left if self.x < target_x else self.stance_frames_right
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_running_left_frame(self) -> None:
        """Update left running animation frame."""
        if not hasattr(self, 'running_frames_left') or not self.running_frames_left:
            return
        
        if self.frame_counter % 7 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.running_frames_left)
        
        self.current_frame = self.running_frames_left[min(self.frame_index, len(self.running_frames_left) - 1)]
    
    def _update_running_right_frame(self) -> None:
        """Update right running animation frame."""
        if not hasattr(self, 'running_frames_right') or not self.running_frames_right:
            return
        
        if self.frame_counter % 7 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.running_frames_right)
        
        self.current_frame = self.running_frames_right[min(self.frame_index, len(self.running_frames_right) - 1)]
    
    def _update_punch_frame(self, target_x: float) -> None:
        """Update punch animation frame."""
        if not hasattr(self, 'punch_frames_left') or not self.punch_frames_left:
            return
        
        if self.frame_counter % 8 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.punch_frames_left)
            if self.frame_index == 0:
                self.is_punching = False
                self.is_movement_in_progress = False
        
        frames = self.punch_frames_left if self.x < target_x else self.punch_frames_right
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_double_punch_frame(self, target_x: float) -> None:
        """Update double punch animation frame."""
        if not hasattr(self, 'double_punch_frames_left') or not self.double_punch_frames_left:
            return
        
        if self.frame_counter % 8 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.double_punch_frames_left)
            if self.frame_index == 0:
                self.is_double_punching = False
                self.is_movement_in_progress = False
        
        frames = self.double_punch_frames_left if self.x < target_x else self.double_punch_frames_right
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_kick_frame(self, target_x: float) -> None:
        """Update kick animation frame."""
        if not hasattr(self, 'kick_frames_left') or not self.kick_frames_left:
            return
        
        if self.frame_counter % 5 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.kick_frames_left)
            if self.frame_index == 0:
                self.is_kicking = False
                self.is_movement_in_progress = False
        
        frames = self.kick_frames_left if self.x < target_x else self.kick_frames_right
        self.current_frame = frames[min(self.frame_index, len(frames) - 1)]
    
    def _update_hit_frame(self) -> None:
        """Update hit animation frame."""
        if not hasattr(self, 'hit_frames_left') or not self.hit_frames_left:
            return
        
        if self.frame_counter % 8 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.hit_frames_left)
            if self.frame_index == 0:
                self.is_hit = False
        
        self.current_frame = self.hit_frames_left[self.frame_index]
    
    def _update_fall_frame(self) -> None:
        """Update fall animation frame."""
        if not hasattr(self, 'fall_frames_left') or not self.fall_frames_left:
            return
        
        if self.frame_counter % 8 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.fall_frames_left)
            if self.frame_index == 0:
                self.is_falling = False
        
        self.current_frame = self.fall_frames_left[self.frame_index]
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the character on the screen.
        
        Args:
            screen (pygame.Surface): The game screen surface.
        """
        if self.current_frame:
            screen.blit(self.current_frame, (self.x, self.y))
    
    def punch(self, target_x: float) -> None:
        """
        Execute a punch attack.
        
        Args:
            target_x (float): Target position for directional punch.
        """
        if not self.is_movement_in_progress:
            self.is_punching = True
            self.is_movement_in_progress = True
            self.frame_index = 0
            self.frame_counter = 0
    
    def double_punch(self, target_x: float) -> None:
        """
        Execute a double punch attack.
        
        Args:
            target_x (float): Target position for directional attack.
        """
        if not self.is_movement_in_progress:
            self.is_double_punching = True
            self.is_movement_in_progress = True
            self.frame_index = 0
            self.frame_counter = 0
    
    def kick(self, target_x: float) -> None:
        """
        Execute a kick attack.
        
        Args:
            target_x (float): Target position for directional kick.
        """
        if not self.is_movement_in_progress:
            self.is_kicking = True
            self.is_movement_in_progress = True
            self.frame_index = 0
            self.frame_counter = 0
    
    def block(self) -> None:
        """Enter blocking stance to reduce incoming damage."""
        if not self.is_movement_in_progress and self.on_ground:
            self.is_blocking = True
    
    def stop_blocking(self) -> None:
        """Exit blocking stance."""
        self.is_blocking = False
    
    def crouch(self) -> None:
        """Enter crouching position."""
        if not self.is_movement_in_progress and self.on_ground:
            self.is_crouching = True
    
    def stand_up(self) -> None:
        """Exit crouching position."""
        self.is_crouching = False
    
    def get_current_action(self) -> str:
        """
        Get the character's current action.
        
        Returns:
            str: Description of current action.
        """
        if self.is_blocking:
            return "blocking"
        elif self.is_crouching:
            return "crouching"
        elif self.is_jumping:
            return "jumping"
        elif self.is_double_punching:
            return "double_punching"
        elif self.is_punching:
            return "punching"
        elif self.is_kicking:
            return "kicking"
        elif self.is_hit:
            return "hit"
        elif self.is_falling:
            return "falling"
        elif self.x_change != 0:
            return "running"
        else:
            return "idle"
