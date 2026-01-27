"""YOLO-based person detection module."""

import streamlit as st
from ultralytics import YOLO

from config.settings import MODEL_PATH, CONF_THRESHOLD


@st.cache_resource
def load_model(model_path: str = MODEL_PATH) -> YOLO:
    """Load and cache the YOLO model.
    
    Args:
        model_path: Path to the YOLO model weights file.
        
    Returns:
        Loaded YOLO model instance.
    """
    return YOLO(model_path)


def detect_persons(frame, model: YOLO, conf_threshold: float = CONF_THRESHOLD):
    """Run person detection on a frame using the YOLO model.
    
    Args:
        frame: Input video frame (numpy array).
        model: Loaded YOLO model instance.
        conf_threshold: Confidence threshold for detections.
        
    Returns:
        YOLO detection results with tracking enabled.
    """
    results = model.track(
        frame,
        persist=True,
        conf=conf_threshold,
        verbose=False
    )
    return results
