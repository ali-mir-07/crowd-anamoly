"""Live statistics panel components."""

import streamlit as st
from typing import Any


def render_live_indicator(placeholder: Any) -> None:
    """Render the LIVE indicator with pulse animation."""
    placeholder.markdown("""
    <div class="live-indicator">
        <div class="live-dot"></div>
        <span class="live-text">LIVE</span>
    </div>
    """, unsafe_allow_html=True)


def render_stat_cards(
    stat1: Any, stat2: Any, stat3: Any, stat4: Any,
    current_persons: int,
    total_tracked: int,
    current_anomalies: int,
    total_anomalies: int
) -> None:
    """Render the four stat cards."""
    stat1.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{current_persons}</div>
        <div class="stat-label">👥 Current Persons</div>
    </div>
    """, unsafe_allow_html=True)
    
    stat2.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_tracked}</div>
        <div class="stat-label">🔢 Total Tracked</div>
    </div>
    """, unsafe_allow_html=True)
    
    stat3.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{current_anomalies}</div>
        <div class="stat-label">⚠️ Active Anomalies</div>
    </div>
    """, unsafe_allow_html=True)
    
    stat4.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_anomalies}</div>
        <div class="stat-label">📊 Total Anomalies</div>
    </div>
    """, unsafe_allow_html=True)


def render_anomaly_breakdown(
    placeholder: Any,
    speed_count: int,
    dir_count: int,
    loiter_count: int
) -> None:
    """Render the anomaly breakdown section."""
    placeholder.markdown(f"""
    <div class="anomaly-breakdown">
        <div class="breakdown-item">
            <span>🏃 Speed Anomalies</span>
            <span class="breakdown-value">{speed_count}</span>
        </div>
        <div class="breakdown-item">
            <span>🧭 Direction Anomalies</span>
            <span class="breakdown-value">{dir_count}</span>
        </div>
        <div class="breakdown-item">
            <span>⏱️ Loitering Events</span>
            <span class="breakdown-value">{loiter_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_movement_stats(
    placeholder: Any,
    avg_speed: float,
    max_speed: float,
    mean_dir: float
) -> None:
    """Render the movement statistics section."""
    placeholder.markdown(f"""
    <div class="anomaly-breakdown">
        <div class="breakdown-item">
            <span>📏 Avg Speed</span>
            <span class="breakdown-value">{avg_speed:.1f} px/f</span>
        </div>
        <div class="breakdown-item">
            <span>🚀 Max Speed</span>
            <span class="breakdown-value">{max_speed:.1f} px/f</span>
        </div>
        <div class="breakdown-item">
            <span>📐 Avg Direction</span>
            <span class="breakdown-value">{mean_dir:.1f}°</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
