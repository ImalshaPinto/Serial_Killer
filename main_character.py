import pygame

# Load the sprite sheets
sprite_sheet = pygame.image.load('SerialKiller.png')
sprite_sheet1 = pygame.image.load('jump1.png')
sprite_sheet2 = pygame.image.load('handpuch1.png')

# Extract frames from running sprite sheet
def get_frame_Running(row, col, width, height):
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from jumping sprite sheet
def get_frame_jumping(row, col, width, height):
    sheet_width, sheet_height = sprite_sheet1.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        return None  
    return sprite_sheet1.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from jumping sprite sheet for left direction
def get_frame_jumping_left(row, col, width, height):
    sheet_width, sheet_height = sprite_sheet1.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        return None  
    return sprite_sheet1.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from punching sprite sheet
def get_frame_handpunch(row, col, width, height):
    sheet_width, sheet_height = sprite_sheet2.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        return None  
    return sprite_sheet2.subsurface(pygame.Rect(col * width, row * height, width, height))

class MainCharacter:
    SPRITE_WIDTH, SPRITE_HEIGHT = 265, 300  # Width and height of the character sprite
    SPRITE_WIDTH_JUMPING, SPRITE_HEIGHT_JUMPING = 198, 300
    SPRITE_WIDTH_HANDPUNCH, SPRITE_HEIGHT_HANDPUNCH = 290, 300
    SPRITE_WIDTH_SWING, SPRITE_HEIGHT_SWING = 395, 300
    GRAVITY = 0.5
    JUMP_POWER = -10

    def __init__(self, x, y):
        self.x = x  # Character's x position
        self.y = y  # Character's y position
        self.x_change = 0  # Change in x position (for movement)
        self.y_change = 0  # Change in y position (for movement)
        self.current_frame = get_frame_Running(0, 0, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)  # Initial frame
        self.frame_counter = 0  # Counter for frame updates
        self.frame_index = 0  # Index of the current frame
        self.is_jumping = False  # Flag to check if the character is jumping
        self.is_punching = False  # Flag to check if the character is punching
        self.is_swing = False  # Flag to check if the character is swinging
        self.velocity_y = 0  # Vertical velocity for jumping
        
        self.standing_frame = get_frame_Running(0, 0, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)
        self.running_right_frames = [get_frame_Running(0, i, self.SPRITE_WIDTH, self.SPRITE_HEIGHT) for i in range(1, 6)]
        self.running_left_frames = [get_frame_Running(1, i, self.SPRITE_WIDTH, self.SPRITE_HEIGHT) for i in range(1, 6)]
        self.jump_frames = [get_frame_jumping(0, i, self.SPRITE_WIDTH_JUMPING, self.SPRITE_HEIGHT_JUMPING) for i in range(6)]
        self.jump_frames = [frame for frame in self.jump_frames if frame is not None]
        self.jump_left_frames = [get_frame_jumping_left(1, i, self.SPRITE_WIDTH_JUMPING, self.SPRITE_HEIGHT_JUMPING) for i in range(6)]
        self.jump_left_frames = [frame for frame in self.jump_left_frames if frame is not None]
        self.handpunch_frames = [get_frame_handpunch(0, i, self.SPRITE_WIDTH_HANDPUNCH, self.SPRITE_HEIGHT_HANDPUNCH) for i in range(2)]
        self.handpunch_frames = [frame for frame in self.handpunch_frames if frame is not None]
        self.swing_frames = [get_frame_handpunch(1, i, self.SPRITE_WIDTH_SWING, self.SPRITE_HEIGHT_SWING) for i in range(2)]
        self.swing_frames = [frame for frame in self.swing_frames if frame is not None]

    def update_position(self):
        self.x += self.x_change  # Update x position
        if self.is_jumping:
            self.y += self.velocity_y  # Update y position
            self.velocity_y += self.GRAVITY  # Apply gravity
            if self.y >= 350:  # Check if character has landed
                self.y = 350
                self.is_jumping = False

        # Ensure the character stays within the screen bounds
        if self.x < 0:
            self.x = 0
        elif self.x > pygame.display.get_surface().get_width() - self.SPRITE_WIDTH:
            self.x = pygame.display.get_surface().get_width() - self.SPRITE_WIDTH

    def update_frame(self):
        if self.is_swing:
            self.frame_counter += 1
            if self.frame_counter % 10 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.swing_frames)
                if self.frame_index == 0:
                    self.is_swing = False  # Stop swinging after one cycle
            self.current_frame = self.swing_frames[self.frame_index]  # Update current frame to swinging frame
        elif self.is_punching:
            self.frame_counter += 1
            if self.frame_counter % 10 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.handpunch_frames)
                if self.frame_index == 0:
                    self.is_punching = False  # Stop punching after one cycle
            self.current_frame = self.handpunch_frames[self.frame_index]  # Update current frame to punching frame
        elif self.is_jumping:
            self.frame_counter += 1
            if self.frame_counter % int(10 / 1) == 0:
                self.frame_index = (self.frame_index + 1) % len(self.jump_frames)
            if self.x_change < 0:
                self.current_frame = self.jump_left_frames[self.frame_index]  # Update current frame to jumping left frame
            else:
                self.current_frame = self.jump_frames[self.frame_index]  # Update current frame to jumping frame
        elif self.x_change > 0:
            self.frame_counter += 1
            if self.frame_counter % 10 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.running_right_frames)
            self.current_frame = self.running_right_frames[self.frame_index]  # Update current frame to running right frame
        elif self.x_change < 0:
            self.frame_counter += 1
            if self.frame_counter % 10 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.running_left_frames)
            self.current_frame = self.running_left_frames[self.frame_index]  # Update current frame to running left frame
        else:
            self.current_frame = self.standing_frame  # Update current frame to standing frame

    def draw(self):
        pygame.display.get_surface().blit(self.current_frame, (self.x, self.y))  # Draw the current frame on the screen