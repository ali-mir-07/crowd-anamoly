"""Sidebar configuration and rendering module."""

import streamlit as st
from dataclasses import dataclass
from typing import Any

from config.settings import CONF_THRESHOLD, SPEED_Z_THRESH, DIR_Z_THRESH, LOITER_FRAMES


@dataclass
class SidebarConfig:
    """Configuration values from sidebar sliders."""
    conf_threshold: float
    speed_thresh: float
    dir_thresh: float
    loiter_frames: int
    alert_section: Any


def render_sidebar() -> SidebarConfig:
    """Render the complete sidebar with all controls."""
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")
        
        # Feature showcase
        st.markdown("### ✨ Features")
        
        features = [
            ("🏃", "Speed Anomaly Detection"),
            ("🧭", "Direction Analysis"),
            ("⏱️", "Loitering Detection"),
            ("🔥", "Real-time Heatmap"),
            ("🤖", "Explainable AI Alerts")
        ]
        
        for icon, text in features:
            st.markdown(f"""
            <div class="feature-card">
                <span class="feature-icon">{icon}</span>
                <span class="feature-text">{text}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Configuration
        st.markdown("### ⚙️ Configuration")
        
        conf_threshold = st.slider(
            "Confidence Threshold",
            0.1, 1.0, CONF_THRESHOLD, 0.05,
            help="Detection confidence threshold"
        )
        
        speed_thresh = st.slider(
            "Speed Z-Score Threshold",
            1.0, 5.0, SPEED_Z_THRESH, 0.1,
            help="Threshold for speed anomaly detection"
        )
        
        dir_thresh = st.slider(
            "Direction Z-Score Threshold",
            1.0, 5.0, DIR_Z_THRESH, 0.1,
            help="Threshold for direction anomaly detection"
        )
        
        loiter_frames = st.slider(
            "Loiter Frame Threshold",
            20, 200, LOITER_FRAMES, 10,
            help="Frames before flagging as loitering"
        )
        
        st.markdown("---")
        
        # Legend
        st.markdown("### 🎨 Color Legend")
        st.markdown("""
        <div class="legend-item">
            <div class="legend-color" style="background: #00ff00;"></div>
            <span>Normal Behavior</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #ff0000;"></div>
            <span>Speed/Direction Anomaly</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #ffa500;"></div>
            <span>Loitering Detected</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Alert section
        st.markdown("### 🚨 Live Alerts")
        alert_section = st.empty()
    
    return SidebarConfig(
        conf_threshold=conf_threshold,
        speed_thresh=speed_thresh,
        dir_thresh=dir_thresh,
        loiter_frames=loiter_frames,
        alert_section=alert_section
    )
