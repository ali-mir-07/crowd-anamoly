"""Alert rendering module."""

from typing import List, Any


def render_alert_section(placeholder: Any, alerts: List[str]) -> None:
    """Render alerts in the sidebar section.
    
    Args:
        placeholder: Streamlit placeholder for alert section.
        alerts: List of alert message strings.
    """
    if alerts:
        alert_html = '<div class="alert-box">'
        alert_html += '<div class="alert-title">🚨 Active Alerts</div>'
        for alert in alerts[:5]:  # Show max 5 alerts
            alert_html += f'<div class="alert-item">{alert}</div>'
        if len(alerts) > 5:
            alert_html += f'<div class="alert-item">...and {len(alerts)-5} more</div>'
        alert_html += '</div>'
    else:
        alert_html = '<div class="no-anomaly">✅ No anomalies detected</div>'
    
    placeholder.markdown(alert_html, unsafe_allow_html=True)
