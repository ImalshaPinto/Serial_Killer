import pygame

def get_frame(sprite_sheet, row, col, width, height):
    """Extract a frame from a sprite sheet."""
    sheet_width, sheet_height = sprite_sheet.get_size()
    # print(f"Extracting frame at row: {row}, col: {col}, width: {width}, height: {height}")  # Comment out or remove this line
    if col * width + width > sheet_width or row * height + height > sheet_height:
        raise ValueError("Frame dimensions exceed sprite sheet dimensions")
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from stance sprite sheet
def get_frame_Stance(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from running sprite sheet
def get_frame_Running(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from duck and up sprite sheet
def get_frame_Duck_Up(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from directional jump sprite sheet
def get_frame_Jump_Directional(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from vertical jump sprite sheet
def get_frame_Jump_Vertical(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from double punch sprite sheet
def get_frame_Double_Punch(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from punch sprite sheet
def get_frame_Punch(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from kick sprite sheet
def get_frame_Kick(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from underkick sprite sheet
def get_frame_Underkick(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

def get_frame_small_hit(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

def get_frame_falling(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

####################################################

# Extract frames from walking sprite sheet
def get_frame_Walking(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from hit sprite sheet
def get_frame_Hit(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from falling down sprite sheet
def get_frame_FallingDown(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from getup sprite sheet
def get_frame_GetUp(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from double punching sprite sheet
def get_frame_DoublePunching(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)

# Extract frames from kick sprite sheet
def get_frame_kicking(sprite_sheet, row, col, width, height):
    return get_frame(sprite_sheet, row, col, width, height)


