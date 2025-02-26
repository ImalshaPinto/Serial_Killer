import pygame

# Extract frames from stance sprite sheet
def get_frame_Stance(sprite_sheet, row, col, width, height):
    sheet_width, sheet_height = sprite_sheet.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        raise ValueError("Frame dimensions exceed sprite sheet dimensions")
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from running sprite sheet
def get_frame_Running(sprite_sheet, row, col, width, height):
    sheet_width, sheet_height = sprite_sheet.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        raise ValueError("Frame dimensions exceed sprite sheet dimensions")
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from duck and up sprite sheet
def get_frame_Duck_Up(sprite_sheet, row, col, width, height):
    sheet_width, sheet_height = sprite_sheet.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        raise ValueError("Frame dimensions exceed sprite sheet dimensions")
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from directional jump sprite sheet
def get_frame_Jump_Directional(sprite_sheet, row, col, width, height):
    sheet_width, sheet_height = sprite_sheet.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        raise ValueError("Frame dimensions exceed sprite sheet dimensions")
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from vertical jump sprite sheet
def get_frame_Jump_Vertical(sprite_sheet, row, col, width, height):
    sheet_width, sheet_height = sprite_sheet.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        raise ValueError("Frame dimensions exceed sprite sheet dimensions")
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))