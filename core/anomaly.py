"""Anomaly detection algorithms module."""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np

from config.settings import SPEED_Z_THRESH, DIR_Z_THRESH, LOITER_FRAMES


@dataclass
class AnomalyResult:
    """Result of anomaly detection for a single tracked person.
    
    Attributes:
        tid: Track ID.
        is_speed_anomaly: Whether speed anomaly was detected.
        is_direction_anomaly: Whether direction anomaly was detected.
        is_loitering: Whether loitering was detected.
        speed_z: Z-score for speed.
        dir_z: Z-score for direction.
        loiter_frames: Number of loitering frames.
        anomaly_messages: List of anomaly description messages.
        color: BGR color tuple for visualization.
    """
    tid: int
    is_speed_anomaly: bool = False
    is_direction_anomaly: bool = False
    is_loitering: bool = False
    speed_z: float = 0.0
    dir_z: float = 0.0
    loiter_frames: int = 0
    anomaly_messages: List[str] = None
    color: Tuple[int, int, int] = (0, 255, 0)  # Default green (normal)
    
    def __post_init__(self):
        if self.anomaly_messages is None:
            self.anomaly_messages = []
    
    @property
    def has_anomaly(self) -> bool:
        """Check if any anomaly was detected."""
        return self.is_speed_anomaly or self.is_direction_anomaly or self.is_loitering
    
    def get_alert_message(self) -> Optional[str]:
        """Get formatted alert message if anomalies exist."""
        if not self.anomaly_messages:
            return None
        return f"**ID {self.tid}:** " + " | ".join(self.anomaly_messages)


def compute_z_scores(
    avg_speed: float,
    avg_dir: float,
    mean_speed: float,
    std_speed: float,
    mean_dir: float,
    std_dir: float
) -> Tuple[float, float]:
    """Compute Z-scores for speed and direction.
    
    Args:
        avg_speed: Average speed for the individual.
        avg_dir: Average direction for the individual.
        mean_speed: Population mean speed.
        std_speed: Population standard deviation of speed.
        mean_dir: Population mean direction.
        std_dir: Population standard deviation of direction.
        
    Returns:
        Tuple of (speed_z_score, direction_z_score).
    """
    speed_z = (avg_speed - mean_speed) / std_speed if std_speed > 0 else 0.0
    dir_z = (avg_dir - mean_dir) / std_dir if std_dir > 0 else 0.0
    return speed_z, dir_z


def detect_anomalies(
    tid: int,
    avg_speed: float,
    avg_dir: float,
    loiter_count: int,
    mean_speed: float,
    std_speed: float,
    mean_dir: float,
    std_dir: float,
    speed_thresh: float = SPEED_Z_THRESH,
    dir_thresh: float = DIR_Z_THRESH,
    loiter_thresh: int = LOITER_FRAMES
) -> AnomalyResult:
    """Detect all types of anomalies for a tracked person.
    
    Args:
        tid: Track ID.
        avg_speed: Average speed for this person.
        avg_dir: Average direction for this person.
        loiter_count: Number of frames this person has been loitering.
        mean_speed: Population mean speed.
        std_speed: Population standard deviation of speed.
        mean_dir: Population mean direction.
        std_dir: Population standard deviation of direction.
        speed_thresh: Z-score threshold for speed anomaly.
        dir_thresh: Z-score threshold for direction anomaly.
        loiter_thresh: Frame threshold for loitering detection.
        
    Returns:
        AnomalyResult containing all anomaly information.
    """
    speed_z, dir_z = compute_z_scores(
        avg_speed, avg_dir, mean_speed, std_speed, mean_dir, std_dir
    )
    
    result = AnomalyResult(
        tid=tid,
        speed_z=speed_z,
        dir_z=dir_z,
        loiter_frames=loiter_count
    )
    
    color = (0, 255, 0)  # Green for normal
    
    # Check speed anomaly
    if abs(speed_z) > speed_thresh:
        result.is_speed_anomaly = True
        result.anomaly_messages.append(f"🏃 Speed (Z={speed_z:.1f})")
        color = (0, 0, 255)  # Red
    
    # Check direction anomaly
    if abs(dir_z) > dir_thresh:
        result.is_direction_anomaly = True
        result.anomaly_messages.append(f"🧭 Direction (Z={dir_z:.1f})")
        color = (0, 0, 255)  # Red
    
    # Check loitering
    if loiter_count > loiter_thresh:
        result.is_loitering = True
        result.anomaly_messages.append("⏱️ Loitering")
        if not result.is_speed_anomaly and not result.is_direction_anomaly:
            color = (0, 165, 255)  # Orange for loitering only
    
    result.color = color
    return result


def compute_population_stats(speeds: List[float], dirs: List[float]) -> Tuple[float, float, float, float]:
    """Compute population statistics for speed and direction.
    
    Args:
        speeds: List of speeds from all detections in current frame.
        dirs: List of directions from all detections in current frame.
        
    Returns:
        Tuple of (mean_speed, std_speed, mean_dir, std_dir).
    """
    mean_speed = np.mean(speeds) if speeds else 0.0
    std_speed = np.std(speeds) if speeds and np.std(speeds) > 0 else 1.0
    mean_dir = np.mean(dirs) if dirs else 0.0
    std_dir = np.std(dirs) if dirs and np.std(dirs) > 0 else 1.0
    
    return float(mean_speed), float(std_speed), float(mean_dir), float(std_dir)


def compute_anomalies(
    tracking_state,
    boxes,
    model,
    speeds: List[float],
    dirs: List[float],
    speed_thresh: float = SPEED_Z_THRESH,
    dir_thresh: float = DIR_Z_THRESH,
    loiter_thresh: int = LOITER_FRAMES
) -> List[AnomalyResult]:
    """Compute anomalies for all detected persons in a frame.
    
    Args:
        tracking_state: TrackingState instance.
        boxes: Detection boxes from YOLO.
        model: YOLO model (for class names).
        speeds: List of speeds from current frame.
        dirs: List of directions from current frame.
        speed_thresh: Z-score threshold for speed anomaly.
        dir_thresh: Z-score threshold for direction anomaly.
        loiter_thresh: Frame threshold for loitering.
        
    Returns:
        List of AnomalyResult for each detected person.
    """
    mean_speed, std_speed, mean_dir, std_dir = compute_population_stats(speeds, dirs)
    
    results = []
    for box in boxes:
        if box.id is None:
            continue
        
        tid = int(box.id[0])
        avg_speed = tracking_state.get_average_speed(tid)
        avg_dir = tracking_state.get_average_direction(tid)
        loiter_count = tracking_state.loiter_count[tid]
        
        result = detect_anomalies(
            tid=tid,
            avg_speed=avg_speed,
            avg_dir=avg_dir,
            loiter_count=loiter_count,
            mean_speed=mean_speed,
            std_speed=std_speed,
            mean_dir=mean_dir,
            std_dir=std_dir,
            speed_thresh=speed_thresh,
            dir_thresh=dir_thresh,
            loiter_thresh=loiter_thresh
        )
        results.append(result)
    
    return results
