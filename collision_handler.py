import pygame

class CollisionHandler:
    def __init__(self):
        self.last_fall_time = 0
        self.last_hit_time = 0
        self.collision_cooldown = 500  # 500ms cooldown after falling or getting hit
    
    def handle_kicking_collision(self, player, villain):
        """
        Handle collision when player is kicking
        
        Args:
            player (Character): The player character
            villain (Character): The villain character
        
        Returns:
            bool: True if collision occurred, False otherwise
        """
        # Check if player is kicking and colliding with villain
        if player.is_kicking and player.get_rect().colliderect(villain.get_rect()):
            # Only trigger fall if villain is not already falling
            if not villain.is_falling_down:
                villain.is_falling_down = True
                villain.is_hit = False
                villain.frame_index = 0
                self.last_fall_time = pygame.time.get_ticks()
                return True
        return False
    
    def handle_punching_collision(self, player, villain):
        """
        Handle collision when player is punching
        
        Args:
            player (Character): The player character
            villain (Character): The villain character
        
        Returns:
            bool: True if collision occurred, False otherwise
        """
        # Check time since last fall to prevent immediate re-collision
        current_time = pygame.time.get_ticks()
        time_since_fall = current_time - self.last_fall_time
        
        # Check if enough time has passed since the last fall or hit
        if time_since_fall > self.collision_cooldown:
            # Check for punching collisions
            if ((player.is_punching or player.is_double_punching) and 
                player.get_rect().colliderect(villain.get_rect())):
                
                # Only trigger hit if villain is not already hit
                if not villain.is_hit:
                    villain.is_hit = True
                    villain.frame_index = 0
                    self.last_hit_time = current_time
                    return True
        
        return False
    
    def update(self, player, villain):
        """
        Main update method to handle all collision detection
        
        Args:
            player (Character): The player character
            villain (Character): The villain character
        """
        # First handle kicking collision
        self.handle_kicking_collision(player, villain)
        
        # Then handle punching collision
        self.handle_punching_collision(player, villain)
        
        # Optional: Reset villain states after specific conditions
        if villain.is_falling_down:
            # Logic to reset villain state when they get up
            pass
