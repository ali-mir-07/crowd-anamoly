"""Video file handling utilities."""

import cv2
import tempfile
from typing import Tuple, Any
from dataclasses import dataclass

from config.settings import RESIZE_WIDTH


@dataclass
class VideoInfo:
    """Video metadata container."""
    total_frames: int
    fps: int
    width: int
    height: int


def load_video(uploaded_file: Any) -> Tuple[cv2.VideoCapture, str]:
    """Load an uploaded video file.
    
    Args:
        uploaded_file: Streamlit uploaded file object.
        
    Returns:
        Tuple of (VideoCapture object, temp file path).
    """
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    tfile.flush()
    
    cap = cv2.VideoCapture(tfile.name)
    return cap, tfile.name


def get_video_info(cap: cv2.VideoCapture) -> VideoInfo:
    """Get video metadata.
    
    Args:
        cap: OpenCV VideoCapture object.
        
    Returns:
        VideoInfo with frame count, fps, and dimensions.
    """
    return VideoInfo(
        total_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        fps=int(cap.get(cv2.CAP_PROP_FPS)),
        width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )


def resize_frame(frame, target_width: int = RESIZE_WIDTH):
    """Resize frame maintaining aspect ratio.
    
    Args:
        frame: Input frame.
        target_width: Target width in pixels.
        
    Returns:
        Resized frame.
    """
    h, w = frame.shape[:2]
    scale = target_width / w
    new_height = int(h * scale)
    return cv2.resize(frame, (target_width, new_height))
