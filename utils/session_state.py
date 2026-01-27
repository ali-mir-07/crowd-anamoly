"""Streamlit session state management."""

import streamlit as st


def init_session_state() -> None:
    """Initialize all session state variables."""
    defaults = {
        'playing': False,
        'frame_idx': 0,
        'total_frames': 0,
        'total_detections': 0,
        'total_anomalies': 0,
        'processing_complete': False,
        'speed_anomalies': 0,
        'dir_anomalies': 0,
        'loiter_anomalies': 0
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def reset_session_state() -> None:
    """Reset session state for a new video."""
    st.session_state.playing = False
    st.session_state.frame_idx = 0
    st.session_state.processing_complete = False
    st.session_state.total_detections = 0
    st.session_state.total_anomalies = 0
    st.session_state.speed_anomalies = 0
    st.session_state.dir_anomalies = 0
    st.session_state.loiter_anomalies = 0


def set_playing(playing: bool) -> None:
    """Set the playing state."""
    st.session_state.playing = playing


def is_playing() -> bool:
    """Check if video is currently playing."""
    return st.session_state.playing


def set_processing_complete(complete: bool) -> None:
    """Set processing complete state."""
    st.session_state.processing_complete = complete


def is_processing_complete() -> bool:
    """Check if processing is complete."""
    return st.session_state.processing_complete
