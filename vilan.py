import pygame
from sprite_utils import get_frame_Walking

# Load the sprite sheet
sprite_sheet = pygame.image.load('sonya/Swalking.png')

class Villain:
    SPRITE_WIDTH_WALKING, SPRITE_HEIGHT_WALKING = 135, 290  # Width and height of the walking sprite

    def __init__(self, x, y):
        self.x = x  # Villain's x position
        self.y = y  # Villain's y position
        self.x_change = 0  # Change in x position (for movement)
        self.current_frame = get_frame_Walking(sprite_sheet, 0, 0, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING)  # Initial frame
        self.frame_index = 0  # Index of the current frame
        self.frame_counter = 0  # Counter for frame updates

        # Load walking frames for both rows
        self.walking_frames_row_0 = [get_frame_Walking(sprite_sheet, 0, i, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING) for i in range(9)]
        self.walking_frames_row_1 = [get_frame_Walking(sprite_sheet, 1, i, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING) for i in range(9)]
        self.walking_frames_row_0 = [frame for frame in self.walking_frames_row_0 if frame is not None]
        self.walking_frames_row_1 = [frame for frame in self.walking_frames_row_1 if frame is not None]

    def update_position(self, target_x):
        # Update x position to move towards the main character while maintaining a distance of 25 pixels
        if self.x < target_x - 10:
            self.x_change = 1  # Move right
        elif self.x > target_x + 100:
            self.x_change = -1  # Move left
        else:
            self.x_change = 0  # Stop moving

        self.x += self.x_change

    def update_frame(self, target_x):
        # Update frames based on movement
        self.frame_counter += 1
        if self.x_change != 0:  # Walking
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.walking_frames_row_0)
            if self.x < target_x:
                self.current_frame = self.walking_frames_row_1[self.frame_index]  # Use row 1 if villain is to the left of the main character
            else:
                self.current_frame = self.walking_frames_row_0[self.frame_index]  # Use row 0 if villain is to the right of the main character

    def draw(self):
        pygame.display.get_surface().blit(self.current_frame, (self.x, self.y))  # Draw the current frame on the screen