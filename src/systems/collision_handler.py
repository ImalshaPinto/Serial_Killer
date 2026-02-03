"""
Collision detection system.

This module handles collision detection and resolution for combat mechanics.
"""

import pygame
from typing import Tuple


class CollisionHandler:
    """
    Handles collision detection between characters in combat.
    
    Attributes:
        last_fall_time (int): Timestamp of the last fall event.
        last_hit_time (int): Timestamp of the last hit event.
        collision_cooldown (int): Cooldown time in milliseconds between collisions.
    """
    
    def __init__(self, collision_cooldown: int = 500):
        """
        Initialize the collision handler.
        
        Args:
            collision_cooldown (int): Cooldown time in milliseconds. Default is 500ms.
        """
        self.last_fall_time = 0
        self.last_hit_time = 0
        self.collision_cooldown = collision_cooldown
    
    def handle_kicking_collision(self, player, villain) -> bool:
        """
        Handle collision when player is kicking.
        
        When a kick connects with the villain, they enter the falling state and take damage.
        
        Args:
            player: The player character entity.
            villain: The villain character entity.
            
        Returns:
            bool: True if collision occurred, False otherwise.
        """
        if (hasattr(player, 'is_kicking') and player.is_kicking and 
            self._rectangles_collide(player, villain)):
            
            if not villain.is_falling_down:
                villain.is_falling_down = True
                villain.is_hit = False
                villain.frame_index = 0
                self.last_fall_time = pygame.time.get_ticks()
                
                # Apply damage and knockback
                damage = 20  # Kick does more damage
                knockback = -30 if villain.x > player.x else 30
                villain.take_damage(damage, knockback)
                
                return True
        
        return False
    
    def handle_punching_collision(self, player, villain) -> bool:
        """
        Handle collision when player is punching.
        
        When a punch connects with the villain, they enter the hit state and take damage.
        Includes cooldown to prevent multiple hits in quick succession.
        
        Args:
            player: The player character entity.
            villain: The villain character entity.
            
        Returns:
            bool: True if collision occurred, False otherwise.
        """
        current_time = pygame.time.get_ticks()
        time_since_fall = current_time - self.last_fall_time
        
        # Check if enough time has passed since the last fall or hit
        if time_since_fall > self.collision_cooldown:
            if (self._is_punching(player) and 
                self._rectangles_collide(player, villain)):
                
                if not villain.is_hit:
                    villain.is_hit = True
                    villain.frame_index = 0
                    self.last_hit_time = current_time
                    
                    # Apply damage and knockback
                    # Double punch does more damage
                    if hasattr(player, 'is_double_punching') and player.is_double_punching:
                        damage = 15
                    else:
                        damage = 8
                    
                    knockback = -15 if villain.x > player.x else 15
                    villain.take_damage(damage, knockback)
                    
                    return True
        
        return False
    
    def update(self, player, villain) -> None:
        """
        Main update method to handle all collision detection for both characters.
        
        Args:
            player: The player character entity.
            villain: The villain character entity.
        """
        # Handle player attacking villain
        self.handle_kicking_collision(player, villain)
        self.handle_punching_collision(player, villain)
        
        # Handle villain attacking player
        self.handle_villain_kicking_collision(villain, player)
        self.handle_villain_punching_collision(villain, player)
    
    def handle_villain_kicking_collision(self, villain, player) -> bool:
        """Handle villain kicking the player."""
        if (hasattr(villain, 'is_kicking') and villain.is_kicking and 
            self._rectangles_collide(villain, player)):
            
            if not player.is_falling:
                player.is_falling = True
                player.is_hit = False
                player.frame_index = 0
                
                # Apply damage and knockback
                damage = 20
                knockback = -30 if player.x > villain.x else 30
                player.take_damage(damage, knockback)
                
                return True
        return False
    
    def handle_villain_punching_collision(self, villain, player) -> bool:
        """Handle villain punching the player."""
        if (self._is_punching(villain) and 
            self._rectangles_collide(villain, player)):
            
            if not player.is_hit:
                player.is_hit = True
                player.frame_index = 0
                
                # Apply damage and knockback
                damage = 12 if (hasattr(villain, 'is_double_punching') and villain.is_double_punching) else 8
                knockback = -15 if player.x > villain.x else 15
                player.take_damage(damage, knockback)
                
                return True
        return False
    
    def is_collision(self, player, villain) -> bool:
        """
        Check if two characters are colliding.
        
        Args:
            player: The player character entity.
            villain: The villain character entity.
            
        Returns:
            bool: True if characters are colliding, False otherwise.
        """
        return self._rectangles_collide(player, villain)
    
    @staticmethod
    def _rectangles_collide(entity1, entity2) -> bool:
        """
        Check if two entity rectangles collide.
        
        Args:
            entity1: First entity with get_rect() method.
            entity2: Second entity with get_rect() method.
            
        Returns:
            bool: True if rectangles overlap.
        """
        rect1 = entity1.get_rect()
        rect2 = entity2.get_rect()
        return rect1.colliderect(rect2)
    
    @staticmethod
    def _is_punching(player) -> bool:
        """
        Check if player is performing any punching action.
        
        Args:
            player: The player character entity.
            
        Returns:
            bool: True if player is punching or double punching.
        """
        return hasattr(player, 'is_punching') and (
            player.is_punching or 
            (hasattr(player, 'is_double_punching') and player.is_double_punching)
        )
    
    def reset_timers(self) -> None:
        """Reset all collision timers."""
        self.last_fall_time = 0
        self.last_hit_time = 0
