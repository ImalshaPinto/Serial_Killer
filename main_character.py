import pygame
from sprite_utils import get_frame_Stance, get_frame_Running, get_frame_Duck_Up, get_frame_Jump_Directional, get_frame_Jump_Vertical

# Load the sprite sheets
sprite_sheet = pygame.image.load('Scorpian/last.png')
sprite_sheet2 = pygame.image.load('Scorpian/Srunning.png')
sprite_sheet3 = pygame.image.load('Scorpian/duck&up.png')
sprite_sheet4 = pygame.image.load('Scorpian/jumpfront3.png')
sprite_sheet5 = pygame.image.load('Scorpian/jump.png')

class MainCharacter:
    SPRITE_WIDTH, SPRITE_HEIGHT = 167, 290  # Width and height of the character sprite
    SPRITE_WIDTH_STANCE, SPRITE_HEIGHT_STANCE = 167, 290  # Width and height of the stance sprite
    SPRITE_WIDTH_RUNNING, SPRITE_HEIGHT_RUNNING = 132, 300  # Width and height of the running sprite
    SPRITE_WIDTH_DUCK, SPRITE_HEIGHT_DUCK = 132, 290  # Width and height of the duck sprite
    SPRITE_WIDTH_UP, SPRITE_HEIGHT_UP = 132, 290  # Width and height of the up sprite
    SPRITE_WIDTH_JUMP_DIRECTIONAL, SPRITE_HEIGHT_JUMP_DIRECTIONAL = 132, 290  # Width and height of the directional jump sprite
    SPRITE_WIDTH_JUMP_VERTICAL, SPRITE_HEIGHT_JUMP_VERTICAL = 132, 290  # Width and height of the vertical jump sprite

    def __init__(self, x, y):
        self.x = x  # Character's x position
        self.y = y  # Character's y position
        self.x_change = 0  # Change in x position (for movement)
        self.is_ducking = False  # Flag to check if the character is ducking
        self.is_getting_up = False  # Flag to check if the character is getting up
        self.is_jumping_directional = False  # Flag to check if the character is performing a directional jump
        self.is_jumping_vertical = False  # Flag to check if the character is performing a vertical jump
        self.current_frame = get_frame_Stance(sprite_sheet, 0, 0, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)  # Initial frame
        self.frame_index = 0  # Index of the current frame
        self.frame_counter = 0  # Counter for frame updates

        # Load stance frames
        self.stance_frames = [get_frame_Stance(sprite_sheet, 0, i, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE) for i in range(4)]
        self.stance_frames = [frame for frame in self.stance_frames if frame is not None]

        # Load running frames
        self.running_frames = [get_frame_Running(sprite_sheet2, 0, i, self.SPRITE_WIDTH_RUNNING, self.SPRITE_HEIGHT_RUNNING) for i in range(12)]
        self.running_frames = [frame for frame in self.running_frames if frame is not None]

        # Load duck frames
        self.duck_frames = [get_frame_Duck_Up(sprite_sheet3, 0, i, self.SPRITE_WIDTH_DUCK, self.SPRITE_HEIGHT_DUCK) for i in range(3)]
        self.duck_frames = [frame for frame in self.duck_frames if frame is not None]

        # Load up frames
        self.up_frames = [get_frame_Duck_Up(sprite_sheet3, 1, i, self.SPRITE_WIDTH_UP, self.SPRITE_HEIGHT_UP) for i in range(3)]
        self.up_frames = [frame for frame in self.up_frames if frame is not None]

        # Load directional jump frames
        self.jump_right_frames = [get_frame_Jump_Directional(sprite_sheet4, 0, i, self.SPRITE_WIDTH_JUMP_DIRECTIONAL, self.SPRITE_HEIGHT_JUMP_DIRECTIONAL) for i in range(9)]
        self.jump_right_frames = [frame for frame in self.jump_right_frames if frame is not None]
        self.jump_left_frames = [get_frame_Jump_Directional(sprite_sheet4, 1, i, self.SPRITE_WIDTH_JUMP_DIRECTIONAL, self.SPRITE_HEIGHT_JUMP_DIRECTIONAL) for i in range(9)]
        self.jump_left_frames = [frame for frame in self.jump_left_frames if frame is not None]

        # Load vertical jump frames
        self.jump_vertical_frames = [get_frame_Jump_Vertical(sprite_sheet5, 0, i, self.SPRITE_WIDTH_JUMP_VERTICAL, self.SPRITE_HEIGHT_JUMP_VERTICAL) for i in range(3)]
        self.jump_vertical_frames = [frame for frame in self.jump_vertical_frames if frame is not None]

    def update_position(self):
        # Update x position
        self.x += self.x_change

        # Ensure the character stays within the screen bounds
        if self.x < 0:
            self.x = 0
        elif self.x > pygame.display.get_surface().get_width() - self.SPRITE_WIDTH:
            self.x = pygame.display.get_surface().get_width() - self.SPRITE_WIDTH

    def update_frame(self):
        # Update frames based on movement
        self.frame_counter += 1
        if self.is_ducking:  # Ducking
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1)
                if self.frame_index >= len(self.duck_frames):
                    self.frame_index = len(self.duck_frames) - 1  # Hold the last frame
            self.current_frame = self.duck_frames[self.frame_index]
        elif self.is_getting_up:  # Getting up
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1)
                if self.frame_index >= len(self.up_frames):
                    self.frame_index = 0
                    self.is_getting_up = False  # Stop getting up after one loop
            self.current_frame = self.up_frames[self.frame_index]
        elif self.is_jumping_directional:  # Directional Jumping
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1)
                if self.frame_index >= len(self.jump_right_frames):
                    self.frame_index = 0
                    self.is_jumping_directional = False  # Stop jumping after one loop
            if self.x_change > 0:
                self.current_frame = self.jump_right_frames[self.frame_index]
            elif self.x_change < 0:
                self.current_frame = self.jump_left_frames[self.frame_index]
        elif self.is_jumping_vertical:  # Vertical Jumping
            if self.frame_counter % 12 == 0:
                self.frame_index = (self.frame_index + 1)
                if self.frame_index >= len(self.jump_vertical_frames):
                    self.frame_index = 0
                    self.is_jumping_vertical = False  # Stop jumping after one loop
            self.current_frame = self.jump_vertical_frames[self.frame_index]
        elif self.x_change > 0:  # Running right
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.running_frames)
            self.current_frame = self.running_frames[self.frame_index]
        elif self.x_change < 0:  # Running left
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index - 1) % len(self.running_frames)
                if self.frame_index < 0:
                    self.frame_index = len(self.running_frames) - 1
            self.current_frame = self.running_frames[self.frame_index]
        else:  # Stance (display the 0th frame)
            self.current_frame = self.stance_frames[0]

    def draw(self):
        pygame.display.get_surface().blit(self.current_frame, (self.x, self.y))  # Draw the current frame on the screen