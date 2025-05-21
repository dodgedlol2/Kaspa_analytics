import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data

st.set_page_config(layout="wide")

# Data loading and processing
if 'df' not in st.session_state or 'genesis_date' not in st.session_state:
    try:
        st.session_state.df, st.session_state.genesis_date = load_data()
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

df = st.session_state.df
genesis_date = st.session_state.genesis_date

try:
    a, b, r2 = fit_power_law(df)
except Exception as e:
    st.error(f"Failed to calculate power law: {str(e)}")
    st.stop()

# Kaspa Brand Color Scheme (extracted from official logo/branding)
COLORS = {
    'primary': '#17B2A7',     # Kaspa's signature teal
    'primary_dark': '#0E8C84', # Darker teal for accents
    'background': '#0D1B2A',   # Deep navy-blue (darker than Kaspa's but complementary)
    'panel': '#1B263B',        # Dark slate with blue undertone
    'border': '#2C3A58',       # Medium slate-blue
    'secondary': '#E9C46A',    # Golden yellow (from Kaspa's gradient)
    'accent': '#F4A261',       # Orange accent (from Kaspa's gradient)
    'text': '#E0E1DD',         # Off-white text
    'success': '#2ECC71',      # Emerald green
    'grid': 'rgba(200, 213, 219, 0.1)'  # Light blueish grid
}

