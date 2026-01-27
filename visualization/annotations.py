"""Frame annotation functions for bounding boxes, trajectories, and overlays."""

import cv2
import numpy as np
from typing import List, Tuple, Dict, Any


def draw_bounding_box(
    frame: np.ndarray,
    x1: int, y1: int, x2: int, y2: int,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> None:
    """Draw a bounding box on the frame.
    
    Args:
        frame: Video frame to draw on (modified in place).
        x1, y1: Top-left corner coordinates.
        x2, y2: Bottom-right corner coordinates.
        color: BGR color tuple.
        thickness: Line thickness.
    """
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)


def draw_label(
    frame: np.ndarray,
    text: str,
    x: int, y: int,
    color: Tuple[int, int, int] = (0, 255, 0),
    font_scale: float = 0.5,
    thickness: int = 1
) -> None:
    """Draw a label with background on the frame.
    
    Args:
        frame: Video frame to draw on (modified in place).
        text: Label text.
        x, y: Position for label (top-left of bounding box).
        color: BGR color tuple for background.
        font_scale: Font scale.
        thickness: Text thickness.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Draw background rectangle
    cv2.rectangle(frame, (x, y - 25), (x + tw + 10, y), color, -1)
    
    # Draw text
    cv2.putText(frame, text, (x + 5, y - 8), font, font_scale, (255, 255, 255), thickness)


def draw_trajectory(
    frame: np.ndarray,
    points: List[Tuple[int, int]],
    color: Tuple[int, int, int] = (255, 255, 0),
    max_thickness: int = 3
) -> None:
    """Draw a trajectory trail on the frame.
    
    Args:
        frame: Video frame to draw on (modified in place).
        points: List of (x, y) points in the trajectory.
        color: BGR color tuple.
        max_thickness: Maximum line thickness.
    """
    for i in range(1, len(points)):
        # Thickness increases towards the end of the trail
        thickness = int(np.sqrt(float(i) / len(points)) * max_thickness) + 1
        cv2.line(frame, points[i - 1], points[i], color, thickness)


def draw_info_overlay(
    frame: np.ndarray,
    frame_count: int,
    current_persons: int,
    current_anomalies: int,
    position: Tuple[int, int] = (10, 10)
) -> None:
    """Draw information overlay on the frame.
    
    Args:
        frame: Video frame to draw on (modified in place).
        frame_count: Current frame number.
        current_persons: Number of detected persons.
        current_anomalies: Number of current anomalies.
        position: Top-left position for the overlay.
    """
    x, y = position
    
    # Draw background
    cv2.rectangle(frame, (x, y), (x + 210, y + 70), (0, 0, 0), -1)
    cv2.rectangle(frame, (x, y), (x + 210, y + 70), (102, 126, 234), 2)
    
    # Draw text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f"Frame: {frame_count}", (x + 10, y + 25), font, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, f"Persons: {current_persons}", (x + 10, y + 45), font, 0.6, (0, 255, 0), 1)
    cv2.putText(frame, f"Anomalies: {current_anomalies}", (x + 10, y + 65), font, 0.6, (0, 0, 255), 1)


def annotate_frame(
    frame: np.ndarray,
    boxes,
    tracking_state,
    anomaly_results: List[Any],
    frame_count: int
) -> Tuple[np.ndarray, List[str]]:
    """Annotate a frame with all detection visualizations.
    
    Args:
        frame: Original video frame.
        boxes: Detection boxes from YOLO.
        tracking_state: TrackingState instance.
        anomaly_results: List of AnomalyResult objects.
        frame_count: Current frame number.
        
    Returns:
        Tuple of (annotated frame, list of alert messages).
    """
    annotated = frame.copy()
    alerts = []
    current_persons = len(boxes) if boxes is not None else 0
    current_anomalies = 0
    
    # Create a mapping from tid to anomaly result
    anomaly_map = {r.tid: r for r in anomaly_results}
    
    if boxes is not None:
        for box in boxes:
            if box.id is None:
                continue
            
            tid = int(box.id[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Get anomaly result for this track
            result = anomaly_map.get(tid)
            color = result.color if result else (0, 255, 0)
            
            # Draw bounding box
            draw_bounding_box(annotated, x1, y1, x2, y2, color)
            
            # Draw label
            draw_label(annotated, f"ID:{tid}", x1, y1, color)
            
            # Draw trajectory
            points = tracking_state.get_trajectory_points(tid)
            if len(points) > 1:
                draw_trajectory(annotated, points)
            
            # Collect alerts
            if result and result.has_anomaly:
                current_anomalies += 1
                alert_msg = result.get_alert_message()
                if alert_msg:
                    alerts.append(alert_msg)
    
    # Draw info overlay
    draw_info_overlay(annotated, frame_count, current_persons, current_anomalies)
    
    return annotated, alerts
