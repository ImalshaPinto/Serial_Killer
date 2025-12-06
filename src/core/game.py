"""
Main game engine and loop.

This module manages the overall game flow, rendering, and event handling.
"""

import pygame
import sys
from typing import Tuple

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND_COLOR, GAME_TITLE,
    PLAYER_START_X, PLAYER_START_Y, ENEMY_START_X, ENEMY_START_Y
)
from src.entities.main_character import MainCharacter
from src.entities.villain import Villain
from src.systems.collision_handler import CollisionHandler
from src.core.game_state import GameState, GameStateManager


class Game:
    """
    Main game engine managing game loop, rendering, and game logic.
    
    Attributes:
        screen (pygame.Surface): The game display surface.
        clock (pygame.time.Clock): Clock for FPS management.
        running (bool): Whether the game loop is active.
        player (MainCharacter): The player character entity.
        villain (Villain): The villain character entity.
        collision_handler (CollisionHandler): Handles collision detection.
        state_manager (GameStateManager): Manages game state transitions.
    """
    
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT):
        """
        Initialize the game.
        
        Args:
            width (int): Screen width in pixels.
            height (int): Screen height in pixels.
        """
        pygame.init()
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        self.running = False
        
        # Initialize game entities
        self.player = MainCharacter(PLAYER_START_X, PLAYER_START_Y)
        self.villain = Villain(ENEMY_START_X, ENEMY_START_Y)
        
        # Initialize game systems
        self.collision_handler = CollisionHandler()
        self.state_manager = GameStateManager()
        
        # Input state tracking
        self.keys_pressed = set()
        
        # Game configuration
        self.width = width
        self.height = height
        
        # Set entity boundary constraints
        self.player.MAX_X = width - self.player.SPRITE_WIDTH_STANCE
        
        # Set up AI behavior timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # AI decision every 1 second
    
    def handle_events(self) -> bool:
        """
        Handle all input events.
        
        Returns:
            bool: False if quit event received, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self._handle_keydown(event.key)
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            
            elif event.type == pygame.USEREVENT + 1:
                # AI behavior timer
                self.villain.random_behavior(self.player.x)
        
        return True
    
    def _handle_keydown(self, key: int) -> None:
        """
        Handle keyboard input for player actions.
        
        Args:
            key (int): The key code pressed.
        """
        if key == pygame.K_LEFT:
            self.player.x_change = -5
        elif key == pygame.K_RIGHT:
            self.player.x_change = 5
        elif key == pygame.K_z:  # Punch
            self.player.punch(self.villain.x)
        elif key == pygame.K_x:  # Double punch
            self.player.double_punch(self.villain.x)
        elif key == pygame.K_c:  # Kick
            self.player.kick(self.villain.x)
    
    def _handle_keyup(self, key: int) -> None:
        """
        Handle keyboard key release events.
        
        Args:
            key (int): The key code released.
        """
        if key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.player.x_change = 0
    
    def update(self) -> None:
        """Update game logic for the current frame."""
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x_change = -5
        elif keys[pygame.K_RIGHT]:
            self.player.x_change = 5
        else:
            if not (keys[pygame.K_z] or keys[pygame.K_x] or keys[pygame.K_c]):
                self.player.x_change = 0
        
        # Update entity positions
        self.player.update_position()
        self.villain.update_position(self.player.x)
        
        # Update animations
        self.player.update_frame(self.villain.x)
        self.villain.update_frame(self.player.x)
        
        # Handle collisions
        self.collision_handler.update(self.player, self.villain)
        
        # Update game state
        self.state_manager.current_state, self.state_manager.character_hit_first, \
            self.state_manager.villain_hit_first = self.state_manager.handle_game_state(
                self.state_manager.current_state,
                self.player,
                self.villain,
                self.state_manager.villain_hit_first,
                self.state_manager.character_hit_first
            )
    
    def render(self) -> None:
        """Render the game frame."""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw game entities
        self.player.draw(self.screen)
        self.villain.draw(self.screen)
        
        # Draw debug info (optional)
        self._draw_debug_info()
        
        # Update display
        pygame.display.flip()
    
    def _draw_debug_info(self) -> None:
        """Draw debug information on screen."""
        font = pygame.font.Font(None, 24)
        
        # Player info
        player_text = font.render(f"Player: {self.player.get_current_action()}", True, (0, 255, 0))
        self.screen.blit(player_text, (10, 10))
        
        # Villain info
        villain_text = font.render(f"Villain: {self.villain.get_current_action()}", True, (255, 0, 0))
        self.screen.blit(villain_text, (10, 35))
        
        # Game state
        state_text = font.render(f"State: {self.state_manager.current_state.value}", True, (255, 255, 255))
        self.screen.blit(state_text, (10, 60))
    
    def run(self) -> None:
        """
        Main game loop.
        
        This method runs the game until the quit event is received.
        """
        self.running = True
        
        while self.running:
            self.running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        self.quit()
    
    def quit(self) -> None:
        """Quit the game and cleanup resources."""
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
