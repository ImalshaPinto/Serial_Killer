"""
Main game engine and loop.

This module manages the overall game flow, rendering, and event handling.
"""

import pygame
import sys
from typing import Tuple

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND_COLOR, GAME_TITLE,
    PLAYER_START_X, PLAYER_START_Y, ENEMY_START_X, ENEMY_START_Y,
    BACKGROUND_IMAGE
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
        
        # Load background image
        try:
            self.background = pygame.image.load(BACKGROUND_IMAGE)
            self.background = pygame.transform.scale(self.background, (width, height))
        except pygame.error as e:
            print(f"Warning: Could not load background image: {e}")
            self.background = None
        
        # Initialize game entities
        self.player = MainCharacter(PLAYER_START_X, PLAYER_START_Y)
        self.villain = Villain(ENEMY_START_X, ENEMY_START_Y)
        
        # Initialize game systems
        self.collision_handler = CollisionHandler()
        self.state_manager = GameStateManager()
        
        # Input state tracking
        self.keys_pressed = set()
        
        # Double-click detection for D key
        self.last_d_press_time = 0
        self.double_click_threshold = 300  # milliseconds
        
        # Round and timer system
        self.round_time = 90  # 90 seconds per round
        self.round_start_time = 0
        self.current_round = 1
        self.max_rounds = 3
        self.player_round_wins = 0
        self.villain_round_wins = 0
        self.round_active = False
        self.game_over = False
        self.winner = None
        
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
                self._handle_keyup(event.key)
            
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
        elif key == pygame.K_UP:  # Jump
            self.player.jump()
        elif key == pygame.K_DOWN:  # Crouch
            self.player.crouch()
        elif key == pygame.K_s:  # Block
            self.player.block()
        elif key == pygame.K_d:  # Punch or Double punch (depends on double-click)
            current_time = pygame.time.get_ticks()
            time_since_last_press = current_time - self.last_d_press_time
            
            # Check if this is a double-click
            if time_since_last_press < self.double_click_threshold:
                # Double-click detected - Double punch
                self.player.double_punch(self.villain.x)
                self.last_d_press_time = 0  # Reset to prevent triple-click
            else:
                # Single click - Regular punch
                self.player.punch(self.villain.x)
                self.last_d_press_time = current_time
        elif key == pygame.K_c:  # Kick
            self.player.kick(self.villain.x)
        elif key == pygame.K_RETURN and self.game_over:  # Restart after game over
            self.restart_game()
    
    def _handle_keyup(self, key: int) -> None:
        """
        Handle keyboard key release events.
        
        Args:
            key (int): The key code released.
        """
        if key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.player.x_change = 0
        elif key == pygame.K_s:  # Stop blocking
            self.player.stop_blocking()
        elif key == pygame.K_DOWN:  # Stand up from crouch
            self.player.stand_up()
    
    def update(self) -> None:
        """Update game logic for the current frame."""
        if self.game_over:
            return
        
        # Start round if not active
        if not self.round_active:
            self.start_round()
        
        # Check timer
        elapsed_time = (pygame.time.get_ticks() - self.round_start_time) / 1000
        if elapsed_time >= self.round_time:
            self.end_round_by_time()
            return
        
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x_change = -5
        elif keys[pygame.K_RIGHT]:
            self.player.x_change = 5
        else:
            if not (keys[pygame.K_d] or keys[pygame.K_c]):
                self.player.x_change = 0
        
        # Update entity positions
        self.player.update_position()
        self.villain.update_position(self.player.x)
        
        # Update animations
        self.player.update_frame(self.villain.x)
        self.villain.update_frame(self.player.x)
        
        # Handle collisions
        self.collision_handler.update(self.player, self.villain)
        
        # Check if anyone is defeated
        if not self.player.is_alive():
            self.end_round("villain")
        elif not self.villain.is_alive():
            self.end_round("player")
        
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
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BACKGROUND_COLOR)
        
        # Draw game entities
        self.player.draw(self.screen)
        self.villain.draw(self.screen)
        
        # Draw UI elements
        self._draw_health_bars()
        self._draw_timer()
        self._draw_round_info()
        
        # Draw game over screen if needed
        if self.game_over:
            self._draw_game_over()
        
        # Draw debug info (optional)
        # self._draw_debug_info()
        
        # Update display
        pygame.display.flip()
    
    def _draw_health_bars(self) -> None:
        """Draw health bars for both characters."""
        # Player health bar (left side)
        bar_width = 300
        bar_height = 30
        bar_x = 50
        bar_y = 20
        
        # Background (red)
        pygame.draw.rect(self.screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Current health (green)
        current_width = int((self.player.health / self.player.max_health) * bar_width)
        pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, current_width, bar_height))
        
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 3)
        
        # Player name
        font = pygame.font.Font(None, 24)
        name_text = font.render("SCORPION", True, (255, 255, 255))
        self.screen.blit(name_text, (bar_x, bar_y - 25))
        
        # Villain health bar (right side)
        villain_bar_x = self.width - bar_width - 50
        
        # Background (red)
        pygame.draw.rect(self.screen, (200, 0, 0), (villain_bar_x, bar_y, bar_width, bar_height))
        
        # Current health (green)
        current_width = int((self.villain.health / self.villain.max_health) * bar_width)
        pygame.draw.rect(self.screen, (0, 200, 0), (villain_bar_x, bar_y, current_width, bar_height))
        
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (villain_bar_x, bar_y, bar_width, bar_height), 3)
        
        # Villain name
        name_text = font.render("SONYA", True, (255, 255, 255))
        self.screen.blit(name_text, (villain_bar_x, bar_y - 25))
    
    def _draw_timer(self) -> None:
        """Draw round timer."""
        if not self.round_active:
            return
        
        elapsed_time = (pygame.time.get_ticks() - self.round_start_time) / 1000
        remaining_time = max(0, self.round_time - int(elapsed_time))
        
        font = pygame.font.Font(None, 48)
        timer_text = font.render(str(remaining_time), True, (255, 255, 0))
        text_rect = timer_text.get_rect(center=(self.width // 2, 40))
        
        # Draw background circle
        pygame.draw.circle(self.screen, (0, 0, 0), (self.width // 2, 40), 35)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.width // 2, 40), 35, 3)
        
        self.screen.blit(timer_text, text_rect)
    
    def _draw_round_info(self) -> None:
        """Draw round number and wins."""
        font = pygame.font.Font(None, 32)
        
        # Round number
        round_text = font.render(f"Round {self.current_round}", True, (255, 255, 255))
        text_rect = round_text.get_rect(center=(self.width // 2, 90))
        self.screen.blit(round_text, text_rect)
        
        # Win indicators (circles below names)
        self._draw_win_indicators(70, 70, self.player_round_wins)  # Player
        self._draw_win_indicators(self.width - 120, 70, self.villain_round_wins)  # Villain
    
    def _draw_win_indicators(self, x: int, y: int, wins: int) -> None:
        """Draw win indicator circles."""
        for i in range(self.max_rounds):
            circle_x = x + (i * 30)
            if i < wins:
                pygame.draw.circle(self.screen, (255, 215, 0), (circle_x, y), 10)  # Gold filled
            else:
                pygame.draw.circle(self.screen, (100, 100, 100), (circle_x, y), 10, 2)  # Gray outline
    
    def _draw_game_over(self) -> None:
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Winner text
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        if self.winner == "player":
            winner_text = font_large.render("SCORPION WINS!", True, (255, 215, 0))
        else:
            winner_text = font_large.render("SONYA WINS!", True, (255, 215, 0))
        
        text_rect = winner_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(winner_text, text_rect)
        
        # Instruction text
        restart_text = font_small.render("Press ENTER to restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def _draw_debug_info(self) -> None:
        """Draw debug information on screen."""
        font = pygame.font.Font(None, 24)
        
        # Player info
        player_text = font.render(f"Player: {self.player.get_current_action()} HP:{self.player.health}", True, (0, 255, 0))
        self.screen.blit(player_text, (10, 120))
        
        # Villain info
        villain_text = font.render(f"Villain: {self.villain.get_current_action()} HP:{self.villain.health}", True, (255, 0, 0))
        self.screen.blit(villain_text, (10, 145))
        
        # Game state
        state_text = font.render(f"State: {self.state_manager.current_state.value}", True, (255, 255, 255))
        self.screen.blit(state_text, (10, 170))
    
    def start_round(self) -> None:
        """Start a new round."""
        self.round_active = True
        self.round_start_time = pygame.time.get_ticks()
        
        # Reset character positions and health
        self.player.x = PLAYER_START_X
        self.player.y = PLAYER_START_Y
        self.player.health = self.player.max_health
        
        self.villain.x = ENEMY_START_X
        self.villain.y = ENEMY_START_Y
        self.villain.health = self.villain.max_health
    
    def end_round(self, winner: str) -> None:
        """End the current round and update wins."""
        self.round_active = False
        
        if winner == "player":
            self.player_round_wins += 1
        else:
            self.villain_round_wins += 1
        
        # Check if game is over (best of 3)
        if self.player_round_wins >= 2:
            self.game_over = True
            self.winner = "player"
        elif self.villain_round_wins >= 2:
            self.game_over = True
            self.winner = "villain"
        else:
            # Next round
            self.current_round += 1
            pygame.time.wait(2000)  # 2 second pause between rounds
    
    def end_round_by_time(self) -> None:
        """End round when time runs out - winner is who has more health."""
        if self.player.health > self.villain.health:
            self.end_round("player")
        elif self.villain.health > self.player.health:
            self.end_round("villain")
        else:
            # Tie - restart round
            self.round_active = False
            pygame.time.wait(2000)
    
    def restart_game(self) -> None:
        """Restart the entire game."""
        self.current_round = 1
        self.player_round_wins = 0
        self.villain_round_wins = 0
        self.game_over = False
        self.winner = None
        self.round_active = False
    
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
