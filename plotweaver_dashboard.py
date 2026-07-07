import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(page_title="PlotWeaver — Partner Health", layout="wide")

# Custom CSS - Light theme with Arial/Calibri
st.markdown("""
<style>
    * {
        font-family: 'Calibri', 'Arial', sans-serif !important;
    }
    
    body {
        background-color: white;
        color: white;
    }
    
    .header { 
        font-size: 36px; 
        font-weight: 700; 
        margin-bottom: 8px; 
        color: white;
        font-family: 'Calibri', 'Arial', sans-serif;
    }
    
    .subheader { 
        font-size: 15px; 
        color: white; 
        margin-bottom: 24px;
        font-family: 'Calibri', 'Arial', sans-serif;
    }
    
    .metric-label { 
        font-size: 11px; 
        color: white; 
        text-transform: uppercase; 
        letter-spacing: 0.1em; 
        margin-bottom: 10px;
        font-weight: 600;
        font-family: 'Calibri', 'Arial', sans-serif;
    }
    
    .metric-value { 
        font-size: 36px; 
        font-weight: 700;
        color: white;
        font-family: 'Calibri', 'Arial', sans-serif;
    }
    
    .metric-delta { 
        font-size: 12px; 
        color: white;
        margin-top: 8px;
        font-family: 'Calibri', 'Arial', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Data
partners_data = {
    "Partner": ["UNILAG", "NFC", "Brazil University", "UNIZIK"],
    "Status": ["Active", "Active", "At-Risk", "Inactive"],
    "Films Shipped": [8, 3, 0, 0],
    "Days Since Login": [0, 2, 21, 42],
    "Health Score": [92, 78, 38, 15],
    "Feature Adoption": [85, 72, 28, 0],
    "Users Active": [12, 5, 1, 0]
}

df_partners = pd.DataFrame(partners_data)

# Header
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="header">📊 Partner Health Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Real-time partner activation tracking. Spot trends, prevent churn.</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<p style="text-align: right; color: #707070; font-size: 12px; font-family: Calibri, Arial;">⏱️ {datetime.now().strftime("%H:%M")} WAT<br>📋 Sample Data</p>', unsafe_allow_html=True)

st.divider()

# KPI row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-label">🟢 Active Partners</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">2</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-delta">50% of 4 total</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-label">🎬 Films Shipped</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">11</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-delta">↓ Could be 32 if all active</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-label">⚠️ At-Risk</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">2</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-delta">Brazil + UNIZIK</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-label">💯 Avg Health</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">55.75</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-delta">↓ Declining</div>', unsafe_allow_html=True)

st.divider()

# Partner table
st.markdown("### 📋 Partner Status")

def get_status_emoji(status):
    if status == "Active":
        return "🟢"
    elif status == "At-Risk":
        return "🟡"
    else:
        return "🔴"

df_display = df_partners.copy()
df_display["Status"] = df_display["Status"].apply(lambda x: f"{get_status_emoji(x)} {x}")

st.dataframe(
    df_display[["Partner", "Status", "Films Shipped", "Health Score", "Days Since Login", "Feature Adoption"]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Onboarding Funnel (UNILAG)")
    st.markdown("How many UNILAG users progress through each activation stage")
    
    funnel_stages = ["Signed Up", "First Login", "Created First Film", "Regular User"]
    funnel_values = [12, 12, 12, 11]
    funnel_colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
    
    fig = go.Figure(go.Funnel(
        y=funnel_stages,
        x=funnel_values,
        marker=dict(color=funnel_colors, line=dict(color="#ffffff", width=2)),
        text=funnel_values,
        textposition="inside",
        hovertemplate="<b>%{y}</b><br>Users: %{x}<extra></extra>"
    ))
    
    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#000000", family="Calibri, Arial", size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 💪 Partner Health Scores")
    st.markdown("Overall engagement level (0-100 scale)")
    
    partners = ["UNILAG", "NFC", "Brazil Uni", "UNIZIK"]
    scores = [92, 78, 38, 15]
    colors = ["#96CEB4", "#FFD93D", "#FF9A76", "#EE5A6F"]
    
    fig2 = go.Figure(data=[
        go.Bar(
            y=partners,
            x=scores,
            orientation='h',
            marker=dict(color=colors, line=dict(color="#ffffff", width=2)),
            text=scores,
            textposition="inside",
            hovertemplate="<b>%{y}</b><br>Health Score: %{x}/100<extra></extra>"
        )
    ])
    
    fig2.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#000000", family="Calibri, Arial", size=12),
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)", range=[0, 100])
    )
    
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Adoption & Users
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Feature Adoption Rate")
    st.markdown("What % of available features each partner uses")
    
    adoption_colors = ["#96CEB4", "#FFD93D", "#FF9A76", "#EE5A6F"]
    
    fig3 = go.Figure(data=[
        go.Bar(
            x=["UNILAG", "NFC", "Brazil Uni", "UNIZIK"],
            y=[85, 72, 28, 0],
            marker=dict(color=adoption_colors, line=dict(color="#ffffff", width=1)),
            text=["85%", "72%", "28%", "0%"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Adoption: %{y}%<extra></extra>"
        )
    ])
    
    fig3.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#000000", family="Calibri, Arial", size=11),
        showlegend=False,
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)", range=[0, 100])
    )
    
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("### 👥 Active Users by Partner")
    st.markdown("Number of engaged team members per partner")
    
    user_colors = ["#96CEB4", "#FFD93D", "#FF9A76", "#EE5A6F"]
    
    fig4 = go.Figure(data=[
        go.Bar(
            x=["UNILAG", "NFC", "Brazil Uni", "UNIZIK"],
            y=[12, 5, 1, 0],
            marker=dict(color=user_colors, line=dict(color="#ffffff", width=1)),
            text=[12, 5, 1, 0],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Active Users: %{y}<extra></extra>"
        )
    ])
    
    fig4.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#000000", family="Calibri, Arial", size=11),
        showlegend=False,
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)")
    )
    
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Alerts
