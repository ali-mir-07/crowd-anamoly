"""Object tracking state management module."""

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, Deque, Tuple, List
import numpy as np
import math

from config.settings import SPEED_HISTORY, DIR_HISTORY, TRAJECTORY_MAX_LENGTH


@dataclass
class TrackingState:
    """Manages tracking state for all detected persons.
    
    Attributes:
        track_history: Position history for each track ID.
        speed_hist: Speed history for each track ID.
        dir_hist: Direction history for each track ID.
        loiter_count: Loitering frame counter for each track ID.
    """
    track_history: Dict[int, Deque[Tuple[int, int]]] = field(
        default_factory=lambda: defaultdict(lambda: deque(maxlen=TRAJECTORY_MAX_LENGTH))
    )
    speed_hist: Dict[int, Deque[float]] = field(
        default_factory=lambda: defaultdict(lambda: deque(maxlen=SPEED_HISTORY))
    )
    dir_hist: Dict[int, Deque[float]] = field(
        default_factory=lambda: defaultdict(lambda: deque(maxlen=DIR_HISTORY))
    )
    loiter_count: Dict[int, int] = field(
        default_factory=lambda: defaultdict(int)
    )
    
    def update_track(self, tid: int, cx: int, cy: int) -> Tuple[float, float]:
        """Update tracking data for a given track ID.
        
        Args:
            tid: Track ID.
            cx: Center x coordinate.
            cy: Center y coordinate.
            
        Returns:
            Tuple of (speed, angle) for this update, or (0, 0) if not enough history.
        """
        self.track_history[tid].append((cx, cy))
        
        speed = 0.0
        angle = 0.0
        
        if len(self.track_history[tid]) >= 2:
            p1 = np.array(self.track_history[tid][-2])
            p2 = np.array(self.track_history[tid][-1])
            
            speed = float(np.linalg.norm(p2 - p1))
            angle = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
            
            self.speed_hist[tid].append(speed)
            self.dir_hist[tid].append(angle)
        
        return speed, angle
    
    def get_average_speed(self, tid: int) -> float:
        """Get average speed for a track ID.
        
        Args:
            tid: Track ID.
            
        Returns:
            Average speed over the history window.
        """
        if self.speed_hist[tid]:
            return float(np.mean(self.speed_hist[tid]))
        return 0.0
    
    def get_average_direction(self, tid: int) -> float:
        """Get average direction for a track ID.
        
        Args:
            tid: Track ID.
            
        Returns:
            Average direction in degrees over the history window.
        """
        if self.dir_hist[tid]:
            return float(np.mean(self.dir_hist[tid]))
        return 0.0
    
    def update_loiter_count(self, tid: int, speed: float, threshold: float = 2.0) -> int:
        """Update loitering counter for a track ID.
        
        Args:
            tid: Track ID.
            speed: Current speed.
            threshold: Speed threshold below which to count as loitering.
            
        Returns:
            Updated loiter count.
        """
        if speed < threshold:
            self.loiter_count[tid] += 1
        else:
            self.loiter_count[tid] = 0
        return self.loiter_count[tid]
    
    def get_trajectory_points(self, tid: int) -> List[Tuple[int, int]]:
        """Get trajectory points for a track ID.
        
        Args:
            tid: Track ID.
            
        Returns:
            List of (x, y) position tuples.
        """
        return list(self.track_history[tid])
    
    def get_total_tracked(self) -> int:
        """Get total number of unique tracked IDs.
        
        Returns:
            Number of unique track IDs.
        """
        return len(self.track_history)
