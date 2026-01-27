"""Configuration settings for Crowd Anomaly Detection.

All configuration constants and default values are defined here.
"""

# Video Processing Settings
FRAME_SKIP = 2  # Process every Nth frame for performance
RESIZE_WIDTH = 720  # Target width for frame resizing

# Detection Settings
CONF_THRESHOLD = 0.4  # YOLO confidence threshold

# Tracking History Settings
SPEED_HISTORY = 12  # Number of frames to average speed over
DIR_HISTORY = 8  # Number of frames to average direction over

# Anomaly Detection Thresholds
SPEED_Z_THRESH = 2.5  # Z-score threshold for speed anomaly
DIR_Z_THRESH = 2.0  # Z-score threshold for direction anomaly
LOITER_FRAMES = 80  # Frames before flagging as loitering

# Streamlit Page Configuration
PAGE_CONFIG = {
    "page_title": "Crowd Outlier Detection",
    "page_icon": "🎯",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Model Settings
MODEL_PATH = "yolov8n.pt"

# Visualization Settings
TRAJECTORY_MAX_LENGTH = 40  # Maximum points in trajectory trail
HEATMAP_BLUR_KERNEL = (25, 25)  # Gaussian blur kernel for heatmap
HEATMAP_ALPHA = 0.3  # Heatmap overlay transparency
FRAME_ALPHA = 0.7  # Frame transparency in overlay
