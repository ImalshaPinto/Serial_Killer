"""
Sprite utilities module for handling sprite sheet loading and frame extraction.

This module provides utilities for loading sprite sheets and extracting individual
frames for animations.
"""

import pygame
from typing import List, Tuple, Optional


class SpriteSheet:
    """
    A utility class for loading and extracting frames from sprite sheets.
    
    Attributes:
        image (pygame.Surface): The loaded sprite sheet image.
        sheet_size (Tuple[int, int]): The dimensions of the sprite sheet.
    """
    
    def __init__(self, file_path: str) -> None:
        """
        Initialize the sprite sheet.
        
        Args:
            file_path (str): Path to the sprite sheet image.
            
        Raises:
            FileNotFoundError: If the sprite sheet file is not found.
        """
        try:
            self.image = pygame.image.load(file_path)
            self.sheet_size = self.image.get_size()
        except pygame.error as e:
            raise FileNotFoundError(f"Failed to load sprite sheet: {file_path}") from e
    
    def get_frame(self, row: int, col: int, width: int, height: int) -> pygame.Surface:
        """
        Extract a single frame from the sprite sheet.
        
        Args:
            row (int): The row index of the frame.
            col (int): The column index of the frame.
            width (int): The width of the frame.
            height (int): The height of the frame.
            
        Returns:
            pygame.Surface: The extracted frame.
            
        Raises:
            ValueError: If frame dimensions exceed sprite sheet dimensions.
        """
        sheet_width, sheet_height = self.sheet_size
        
        # Validate frame dimensions
        if col * width + width > sheet_width or row * height + height > sheet_height:
            raise ValueError(
                f"Frame dimensions ({width}x{height}) at ({row}, {col}) exceed "
                f"sprite sheet size ({sheet_width}x{sheet_height})"
            )
        
        # Extract frame using subsurface for efficiency
        frame_rect = pygame.Rect(col * width, row * height, width, height)
        return self.image.subsurface(frame_rect)
    
    def get_frames(self, row: int, num_frames: int, width: int, height: int) -> List[pygame.Surface]:
        """
        Extract multiple frames from a single row.
        
        Args:
            row (int): The row index.
            num_frames (int): The number of frames to extract.
            width (int): The width of each frame.
            height (int): The height of each frame.
            
        Returns:
            List[pygame.Surface]: List of extracted frames.
        """
        frames = []
        for col in range(num_frames):
            try:
                frame = self.get_frame(row, col, width, height)
                frames.append(frame)
            except ValueError:
                # Stop if we exceed sprite sheet bounds
                break
        
        return frames
    
    def get_frames_from_rows(
        self,
        rows: List[int],
        cols_per_row: int,
        width: int,
        height: int
    ) -> List[pygame.Surface]:
        """
        Extract frames from multiple rows.
        
        Args:
            rows (List[int]): List of row indices.
            cols_per_row (int): Number of columns per row.
            width (int): Width of each frame.
            height (int): Height of each frame.
            
        Returns:
            List[pygame.Surface]: List of extracted frames.
        """
        frames = []
        for row in rows:
            row_frames = self.get_frames(row, cols_per_row, width, height)
            frames.extend(row_frames)
        
        return frames


def load_sprite_sheet(file_path: str) -> SpriteSheet:
    """
    Load a sprite sheet from file.
    
    Args:
        file_path (str): Path to the sprite sheet image.
        
    Returns:
        SpriteSheet: The loaded sprite sheet object.
    """
    return SpriteSheet(file_path)


def extract_frame(sprite_sheet: pygame.Surface, row: int, col: int,
                 width: int, height: int) -> pygame.Surface:
    """
    Legacy function for extracting a single frame (deprecated).
    
    Use SpriteSheet class instead.
    
    Args:
        sprite_sheet (pygame.Surface): The sprite sheet image.
        row (int): Row index.
        col (int): Column index.
        width (int): Frame width.
        height (int): Frame height.
        
    Returns:
        pygame.Surface: The extracted frame.
    """
    if col * width + width > sprite_sheet.get_width() or \
       row * height + height > sprite_sheet.get_height():
        raise ValueError("Frame dimensions exceed sprite sheet dimensions")
    
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))
