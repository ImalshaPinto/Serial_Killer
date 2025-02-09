
import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((1250, 700))

# Title and Icon
pygame.display.set_caption("Skull Killer")
icon = pygame.image.load('backgroundLevel1.jpg')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('backgroundLevel1.jpg')
background = pygame.transform.scale(background, (1250, 700))

# Load the sprite sheets
sprite_sheet = pygame.image.load('SerialKiller.png')
sprite_sheet1 = pygame.image.load('jump1.png')

# Extract frames from running sprite sheet
def get_frame_Running(row, col, width, height):
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from jumping sprite sheet
def get_frame_jumping(row, col, width, height):
    sheet_width, sheet_height = sprite_sheet1.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        return None  
    return sprite_sheet1.subsurface(pygame.Rect(col * width, row * height, width, height))

# Running Animations
SPRITE_WIDTH, SPRITE_HEIGHT = 265, 300  
standing_frame = get_frame_Running(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)  
running_right_frames = [get_frame_Running(0, i, SPRITE_WIDTH, SPRITE_HEIGHT) for i in range(1, 6)]
running_left_frames = [get_frame_Running(1, i, SPRITE_WIDTH, SPRITE_HEIGHT) for i in range(1, 6)]

# Jumping Animations
SPRITE_WIDTH_JUMPING, SPRITE_HEIGHT_JUMPING = 192, 300
jump_frames = [get_frame_jumping(0, i, SPRITE_WIDTH_JUMPING, SPRITE_HEIGHT_JUMPING) for i in range(6)]
jump_frames = [frame for frame in jump_frames if frame is not None]


# Player properties
playerX, playerY = 370, 350
playerX_change, playerY_change = 0, 0
current_frame = standing_frame
frame_counter, frame_index = 0, 0

# Jumping logic
gravity = 0.5
jump_power = -10
is_jumping = False
velocity_y = 0

# Draw player function
def player(X, Y, frame):
    screen.blit(frame, (X, Y))

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(background, (0, 0))  # Draw the background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key Press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3  # Move left
            if event.key == pygame.K_RIGHT:
                playerX_change = 3   # Move right
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                velocity_y = jump_power  
                frame_index = 0  # Reset jump frame index to start from the beginning

        # Key Release
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                playerX_change = 0  

    # Update X position even when jumping
    playerX += playerX_change

    # Handle Jumping
    if is_jumping:
        playerY += velocity_y
        velocity_y += gravity  
        
        if playerY >= 350:  # Ground level
            playerY = 350
            is_jumping = False  

    # Boundary checks for running and jumping frames
    if playerX < 0:
        playerX = 0
    elif playerX > screen.get_width() - SPRITE_WIDTH:  # Ensure boundary check for running frames
        playerX = screen.get_width() - SPRITE_WIDTH

    # Animation logic with smooth transition and slower jump loop speed (60% of running speed)
    if is_jumping:
        frame_counter += 1
        if frame_counter % int(10 / 1) == 0:  # Slower jump loop speed (60% of running speed)
            frame_index = (frame_index + 1) % len(jump_frames)  # Ensure frame_index is within range
        current_frame = jump_frames[frame_index]
    elif playerX_change > 0:  # Moving Right
        frame_counter += 1
        if frame_counter % 10 == 0:
            frame_index = (frame_index + 1) % len(running_right_frames)  # Ensure frame_index is within range
        current_frame = running_right_frames[frame_index]
    elif playerX_change < 0:  # Moving Left
        frame_counter += 1
        if frame_counter % 10 == 0:
            frame_index = (frame_index + 1) % len(running_left_frames)  # Ensure frame_index is within range
        current_frame = running_left_frames[frame_index]
    else:
        current_frame = standing_frame

    # Draw the player
    player(playerX, playerY, current_frame)

    pygame.display.update()
    clock.tick(60)

pygame.quit()