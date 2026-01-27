"""Custom CSS styles for the Streamlit application."""


def get_custom_css() -> str:
    """Get the complete custom CSS for the application.
    
    Returns:
        CSS string to be injected via st.markdown.
    """
    return """
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        text-align: center;
        margin-top: 10px;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(145deg, #1e3a5f, #2d5a87);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 10px;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        background: linear-gradient(90deg, #00d4ff, #7b2cbf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.85rem;
        margin-top: 5px;
    }
    
    /* Alert styling */
    .alert-box {
        background: linear-gradient(145deg, #2d1f3d, #4a2c5a);
        border-left: 4px solid #ff6b6b;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.4); }
        50% { box-shadow: 0 0 20px 5px rgba(255, 107, 107, 0.2); }
    }
    
    .alert-title {
        color: #ff6b6b;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
    
    .alert-item {
        color: rgba(255,255,255,0.9);
        padding: 8px 12px;
        margin: 5px 0;
        background: rgba(255,107,107,0.1);
        border-radius: 8px;
        font-size: 0.85rem;
    }
    
    /* Control buttons */
    .control-panel {
        background: linear-gradient(145deg, #1e3a5f, #2d5a87);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Video container */
    .video-container {
        background: #0a0a1a;
        border-radius: 20px;
        padding: 10px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Heatmap container */
    .heatmap-container {
        background: linear-gradient(145deg, #1e3a5f, #2d5a87);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .heatmap-title {
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }
    
    .feature-text {
        color: rgba(255,255,255,0.85);
        font-size: 0.95rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* No anomaly card */
    .no-anomaly {
        background: linear-gradient(145deg, #1a4d2e, #2d6a4f);
        border-left: 4px solid #52b788;
        border-radius: 10px;
        padding: 15px;
        color: #95d5b2;
        text-align: center;
    }
    
    /* Legend */
    .legend-item {
        display: flex;
        align-items: center;
        margin: 8px 0;
        color: rgba(255,255,255,0.8);
    }
    
    .legend-color {
        width: 20px;
        height: 20px;
        border-radius: 5px;
        margin-right: 10px;
    }
    
    /* Stats panel */
    .stats-panel {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        height: 100%;
    }
    
    .stats-title {
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(102, 126, 234, 0.5);
    }
    
    /* Live indicator */
    .live-indicator {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 0, 0, 0.2);
        padding: 5px 12px;
        border-radius: 20px;
        margin-bottom: 15px;
    }
    
    .live-dot {
        width: 10px;
        height: 10px;
        background: #ff0000;
        border-radius: 50%;
        margin-right: 8px;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .live-text {
        color: #ff6b6b;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    /* Anomaly breakdown */
    .anomaly-breakdown {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 12px;
        margin-top: 10px;
    }
    
    .breakdown-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.8);
        font-size: 0.85rem;
    }
    
    .breakdown-item:last-child {
        border-bottom: none;
    }
    
    .breakdown-value {
        font-weight: bold;
        color: #00d4ff;
    }
</style>
"""
