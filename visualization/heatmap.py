"""Heatmap generation and rendering module."""

import cv2
import numpy as np
from typing import Tuple, Optional

from config.settings import HEATMAP_BLUR_KERNEL, HEATMAP_ALPHA, FRAME_ALPHA


class HeatmapGenerator:
    """Generates and manages activity heatmaps.
    
    Accumulates position data over time and renders as a colored heatmap.
    """
    
    def __init__(self, height: int, width: int):
        """Initialize heatmap generator.
        
        Args:
            height: Frame height in pixels.
            width: Frame width in pixels.
        """
        self.heatmap = np.zeros((height, width), dtype=np.float32)
        self.height = height
        self.width = width
    
    def update(self, cx: int, cy: int) -> None:
        """Add a point to the heatmap.
        
        Args:
            cx: Center x coordinate.
            cy: Center y coordinate.
        """
        # Ensure coordinates are within bounds
        cy_safe = min(max(0, cy), self.height - 1)
        cx_safe = min(max(0, cx), self.width - 1)
        self.heatmap[cy_safe, cx_safe] += 1
    
    def render(self) -> np.ndarray:
        """Render the heatmap as a colored image.
        
        Returns:
            BGR colored heatmap image.
        """
        # Apply Gaussian blur for smooth appearance
        heat_blurred = cv2.GaussianBlur(self.heatmap, HEATMAP_BLUR_KERNEL, 0)
        
        # Normalize to 0-255 range
        heat_norm = cv2.normalize(heat_blurred, None, 0, 255, cv2.NORM_MINMAX)
        heat_norm = heat_norm.astype(np.uint8)
        
        # Apply color map
        heat_colored = cv2.applyColorMap(heat_norm, cv2.COLORMAP_JET)
        
        return heat_colored
    
    def create_overlay(self, frame: np.ndarray) -> np.ndarray:
        """Create frame with heatmap overlay.
        
        Args:
            frame: Original video frame.
            
        Returns:
            Frame with heatmap overlaid.
        """
        heat_colored = self.render()
        overlay = cv2.addWeighted(frame, FRAME_ALPHA, heat_colored, HEATMAP_ALPHA, 0)
        return overlay
    
    def get_display_strip(self, width: int, height: int = 80) -> np.ndarray:
        """Get a resized heatmap strip for display.
        
        Args:
            width: Target width.
            height: Target height (default 80).
            
        Returns:
            Resized colored heatmap image.
        """
        heat_colored = self.render()
        return cv2.resize(heat_colored, (width, height))
    
    def reset(self) -> None:
        """Reset the heatmap to zeros."""
        self.heatmap = np.zeros((self.height, self.width), dtype=np.float32)


def create_heatmap_generator(frame: np.ndarray) -> HeatmapGenerator:
    """Factory function to create a HeatmapGenerator from a frame.
    
    Args:
        frame: Video frame to get dimensions from.
        
    Returns:
        Initialized HeatmapGenerator.
    """
    height, width = frame.shape[:2]
    return HeatmapGenerator(height, width)
