"""Reusable UI components for the Streamlit application."""

import streamlit as st
from typing import Tuple, Any


def render_header() -> None:
    """Render the main application header."""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Crowd Outlier Detection</h1>
        <p>AI-Powered Behavioral Analysis with Explainable Alerts</p>
    </div>
    """, unsafe_allow_html=True)


def render_welcome_screen() -> None:
    """Render the welcome screen when no video is uploaded."""
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2 style="color: rgba(255,255,255,0.8);">👆 Upload a video to get started</h2>
        <p style="color: rgba(255,255,255,0.5);">
            Supported formats: MP4, AVI, MOV
        </p>
        <br>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
            <div class="stat-card" style="width: 200px;">
                <div style="font-size: 3rem;">🎯</div>
                <div class="stat-label">Real-time Detection</div>
            </div>
            <div class="stat-card" style="width: 200px;">
                <div style="font-size: 3rem;">🔍</div>
                <div class="stat-label">Behavior Analysis</div>
            </div>
            <div class="stat-card" style="width: 200px;">
                <div style="font-size: 3rem;">🤖</div>
                <div class="stat-label">Explainable AI</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_control_panel(playback_speed_default: float = 1.0) -> Tuple[bool, bool, bool, float]:
    """Render the video control panel.
    
    Args:
        playback_speed_default: Default playback speed.
        
    Returns:
        Tuple of (play_clicked, pause_clicked, stop_clicked, playback_speed).
    """
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    
    ctrl_cols = st.columns([1, 1, 1, 3])
    
    with ctrl_cols[0]:
        play_btn = st.button("▶️ Play", use_container_width=True, key="play")
    with ctrl_cols[1]:
        pause_btn = st.button("⏸️ Pause", use_container_width=True, key="pause")
    with ctrl_cols[2]:
        stop_btn = st.button("⏹️ Stop", use_container_width=True, key="stop")
    with ctrl_cols[3]:
        playback_speed = st.select_slider(
            "Speed",
            options=[0.25, 0.5, 1.0, 1.5, 2.0],
            value=playback_speed_default,
            format_func=lambda x: f"{x}x"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return play_btn, pause_btn, stop_btn, playback_speed


def render_progress(progress_bar: Any, progress_text: Any, frame_count: int, total_frames: int) -> None:
    """Update progress display.
    
    Args:
        progress_bar: Streamlit progress bar element.
        progress_text: Streamlit text element for progress.
        frame_count: Current frame number.
        total_frames: Total frames in video.
    """
    progress = frame_count / total_frames if total_frames > 0 else 0
    progress_bar.progress(progress)
    progress_text.markdown(
        f"<p style='text-align: center; color: rgba(255,255,255,0.7);'>"
        f"Frame {frame_count}/{total_frames} | "
        f"{progress*100:.1f}% Complete</p>",
        unsafe_allow_html=True
    )


def render_summary_report(
    total_frames: int,
    total_tracked: int,
    total_anomalies: int,
    total_detections: int,
    speed_anomaly_count: int,
    dir_anomaly_count: int,
    loiter_anomaly_count: int
) -> None:
    """Render the final processing summary report.
    
    Args:
        total_frames: Total frames processed.
        total_tracked: Total unique tracked IDs.
        total_anomalies: Total anomalies detected.
        total_detections: Total person detections.
        speed_anomaly_count: Count of speed anomalies.
        dir_anomaly_count: Count of direction anomalies.
        loiter_anomaly_count: Count of loitering events.
    """
    st.balloons()
    st.success("🎉 Video processing complete!")
    
    # Final summary
    st.markdown("### 📋 Processing Summary")
    
    summary_cols = st.columns(4)
    with summary_cols[0]:
        st.metric("Total Frames", total_frames)
    with summary_cols[1]:
        st.metric("Unique IDs", total_tracked)
    with summary_cols[2]:
        st.metric("Total Anomalies", total_anomalies)
    with summary_cols[3]:
        anomaly_rate = (total_anomalies / max(total_detections, 1)) * 100
        st.metric("Anomaly Rate", f"{anomaly_rate:.1f}%")
    
    # Detailed breakdown
    st.markdown("### 📊 Detailed Anomaly Report")
    report_cols = st.columns(3)
    
    with report_cols[0]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{speed_anomaly_count}</div>
            <div class="stat-label">🏃 Speed Anomalies</div>
        </div>
        """, unsafe_allow_html=True)
    
    with report_cols[1]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{dir_anomaly_count}</div>
            <div class="stat-label">🧭 Direction Anomalies</div>
        </div>
        """, unsafe_allow_html=True)
    
    with report_cols[2]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{loiter_anomaly_count}</div>
            <div class="stat-label">⏱️ Loitering Events</div>
        </div>
        """, unsafe_allow_html=True)


def render_video_uploader() -> Any:
    """Render the video upload component.
    
    Returns:
        Uploaded file object or None.
    """
    st.markdown("### 📹 Upload Video")
    return st.file_uploader(
        "Upload crowd surveillance video",
        type=["mp4", "avi", "mov"],
        help="Supported formats: MP4, AVI, MOV"
    )


def render_heatmap_header() -> None:
    """Render the heatmap section header."""
    st.markdown("""
    <div class="heatmap-container">
        <div class="heatmap-title">🔥 Activity Heatmap</div>
    </div>
    """, unsafe_allow_html=True)


def render_video_container_start() -> None:
    """Render the start of the video container div."""
    st.markdown('<div class="video-container">', unsafe_allow_html=True)


def render_video_container_end() -> None:
    """Render the end of the video container div."""
    st.markdown('</div>', unsafe_allow_html=True)


def render_stats_panel_header() -> None:
    """Render the stats panel header."""
    st.markdown("""
    <div class="stats-panel">
        <div class="stats-title">📊 Live Statistics</div>
    </div>
    """, unsafe_allow_html=True)
