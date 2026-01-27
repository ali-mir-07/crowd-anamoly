"""
Crowd Outlier Detection Application

AI-Powered Behavioral Analysis with Explainable Alerts.
Main entry point that orchestrates all modules.
"""

import streamlit as st
import time
import numpy as np

# Configuration
from config.settings import PAGE_CONFIG, FRAME_SKIP, RESIZE_WIDTH

# Core modules
from core.detector import load_model, detect_persons
from core.tracker import TrackingState
from core.anomaly import compute_anomalies, compute_population_stats

# Visualization
from visualization.styles import get_custom_css
from visualization.heatmap import HeatmapGenerator
from visualization.annotations import annotate_frame

# UI Components
from ui.components import (
    render_header,
    render_welcome_screen,
    render_control_panel,
    render_progress,
    render_summary_report,
    render_video_uploader,
    render_heatmap_header,
    render_video_container_start,
    render_video_container_end,
    render_stats_panel_header,
)
from ui.sidebar import render_sidebar
from ui.stats_panel import (
    render_live_indicator,
    render_stat_cards,
    render_anomaly_breakdown,
    render_movement_stats,
)
from ui.alerts import render_alert_section

# Utilities
from utils.video import load_video, get_video_info, resize_frame
from utils.session_state import init_session_state


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(**PAGE_CONFIG)
    
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar and get config
    sidebar_config = render_sidebar()
    
    # Load YOLO model
    model = load_model()
    
    # Video upload section
    uploaded_video = render_video_uploader()
    
    if uploaded_video:
        process_video(uploaded_video, model, sidebar_config)
    else:
        render_welcome_screen()


def process_video(uploaded_video, model, sidebar_config):
    """Process the uploaded video with anomaly detection."""
    # Load video
    cap, _ = load_video(uploaded_video)
    video_info = get_video_info(cap)
    
    st.session_state.total_frames = video_info.total_frames
    
    # Render control panel
    play_btn, pause_btn, stop_btn, playback_speed = render_control_panel()
    
    # Handle button clicks
    if play_btn:
        st.session_state.playing = True
    if pause_btn:
        st.session_state.playing = False
    if stop_btn:
        st.session_state.playing = False
        st.session_state.frame_idx = 0
        cap.set(0, 0)  # CV2.CAP_PROP_POS_FRAMES
    
    # Progress bar
    progress_bar = st.progress(0)
    progress_text = st.empty()
    
    # Heatmap section
    render_heatmap_header()
    heatmap_display = st.empty()
    
    # Video and stats layout
    video_col, stats_col = st.columns([2.5, 1])
    
    with video_col:
        render_video_container_start()
        stframe = st.empty()
        render_video_container_end()
    
    with stats_col:
        render_stats_panel_header()
        live_indicator = st.empty()
        stat1, stat2, stat3, stat4 = st.empty(), st.empty(), st.empty(), st.empty()
        
        st.markdown("#### 📈 Anomaly Breakdown")
        breakdown_placeholder = st.empty()
        
        st.markdown("#### 🏃 Movement Stats")
        movement_stats = st.empty()
    
    # Initialize tracking
    tracking_state = TrackingState()
    heatmap_gen = None
    
    # Counters
    frame_count = 0
    total_detections = 0
    total_anomalies = 0
    speed_anomaly_count = 0
    dir_anomaly_count = 0
    loiter_anomaly_count = 0
    
    # Auto-start
    if not st.session_state.processing_complete:
        st.session_state.playing = True
    
    # Main processing loop
    while cap.isOpened():
        if not st.session_state.playing:
            time.sleep(0.1)
            continue
        
        ret, frame = cap.read()
        if not ret:
            st.session_state.processing_complete = True
            st.session_state.playing = False
            break
        
        frame_count += 1
        if frame_count % FRAME_SKIP != 0:
            continue
        
        # Update progress
        render_progress(progress_bar, progress_text, frame_count, video_info.total_frames)
        
        # Resize frame
        frame = resize_frame(frame, RESIZE_WIDTH)
        
        # Initialize heatmap generator
        if heatmap_gen is None:
            heatmap_gen = HeatmapGenerator(frame.shape[0], frame.shape[1])
        
        # Detection
        results = detect_persons(frame, model, sidebar_config.conf_threshold)
        
        # Process detections
        speeds, dirs = [], []
        current_persons = 0
        boxes = None
        
        if results and results[0].boxes is not None:
            boxes = results[0].boxes
            current_persons = len(boxes)
            total_detections += current_persons
            
            # Update tracking for each detection
            for box in boxes:
                if box.id is None:
                    continue
                
                tid = int(box.id[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                
                # Update tracking
                speed, angle = tracking_state.update_track(tid, cx, cy)
                if speed > 0:
                    speeds.append(speed)
                    dirs.append(angle)
                
                # Update heatmap
                heatmap_gen.update(cx, cy)
                
                # Update loiter count
                avg_speed = tracking_state.get_average_speed(tid)
                tracking_state.update_loiter_count(tid, avg_speed)
        
        # Compute anomalies
        anomaly_results = []
        if boxes is not None:
            anomaly_results = compute_anomalies(
                tracking_state, boxes, model, speeds, dirs,
                sidebar_config.speed_thresh,
                sidebar_config.dir_thresh,
                sidebar_config.loiter_frames
            )
            
            # Count anomalies
            for result in anomaly_results:
                if result.is_speed_anomaly:
                    speed_anomaly_count += 1
                if result.is_direction_anomaly:
                    dir_anomaly_count += 1
                if result.is_loitering:
                    loiter_anomaly_count += 1
                if result.has_anomaly:
                    total_anomalies += 1
        
        # Annotate frame
        annotated, alerts = annotate_frame(
            frame, boxes, tracking_state, anomaly_results, frame_count
        )
        
        # Create overlay with heatmap
        overlay = heatmap_gen.create_overlay(annotated)
        
        # Display heatmap strip
        heat_display = heatmap_gen.get_display_strip(RESIZE_WIDTH)
        heatmap_display.image(heat_display, channels="BGR", use_container_width=True)
        
        # Display video
        stframe.image(overlay, channels="BGR", use_container_width=True)
        
        # Update stats
        current_anomalies = sum(1 for r in anomaly_results if r.has_anomaly)
        
        render_live_indicator(live_indicator)
        render_stat_cards(
            stat1, stat2, stat3, stat4,
            current_persons,
            tracking_state.get_total_tracked(),
            current_anomalies,
            total_anomalies
        )
        render_anomaly_breakdown(
            breakdown_placeholder,
            speed_anomaly_count,
            dir_anomaly_count,
            loiter_anomaly_count
        )
        
        # Movement stats
        mean_speed, std_speed, mean_dir, std_dir = compute_population_stats(speeds, dirs)
        max_speed = float(np.max(speeds)) if speeds else 0.0
        render_movement_stats(movement_stats, mean_speed, max_speed, mean_dir)
        
        # Update alerts
        render_alert_section(sidebar_config.alert_section, alerts)
        
        # Control playback speed
        time.sleep(0.01 / playback_speed)
    
    cap.release()
    
    # Show completion
    if st.session_state.processing_complete:
        render_summary_report(
            video_info.total_frames,
            tracking_state.get_total_tracked(),
            total_anomalies,
            total_detections,
            speed_anomaly_count,
            dir_anomaly_count,
            loiter_anomaly_count
        )


if __name__ == "__main__":
    main()