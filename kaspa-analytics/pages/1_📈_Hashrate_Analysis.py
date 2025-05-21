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

# Custom CSS for unified styling
st.markdown("""
<style>
    /* Main background color */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Control block styling */
    .control-block {
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid #2b3137;
        background-color: #1a1e25;
        margin-right: 15px;
        min-width: 160px;
        height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .title-spacing {
        padding-left: 40px;
        margin-bottom: 15px;
    }
    
    .control-label {
        font-size: 13px !important;
        margin-bottom: 6px !important;
        white-space: nowrap;
        font-weight: 500;
        color: #e0e0e0 !important;
    }
    
    .stToggle {
        width: 100%;
    }
    
    .stToggle button {
        width: 100% !important;
        font-size: 12px !important;
    }
    
    .controls-wrapper {
        padding-top: 11px;
    }
    
    .main-container {
        padding: 25px;
    }
    
    .plotly-rangeslider {
        height: 80px !important;
    }
    
    /* Main chart container styling */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1a1e25 !important;
        border-radius: 10px !important;
        border: 1px solid #2b3137 !important;
        padding: 15px !important;
    }
    
    /* Metric cards styling */
    div[data-testid="stMetric"] {
        background-color: #1a1e25 !important;
        border: 1px solid #2b3137 !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
    }
    
    div[data-testid="stMetricValue"] > div {
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #00FFCC !important;
    }
    
    div[data-testid="stMetricLabel"] > div {
        font-size: 14px !important;
        opacity: 0.8 !important;
        color: #e0e0e0 !important;
    }
    
    .stMetric {
        margin: 5px !important;
        height: 100% !important;
    }
    
    /* Title styling */
    h2 {
        color: #e0e0e0 !important;
    }
    
    /* Toggle button styling */
    .st-bd {
        background-color: #1a1e25 !important;
    }
    
    .st-cg {
        background-color: #00FFCC !important;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #1a1e25 !important;
        color: #00FFCC !important;
        border: 1px solid #2b3137 !important;
    }
    
    .stButton button:hover {
        background-color: #2b3137 !important;
        color: #00FFCC !important;
        border: 1px solid #00FFCC !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    # Create columns for title and controls
    title_col, control_col = st.columns([2, 8])

    with title_col:
        st.markdown('<div class="title-spacing"><h2>Kaspa Hashrate</h2></div>', unsafe_allow_html=True)

    with control_col:
        st.markdown('<div class="controls-wrapper">', unsafe_allow_html=True)
        cols = st.columns([1.5, 1.5, 1.5, 1.5, 3])

        with cols[0]:
            with st.container():
                st.markdown('<div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
                y_scale = st.toggle("Linear/Log", value=True, key="y_scale")
                y_scale = "Log" if y_scale else "Linear"

        with cols[1]:
            with st.container():
                st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
                x_scale_type = st.toggle("Linear/Log", value=False, key="x_scale")
                x_scale_type = "Log" if x_scale_type else "Linear"

        with cols[2]:
            with st.container():
                st.markdown('<div class="control-label">Deviation Bands</div>', unsafe_allow_html=True)
                show_bands = st.toggle("Hide/Show", value=False, key="bands_toggle")

        with cols[3]:
            with st.container():
                st.markdown('<div class="control-label">Auto Scale</div>', unsafe_allow_html=True)
                auto_scale = st.toggle("Off/On", value=True, key="auto_scale")

        st.markdown('</div>', unsafe_allow_html=True)

    # Create figure with unified color scheme
    fig = go.Figure()

    # Determine x-axis values based on scale type
    max_days = df['days_from_genesis'].max() + 300
    if x_scale_type == "Log":
        x_values = df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
        tickformat = None
        hoverformat = None
    else:
        x_values = df['Date']
        x_title = "Date"
        tickformat = "%b %Y"
        hoverformat = "%b %d, %Y"

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

    # Power-law fit extended 300 days into future
    x_fit = np.linspace(df['days_from_genesis'].min(), max_days, 300)
    y_fit = a * np.power(x_fit, b)

    if x_scale_type == "Log":
        fit_x = x_fit
    else:
        fit_x = [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2:.3f})',
        line=dict(color='#FFA726', dash='dot', width=2)
    ))

    # Deviation bands
    if show_bands:
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='-60% Deviation',
            line=dict(color='rgba(255, 255, 255, 0.5)', dash='dot', width=1),
            hoverinfo='skip',
            fill=None
        ))
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='+120% Deviation',
            line=dict(color='rgba(255, 255, 255, 0.5)', dash='dot', width=1),
            hoverinfo='skip',
            fill='tonexty',
            fillcolor='rgba(100, 100, 100, 0.2)'
        ))

    # Enhanced layout
    fig.update_layout(
        plot_bgcolor='#1a1e25',
        paper_bgcolor='#1a1e25',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=700,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Hashrate (PH/s)',
        xaxis_title=x_title,
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.1,
                bgcolor='#1a1e25',
                bordercolor="#2b3137",
                borderwidth=1
            ),
            type="log" if x_scale_type == "Log" else None,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            minor=dict(
                ticklen=6,
                gridcolor='rgba(255, 255, 255, 0.05)',
                gridwidth=0.5
            ),
            tickformat=tickformat,
            range=[None, max_days] if x_scale_type == "Log" else 
                  [df['Date'].min(), genesis_date + pd.Timedelta(days=max_days)],
            linecolor='#2b3137',
            zerolinecolor='#2b3137'
        ),
        yaxis=dict(
            type="log" if y_scale == "Log" else "linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            minor=dict(
                ticklen=6,
                gridcolor='rgba(255, 255, 255, 0.05)',
                gridwidth=0.5
            ),
            linecolor='#2b3137',
            zerolinecolor='#2b3137',
            fixedrange=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(26, 30, 37, 0.8)'
        ),
        hoverlabel=dict(
            bgcolor='#1a1e25',
            bordercolor='#2b3137',
            font_color='#e0e0e0'
        )
    )

    # JavaScript for professional auto-scaling
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const plotElement = document.querySelector('.plotly-graph-div.js-plotly-plot');
        if (plotElement) {
            // Store original ranges for reset
            let originalXRange = null;
            let originalYRange = null;
            
            // Get initial ranges
            Plotly.relayout(plotElement).then(function(gd) {
                originalXRange = [gd.layout.xaxis.range[0], gd.layout.xaxis.range[1]];
                originalYRange = [gd.layout.yaxis.range[0], gd.layout.yaxis.range[1]];
            });
            
            // Auto-scaling function
            function autoScaleYAxis() {
                if (!%s) return; // Skip if auto-scale is off
                
                Plotly.relayout(plotElement).then(function(gd) {
                    const xRange = gd.layout.xaxis.range;
                    const fullData = gd.data[0]; // Main hashrate data
                    
                    // Convert xRange to indices
                    let startIdx, endIdx;
                    if (fullData.x instanceof Array) {
                        // Date-based x-axis
                        startIdx = fullData.x.findIndex(x => new Date(x) >= new Date(xRange[0]));
                        endIdx = fullData.x.findIndex(x => new Date(x) >= new Date(xRange[1]));
                    } else {
                        // Numeric x-axis
                        startIdx = Math.max(0, Math.floor(xRange[0]));
                        endIdx = Math.min(fullData.x.length-1, Math.ceil(xRange[1]));
                    }
                    
                    if (startIdx === -1) startIdx = 0;
                    if (endIdx === -1) endIdx = fullData.x.length-1;
                    
                    // Get y-values in visible range
                    const visibleY = fullData.y.slice(startIdx, endIdx+1);
                    if (visibleY.length === 0) return;
                    
                    // Calculate new y-range with 10% padding
                    const yMin = Math.min(...visibleY);
                    const yMax = Math.max(...visibleY);
                    const padding = (yMax - yMin) * 0.1;
                    
                    const newYRange = [
                        Math.max(0, yMin - padding),
                        yMax + padding
                    ];
                    
                    // Apply new range
                    Plotly.relayout(plotElement, {
                        'yaxis.range': newYRange,
                        'yaxis.autorange': false
                    });
                });
            }
            
            // Reset function
            window.resetZoom = function() {
                Plotly.relayout(plotElement, {
                    'xaxis.range': originalXRange,
                    'yaxis.range': originalYRange,
                    'yaxis.autorange': false
                });
            }
            
            // Set up event listeners
            plotElement.on('plotly_relayout', function(eventdata) {
                // Check if user zoomed or panned
                if (eventdata['xaxis.range[0]'] !== undefined || 
                    eventdata['xaxis.range[1]'] !== undefined) {
                    autoScaleYAxis();
                }
            });
        }
    });
    </script>
    """ % ('true' if auto_scale else 'false'), unsafe_allow_html=True)

    # Display the chart and controls
    chart_container = st.container()
    with chart_container:
        st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})
        
        # Add reset button
        reset_col, _ = st.columns([1, 9])
        with reset_col:
            if st.button('Reset View', key='reset_zoom'):
                st.markdown("""
                <script>
                if (typeof resetZoom === 'function') {
                    resetZoom();
                }
                </script>
                """, unsafe_allow_html=True)


# Stats in cards with matching styling
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
cols = st.columns(3)
with cols[0]:
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
