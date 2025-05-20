import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data

st.set_page_config(layout="wide")

# Custom CSS for professional styling
st.markdown("""
<style>
    .chart-wrapper {
        position: relative;
    }
    .scale-controls {
        position: absolute;
        z-index: 100;
        background: rgba(30, 30, 30, 0.7);
        border-radius: 4px;
        padding: 4px;
    }
    .y-scale-controls {
        top: 10px;
        left: 10px;
    }
    .x-scale-controls {
        bottom: 10px;
        right: 10px;
    }
    .scale-btn {
        border: 1px solid #636e72 !important;
        border-radius: 4px !important;
        padding: 0.15rem 0.5rem !important;
        font-size: 0.8rem !important;
        background-color: transparent !important;
        color: white !important;
        min-width: 24px !important;
        height: 24px !important;
        margin: 0 2px !important;
    }
    .scale-btn:hover {
        background-color: rgba(45, 52, 54, 0.9) !important;
        border-color: #00FFCC !important;
    }
    .scale-btn.active {
        background-color: rgba(0, 255, 204, 0.2) !important;
        border-color: #00FFCC !important;
    }
    .scale-btn-tooltip {
        visibility: hidden;
        width: 120px;
        background-color: #2d3436;
        color: #fff;
        text-align: center;
        border-radius: 4px;
        padding: 4px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
    }
    .scale-btn-container:hover .scale-btn-tooltip {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

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

# Initialize session state for scale toggles
if 'y_scale_type' not in st.session_state:
    st.session_state.y_scale_type = "log"
if 'x_scale_type' not in st.session_state:
    st.session_state.x_scale_type = "linear"
if 'show_bands' not in st.session_state:
    st.session_state.show_bands = False

# Callback functions for button clicks
def set_y_scale(scale_type):
    st.session_state.y_scale_type = scale_type

def set_x_scale(scale_type):
    st.session_state.x_scale_type = scale_type

# ====== PROFESSIONAL CHART CONTAINER ======
with st.container(border=True):
    st.markdown("### Kaspa Hashrate")
    
    # Create a wrapper div for the chart and controls
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    
    # Create figure with enhanced grid
    fig = go.Figure()

    # Determine x-axis values based on scale type
    if st.session_state.x_scale_type == "log":
        x_values = df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
    else:
        x_values = df['Date']
        x_title = "Date"

    # Main trace
    fig.add_trace(go.Scatter(
        x=x_values,
        y=df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=df['Date']
    ))

    # Power-law fit (always shown)
    x_fit = np.linspace(df['days_from_genesis'].min(), df['days_from_genesis'].max(), 100)
    y_fit = a * np.power(x_fit, b)
    
    if st.session_state.x_scale_type == "log":
        fit_x = x_fit
    else:
        fit_x = [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]
    
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2:.3f})',
        line=dict(color='orange', dash='dot', width=1.8)
    ))
    
    # Deviation bands (only shown when toggled)
    if st.session_state.show_bands:
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='-60%',
            line=dict(color='rgba(255,165,0,0.8)', dash='dot', width=1.2),
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='+120%',
            line=dict(color='rgba(255,165,0,0.8)', dash='dot', width=1.2),
            hoverinfo='skip'
        ))

    # Enhanced layout with proper axis type handling
    layout_updates = {
        'template': 'plotly_dark',
        'hovermode': 'x unified',
        'height': 600,
        'margin': dict(l=20, r=20, t=40, b=40),
        'yaxis': {
            'title': 'PH/s',
            'type': st.session_state.y_scale_type,
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': 'rgba(100,100,100,0.2)',
            'minor': {
                'ticklen': 6,
                'gridcolor': 'rgba(100,100,100,0.1)',
                'gridwidth': 0.5
            }
        },
        'xaxis': {
            'title': x_title,
            'type': st.session_state.x_scale_type if st.session_state.x_scale_type == "log" else "date",
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': 'rgba(100,100,100,0.2)',
            'minor': {
                'ticklen': 6,
                'gridcolor': 'rgba(100,100,100,0.1)',
                'gridwidth': 0.5
            }
        },
        'legend': {
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1.02,
            'xanchor': "right",
            'x': 1,
            'font': dict(size=10)
        }
    }
    
    fig.update_layout(**layout_updates)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Y-axis scale controls (top-left)
    st.markdown(f"""
    <div class="scale-controls y-scale-controls">
        <div class="scale-btn-container" style="display: inline-block; position: relative;">
            <button class="scale-btn {'active' if st.session_state.y_scale_type == 'linear' else ''}" 
                    onclick="(function() {{ const event = new CustomEvent('setYScale', {{ detail: 'linear' }}); window.dispatchEvent(event); }})()">A</button>
            <span class="scale-btn-tooltip">Autoscale/Linear</span>
        </div>
        <div class="scale-btn-container" style="display: inline-block; position: relative;">
            <button class="scale-btn {'active' if st.session_state.y_scale_type == 'log' else ''}" 
                    onclick="(function() {{ const event = new CustomEvent('setYScale', {{ detail: 'log' }}); window.dispatchEvent(event); }})()">L</button>
            <span class="scale-btn-tooltip">Logarithmic Scale</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # X-axis scale controls (bottom-right)
    st.markdown(f"""
    <div class="scale-controls x-scale-controls">
        <div class="scale-btn-container" style="display: inline-block; position: relative;">
            <button class="scale-btn {'active' if st.session_state.x_scale_type == 'linear' else ''}" 
                    onclick="(function() {{ const event = new CustomEvent('setXScale', {{ detail: 'linear' }}); window.dispatchEvent(event); }})()">A</button>
            <span class="scale-btn-tooltip">Autoscale/Linear</span>
        </div>
        <div class="scale-btn-container" style="display: inline-block; position: relative;">
            <button class="scale-btn {'active' if st.session_state.x_scale_type == 'log' else ''}" 
                    onclick="(function() {{ const event = new CustomEvent('setXScale', {{ detail: 'log' }}); window.dispatchEvent(event); }})()">L</button>
            <span class="scale-btn-tooltip">Logarithmic Scale</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close chart-wrapper

# Stats in minimal cards
cols = st.columns(3)
with cols[0].container(border=True):
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1].container(border=True):
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2].container(border=True):
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")

# JavaScript to handle button clicks
st.markdown("""
<script>
    // Handle custom events from buttons
    window.addEventListener('setYScale', function(e) {
        Streamlit.setComponentValue({y_scale_type: e.detail});
    });
    window.addEventListener('setXScale', function(e) {
        Streamlit.setComponentValue({x_scale_type: e.detail});
    });
    
    // Force rerun when buttons are clicked
    document.addEventListener('DOMContentLoaded', function() {
        const buttons = document.querySelectorAll('.scale-btn');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                setTimeout(() => {
                    Streamlit.setComponentValue({forceRerun: Date.now()});
                }, 100);
            });
        });
    });
</script>
""", unsafe_allow_html=True)
