"""Visualization module for heatmaps, annotations, and styling."""

from .heatmap import HeatmapGenerator
from .annotations import (
    draw_bounding_box,
    draw_label,
    draw_trajectory,
    draw_info_overlay,
    annotate_frame,
)
from .styles import get_custom_css

__all__ = [
    "HeatmapGenerator",
    "draw_bounding_box",
    "draw_label",
    "draw_trajectory",
    "draw_info_overlay",
    "annotate_frame",
    "get_custom_css",
]
