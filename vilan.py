import pygame
from sprite_utils import get_frame_Walking, get_frame_Stance, get_frame_Hit

# Load the sprite sheets
sprite_sheet = pygame.image.load('sonya/Swalking.png')
stance_sheet = pygame.image.load('sonya/stance1.png')
hit_sheet = pygame.image.load('sonya/smallhit.png')

class Villain:
    SPRITE_WIDTH_WALKING, SPRITE_HEIGHT_WALKING = 135, 290
    SPRITE_WIDTH_STANCE, SPRITE_HEIGHT_STANCE = 133, 290
    SPRITE_WIDTH_HIT, SPRITE_HEIGHT_HIT = 133, 290

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_change = 0
        self.current_frame = get_frame_Walking(sprite_sheet, 0, 0, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING)
        self.frame_index = 0
        self.frame_counter = 0
        self.is_hit = False

        # Load walking frames
        self.walking_right = [get_frame_Walking(sprite_sheet, 0, i, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING) for i in range(9)]
        self.walking_left = [get_frame_Walking(sprite_sheet, 1, i, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING) for i in range(9)]

        # Load stance frames
        self.stance_left = [get_frame_Stance(stance_sheet, 0, i, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE) for i in range(7)]
        self.stance_right = [get_frame_Stance(stance_sheet, 1, i, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE) for i in range(7)]

        # Load hit frames
        self.hit_left = [get_frame_Hit(hit_sheet, 0, i, self.SPRITE_WIDTH_HIT, self.SPRITE_HEIGHT_HIT) for i in range(3)]
        self.hit_right = [get_frame_Hit(hit_sheet, 1, i, self.SPRITE_WIDTH_HIT, self.SPRITE_HEIGHT_HIT) for i in range(3)]

    def update_position(self, target_x):
        """Update x position to move towards the target."""
        if self.x < target_x - 10:
            self.x_change = 1  # Move right
        elif self.x > target_x + 100:
            self.x_change = -1  # Move left
        else:
            self.x_change = 0  # Stop moving

        self.x += self.x_change

    def update_frame_right(self):
        """Update frames when the villain is on the right."""
        self.frame_counter += 1
        if self.x_change != 0:  # Walking
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.walking_right)
            self.current_frame = self.walking_right[self.frame_index]
        else:  # Stance
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.stance_right)
            self.current_frame = self.stance_right[self.frame_index]

    def update_frame_left(self):
        """Update frames when the villain is on the left."""
        self.frame_counter += 1
        if self.x_change != 0:  # Walking
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.walking_left)
            self.current_frame = self.walking_left[self.frame_index]
        else:  # Stance
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.stance_left)
            self.current_frame = self.stance_left[self.frame_index]

    def update_frame_hit(self, target_x):
        """Update frames when the villain is hit."""
        self.frame_counter += 1
        if self.frame_counter % 6 == 0:
            self.frame_index += 1
            if self.frame_index >= len(self.hit_left):
                self.frame_index = 0
                self.is_hit = False  # Stop hit animation after one loop
                self.update_frame(target_x)  # Return to stance animation
        if self.x < target_x:
            self.current_frame = self.hit_left[self.frame_index]
        else:
            self.current_frame = self.hit_right[self.frame_index]

    def update_frame(self, target_x):
        """Determine whether to use left or right animation."""
        if self.is_hit:
            self.update_frame_hit(target_x)
        elif self.x < target_x:
            self.update_frame_left()
        else:
            self.update_frame_right()

    def draw(self):
        pygame.display.get_surface().blit(self.current_frame, (self.x, self.y))

    def get_rect(self):
        """Get the rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING)

    def check_collision(self, player_rect):
        """Check for collision with the player."""
        villain_rect = self.get_rect()
        return villain_rect.colliderect(player_rect)