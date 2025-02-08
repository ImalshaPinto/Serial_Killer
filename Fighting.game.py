import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((1250, 700))

# Title and Icon
pygame.display.set_caption("SerialKiller")
icon = pygame.image.load('shadow.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('backgroundLevel1.jpg')
background = pygame.transform.scale(background, (1250, 700))

# Load the sprite sheet
sprite_sheet = pygame.image.load('SerialKiller.png')

# Extract individual frames from the sprite sheet
def get_frame(row, col, width, height):
    """Extract a single frame from the sprite sheet."""
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))

# Define sprite animations
SPRITE_WIDTH, SPRITE_HEIGHT = 265, 300  # Adjust to match your sprite dimensions
standing_frame = get_frame(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)  # Default standing frame
running_right_frames = [get_frame(0, 1, SPRITE_WIDTH, SPRITE_HEIGHT), get_frame(0, 2, SPRITE_WIDTH, SPRITE_HEIGHT),get_frame(0, 3, SPRITE_WIDTH, SPRITE_HEIGHT),get_frame(0, 4, SPRITE_WIDTH, SPRITE_HEIGHT),get_frame(0, 5, SPRITE_WIDTH, SPRITE_HEIGHT)]
running_left_frames = [get_frame(1, 1, SPRITE_WIDTH, SPRITE_HEIGHT), get_frame(1, 2, SPRITE_WIDTH, SPRITE_HEIGHT),get_frame(1, 3, SPRITE_WIDTH, SPRITE_HEIGHT),get_frame(1, 4, SPRITE_WIDTH, SPRITE_HEIGHT),get_frame(1, 5, SPRITE_WIDTH, SPRITE_HEIGHT)]

# Player properties
playerX = 370
playerY = 350
playerX_change = 0
playerY_change = 0
current_frame = standing_frame
frame_counter = 0
frame_index = 0

# Draw the player
def player(X, Y, frame):
    """Draw the player on the screen."""
    screen.blit(frame, (X, Y))

# Game loop
running = True
while running:
    # Fill the screen and draw the background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle keypress events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Update player position
    playerX += playerX_change
    playerY += playerY_change

    # Boundary checks
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1000:  # Considering sprite width
        playerX = 1000
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:  # Considering sprite height
        playerY = 536

    # Animation logic
    if playerX_change > 0:  # Moving right
        frame_counter += 1
        if frame_counter % 80 == 0:  # Change frame every 10 loops
            frame_index = (frame_index + 1) % len(running_right_frames)
        current_frame = running_right_frames[frame_index]
    elif playerX_change < 0:  # Moving left
        frame_counter += 1
        if frame_counter % 80 == 0:
            frame_index = (frame_index + 1) % len(running_left_frames)
        current_frame = running_left_frames[frame_index]
    else:
        current_frame = standing_frame  # Default standing position

    # Draw the player
    player(playerX, playerY, current_frame)

    pygame.display.update()

pygame.quit()