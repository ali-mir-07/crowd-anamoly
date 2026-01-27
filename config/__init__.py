"""Configuration module for Crowd Anomaly Detection."""

from .settings import (
    FRAME_SKIP,
    RESIZE_WIDTH,
    CONF_THRESHOLD,
    SPEED_HISTORY,
    DIR_HISTORY,
    SPEED_Z_THRESH,
    DIR_Z_THRESH,
    LOITER_FRAMES,
    PAGE_CONFIG,
)

__all__ = [
    "FRAME_SKIP",
    "RESIZE_WIDTH",
    "CONF_THRESHOLD",
    "SPEED_HISTORY",
    "DIR_HISTORY",
    "SPEED_Z_THRESH",
    "DIR_Z_THRESH",
    "LOITER_FRAMES",
    "PAGE_CONFIG",
]
