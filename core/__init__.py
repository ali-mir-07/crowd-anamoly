"""Core module for detection, tracking, and anomaly analysis."""

from .detector import load_model, detect_persons
from .tracker import TrackingState
from .anomaly import AnomalyResult, compute_anomalies

__all__ = [
    "load_model",
    "detect_persons",
    "TrackingState",
    "AnomalyResult",
    "compute_anomalies",
]