# Custom CSS with Kaspa branding
st.markdown(f"""
<style>
    /* Base styling */
    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
    }}
    
    /* Sidebar matching */
    .st-emotion-cache-6qob1r, .sidebar-content {{
        background-color: {COLORS['panel']} !important;
        border-right: 1px solid {COLORS['border']} !important;
    }}
    
    /* Control blocks */
    .control-block {{
        background-color: {COLORS['panel']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 12px;
        margin-right: 15px;
        height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    
    .control-label {{
        font-size: 13px !important;
        margin-bottom: 8px !important;
        color: {COLORS['text']} !important;
        font-weight: 500;
        letter-spacing: 0.5px;
    }}
    
    /* Toggle buttons */
    .stToggle button {{
        background-color: {COLORS['panel']} !important;
        border: 1px solid {COLORS['border']} !important;
        color: {COLORS['text']} !important;
    }}
    
    .stToggle button:hover {{
        border-color: {COLORS['primary']} !important;
    }}
    
    /* Main containers */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {COLORS['panel']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px;
        padding: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    /* Metrics cards */
    div[data-testid="stMetric"] {{
        background-color: {COLORS['panel']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 8px;
        padding: 20px !important;
    }}
    
    div[data-testid="stMetricValue"] > div {{
        font-size: 26px !important;
        font-weight: 700 !important;
        color: {COLORS['primary']} !important;
    }}
    
    div[data-testid="stMetricLabel"] > div {{
        font-size: 14px !important;
        color: {COLORS['text']} !important;
        opacity: 0.9 !important;
        letter-spacing: 0.3px;
    }}
    
    /* Titles */
    h2 {{
        color: {COLORS['primary']} !important;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 5px !important;
    }}
    
    /* Tooltips */
    .hovertext text.hovertext {{
        fill: {COLORS['text']} !important;
    }}
    
    /* Range slider */
    .plotly-rangeslider {{
        background-color: {COLORS['panel']} !important;
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['panel']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['primary_dark']};
        border-radius: 4px;
    }}
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    # Header with title and controls
    header_col1, header_col2 = st.columns([2, 8])
    
    with header_col1:
        st.markdown(f"""
        <div style="padding-left: 15px; margin-bottom: 10px;">
            <h2>Kaspa Hashrate</h2>
            <div style="color: {COLORS['text']}; opacity: 0.8; font-size: 14px;">
                Power-law growth analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        controls = st.columns([1.5, 1.5, 1.5, 4])
        
        with controls[0]:
            with st.container():
                st.markdown('<div class="control-label">HASHRATE SCALE</div>', unsafe_allow_html=True)
                y_scale = st.toggle("Linear/Log", value=True, key="y_scale", label_visibility="collapsed")
                y_scale = "Log" if y_scale else "Linear"
        
        with controls[1]:
            with st.container():
                st.markdown('<div class="control-label">TIME SCALE</div>', unsafe_allow_html=True)
                x_scale_type = st.toggle("Linear/Log", value=False, key="x_scale", label_visibility="collapsed")
                x_scale_type = "Log" if x_scale_type else "Linear"
        
        with controls[2]:
            with st.container():
                st.markdown('<div class="control-label">DEVIATION BANDS</div>', unsafe_allow_html=True)
                show_bands = st.toggle("Hide/Show", value=False, key="bands_toggle", label_visibility="collapsed")

    # Create the figure
    fig = go.Figure()

    # Axis configuration
    max_days = df['days_from_genesis'].max() + 300
    if x_scale_type == "Log":
        x_values = df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
        tickformat = None
    else:
        x_values = df['Date']
        x_title = "Date"
        tickformat = "%b %Y"

    # Main hashrate trace (using Kaspa's primary teal)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color=COLORS['primary'], width=2.8),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=df['Date']
    ))

    # Power-law fit (using Kaspa's golden yellow)
    x_fit = np.linspace(df['days_from_genesis'].min(), max_days, 300)
    y_fit = a * np.power(x_fit, b)
    fit_x = x_fit if x_scale_type == "Log" else [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2:.3f})',
        line=dict(color=COLORS['secondary'], dash='dot', width=2.5)
    ))

    # Deviation bands (using Kaspa's orange accent)
    if show_bands:
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='-60% Deviation',
            line=dict(color=f"rgba{(*[int(COLORS['accent'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)}, 0.3)", width=1),
            hoverinfo='skip',
            fill=None
        ))
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='+120% Deviation',
            line=dict(color=f"rgba{(*[int(COLORS['accent'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)}, 0.3)", width=1),
            hoverinfo='skip',
            fill='tonexty',
            fillcolor=f"rgba{(*[int(COLORS['primary'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)}, 0.1)"
        ))

    # Professional chart layout with Kaspa colors
    fig.update_layout(
        plot_bgcolor=COLORS['panel'],
        paper_bgcolor=COLORS['panel'],
        font_color=COLORS['text'],
        hovermode='x unified',
        height=700,
        margin=dict(l=50, r=50, t=80, b=80),
        yaxis_title='Hashrate (PH/s)',
        xaxis_title=x_title,
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.08,
                bgcolor=COLORS['panel'],
                bordercolor=COLORS['border'],
                borderwidth=1
            ),
            type="log" if x_scale_type == "Log" else None,
            showgrid=True,
            gridcolor=COLORS['grid'],
            gridwidth=1,
            linecolor=COLORS['border'],
            zerolinecolor=COLORS['border'],
            tickformat=tickformat
        ),
        yaxis=dict(
            type="log" if y_scale == "Log" else "linear",
            showgrid=True,
            gridcolor=COLORS['grid'],
            gridwidth=1,
            linecolor=COLORS['border'],
            zerolinecolor=COLORS['border'],
            minor=dict(
                ticklen=6,
                gridcolor=f"rgba{(*[int(COLORS['primary'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)}, 0.05)",
                gridwidth=0.5
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor=f"rgba{(*[int(COLORS['panel'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)}, 0.7)",
            bordercolor=COLORS['border'],
            borderwidth=1,
            font=dict(size=12)
        ),
        hoverlabel=dict(
            bgcolor=COLORS['panel'],
            bordercolor=COLORS['border'],
            font_size=12,
            font_color=COLORS['text']
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# Metrics row with Kaspa styling
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
metrics = st.columns(3)

with metrics[0]:
    st.metric(
        label="POWER-LAW SLOPE",
        value=f"{b:.3f}",
        help="Exponent in the power-law equation y = a*x^b"
    )

with metrics[1]:
    st.metric(
        label="MODEL FIT (R²)",
        value=f"{r2:.3f}",
        help="Coefficient of determination (0-1 scale)"
    )

with metrics[2]:
    st.metric(
        label="CURRENT HASHRATE",
        value=f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s",
        help="Network hashrate at last data point"
    )
