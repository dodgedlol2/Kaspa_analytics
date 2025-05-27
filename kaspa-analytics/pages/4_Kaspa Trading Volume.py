import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import load_volume_data, fit_power_law
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Custom CSS - matching the style of your hashrate page
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .st-emotion-cache-6qob1r, .sidebar-content { background-color: #262730 !important; }
    .title-spacing { padding-left: 40px; margin-bottom: 15px; }
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #262730 !important;
        border-radius: 10px !important;
        border: 1px solid #3A3C4A !important;
        padding: 15px !important;
    }
    div[data-testid="stMetric"] {
        background-color: #262730 !important;
        border: 1px solid #3A3C4A !important;
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
    .stMetric { margin: 5px !important; height: 100% !important; }
    h2 { color: #e0e0e0 !important; }
    .hovertext text.hovertext { fill: #e0e0e0 !important; }
    .range-slider .handle:after { background-color: #00FFCC !important; }
    .metrics-container {
        width: calc(100% - 40px) !important;
        margin-left: 20px !important;
        margin-right: 20px !important;
        margin-top: 10px !important;
        margin-bottom: 0px !important;
    }
    .control-label {
        font-size: 11px !important;
        color: #e0e0e0 !important;
        margin-bottom: 2px !important;
        white-space: nowrap;
    }
    .st-emotion-cache-1dp5vir {
        border-top: 2px solid #3A3C4A !important;
        margin-top: 1px !important;
        margin-bottom: 2px !important;
    }
    [data-baseweb="select"] {
        font-size: 12px !important;
    }
    [data-baseweb="select"] > div {
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid #3A3C4A !important;
        background-color: #262730 !important;
        transition: all 0.2s ease;
    }
    [data-baseweb="select"] > div:hover {
        border-color: #00FFCC !important;
    }
    [data-baseweb="select"] > div[aria-expanded="true"],
    [data-baseweb="select"] > div:focus-within {
        border-color: #00FFCC !important;
        box-shadow: 0 0 0 1px #00FFCC !important;
    }
    [role="option"] {
        font-size: 12px !important;
        padding: 8px 12px !important;
    }
    [role="option"]:hover {
        background-color: #3A3C4A !important;
    }
    [aria-selected="true"] {
        background-color: #00FFCC20 !important;
        color: #00FFCC !important;
    }
    div[role="combobox"] > div {
        font-size: 12px !important;
        color: #e0e0e0 !important;
    }
    .stSelectbox [data-baseweb="select"] > div:has(> div[aria-selected="true"]) {
        border-color: #00FFCC !important;
        background-color: #00FFCC10 !important;
    }
    .stSelectbox [data-baseweb="select"] > div:has(> div[aria-selected="true"]) > div {
        color: #00FFCC !important;
    }
    .delta-positive {
        color: #00FFCC !important;
    }
    .delta-negative {
        color: #FF5252 !important;
    }
</style>
""", unsafe_allow_html=True)

# Data loading
if 'volume_df' not in st.session_state:
    try:
        st.session_state.volume_df = load_volume_data()
    except Exception as e:
        st.error(f"Failed to load volume data: {str(e)}")
        st.stop()

volume_df = st.session_state.volume_df
volume_df['Date'] = pd.to_datetime(volume_df['Date']).dt.normalize()

# Calculate moving averages
volume_df['MA_30'] = volume_df['Volume_USD'].rolling(30).mean()
volume_df['MA_60'] = volume_df['Volume_USD'].rolling(60).mean()

# Calculate power law fit for the entire dataset
try:
    a, b, r2 = fit_power_law(volume_df, y_col='Volume_USD')
except Exception as e:
    st.error(f"Failed to calculate power law: {str(e)}")
    st.stop()

# Calculate rolling power law parameters (for the second chart)
def calculate_rolling_power_law(df, window=365):
    results = []
    for i in range(window, len(df)):
        window_df = df.iloc[i-window:i]
        try:
            a, b, r2 = fit_power_law(window_df, y_col='Volume_USD')
            results.append({
                'Date': window_df['Date'].iloc[-1],
                'Slope': b,
                'R2': r2
            })
        except:
            pass
    return pd.DataFrame(results)

if 'rolling_power_law' not in st.session_state:
    try:
        st.session_state.rolling_power_law = calculate_rolling_power_law(volume_df)
    except Exception as e:
        st.error(f"Failed to calculate rolling power law: {str(e)}")
        st.stop()

rolling_power_law = st.session_state.rolling_power_law

# Calculate 30-day change in R2 if we have enough data
r2_change = None
r2_change_pct = None
if len(rolling_power_law) >= 30:
    current_r2 = rolling_power_law['R2'].iloc[-1]
    prev_r2 = rolling_power_law['R2'].iloc[-30]
    r2_change = current_r2 - prev_r2
    r2_change_pct = (r2_change / prev_r2) * 100

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Trading Volume Power Law Analysis</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container
    col_spacer_left, col1, col2, col3, col4, col5, col6, spacer1, spacer2, spacer3, spacer4, spacer5, spacer6, spacer7 = st.columns(
        [0.35, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1]
    )

    with col1:
        st.markdown('<div class="control-label">Volume Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Volume Scale", y_scale_options,
                               index=1,
                               label_visibility="collapsed", key="y_scale_select")

    with col2:
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale_type = st.selectbox("Time Scale", x_scale_options,
                                index=0,
                                label_visibility="collapsed", key="x_scale_select")

    with col3:
        st.markdown('<div class="control-label">Period</div>', unsafe_allow_html=True)
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        time_range = st.selectbox("Time Range", time_ranges,
                                  index=time_ranges.index("All"),
                                  label_visibility="collapsed", key="time_range_select")

    with col4:
        st.markdown('<div class="control-label">Power Law Fit</div>', unsafe_allow_html=True)
        power_law_options = ["Hide", "Show"]
        show_power_law = st.selectbox("Power Law Fit", power_law_options,
                                      index=0,  # Default to hidden
                                      label_visibility="collapsed", key="power_law_select")
    
    with col5:
        st.markdown('<div class="control-label">30D MA</div>', unsafe_allow_html=True)
        ma30_options = ["Hide", "Show"]
        show_ma30 = st.selectbox("30D MA", ma30_options,
                                 index=0,  # Default to hidden
                                 label_visibility="collapsed", key="ma30_select")
    
    with col6:
        st.markdown('<div class="control-label">60D MA</div>', unsafe_allow_html=True)
        ma60_options = ["Hide", "Show"]
        show_ma60 = st.selectbox("60D MA", ma60_options,
                                 index=0,  # Default to hidden
                                 label_visibility="collapsed", key="ma60_select")
    
    # Second divider - under the dropdown menus
    st.divider()

    # Filter data based on time range
    last_date = volume_df['Date'].iloc[-1]
    if time_range == "1W":
        start_date = last_date - timedelta(days=7)
    elif time_range == "1M":
        start_date = last_date - timedelta(days=30)
    elif time_range == "3M":
        start_date = last_date - timedelta(days=90)
    elif time_range == "6M":
        start_date = last_date - timedelta(days=180)
    elif time_range == "1Y":
        start_date = last_date - timedelta(days=365)
    else:
        start_date = volume_df['Date'].iloc[0]

    filtered_df = volume_df[volume_df['Date'] >= start_date]

    fig = go.Figure()

    if x_scale_type == "Log":
        x_values = filtered_df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
        tickformat = None
        hoverformat = None
    else:
        x_values = filtered_df['Date']
        x_title = "Date"
        tickformat = "%b %Y"
        hoverformat = "%b %d, %Y"

    # Add Volume trace
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Volume_USD'],
        mode='lines',
        name='Volume (USD)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Volume</b>: $%{y:,.0f}<extra></extra>',
        text=filtered_df['Date']
    ))

    # Add Price trace (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Price'],
        mode='lines',
        name='Price (USD)',
        line=dict(color='rgba(150, 150, 150, 0.7)', width=1.2),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>',
        text=filtered_df['Date'],
        yaxis='y2'
    ))

    # Add moving averages if enabled
    if show_ma30 == "Show":
        fig.add_trace(go.Scatter(
            x=x_values,
            y=filtered_df['MA_30'],
            mode='lines',
            name='30D MA Volume',
            line=dict(color='#FFA726', width=2),
            hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>30D MA Volume</b>: $%{y:,.0f}<extra></extra>',
            text=filtered_df['Date']
        ))

    if show_ma60 == "Show":
        fig.add_trace(go.Scatter(
            x=x_values,
            y=filtered_df['MA_60'],
            mode='lines',
            name='60D MA Volume',
            line=dict(color='#FF5252', width=2),
            hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>60D MA Volume</b>: $%{y:,.0f}<extra></extra>',
            text=filtered_df['Date']
        ))

    if show_power_law == "Show":
        x_fit = filtered_df['days_from_genesis']
        y_fit = a * np.power(x_fit, b)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2:.3f})',
            line=dict(color='#FFA726', dash='dot', width=2)
        ))

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

    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=700,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Volume (USD)',
        xaxis_title=x_title,
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.1,
                bgcolor='#262730',
                bordercolor="#3A3C4A",
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
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
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
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A',
            color='#00FFCC'
        ),
        yaxis2=dict(
            title='Price (USD)',
            overlaying='y',
            side='right',
            type="log" if y_scale == "Log" else "linear",
            showgrid=False,
            linecolor='rgba(150, 150, 150, 0.5)',
            zeroline=False,
            color='rgba(150, 150, 150, 0.7)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(38, 39, 48, 0.8)'
        ),
        hoverlabel=dict(
            bgcolor='#262730',
            bordercolor='#3A3C4A',
            font_color='#e0e0e0'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# Stats
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(4)
with cols[0]:
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1]:
    if r2_change is not None:
        delta_color = "delta-positive" if r2_change >= 0 else "delta-negative"
        delta_text = f"{r2_change_pct:.1f}% (30D)"
        st.metric("Model Fit (R²)", 
                 f"{r2:.3f}", 
                 delta=delta_text,
                 delta_color=("normal" if r2_change >= 0 else "inverse"))
    else:
        st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2]:
    st.metric("Current Volume", f"${volume_df['Volume_USD'].iloc[-1]:,.0f}")
with cols[3]:
    st.metric("Current Price", f"${volume_df['Price'].iloc[-1]:.4f}")
st.markdown('</div>', unsafe_allow_html=True)

# ====== POWER LAW TRENDS CHART ======
st.markdown('<div class="title-spacing"><h2>Power Law Parameter Trends</h2></div>', unsafe_allow_html=True)
st.divider()

# Create the trends chart
trend_fig = go.Figure()

# Add Slope trace
trend_fig.add_trace(go.Scatter(
    x=rolling_power_law['Date'],
    y=rolling_power_law['Slope'],
    mode='lines',
    name='Slope (b)',
    line=dict(color='#00FFCC', width=2),
    hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Slope</b>: %{y:.3f}<extra></extra>',
    yaxis='y'
))

# Add R² trace (secondary y-axis)
trend_fig.add_trace(go.Scatter(
    x=rolling_power_law['Date'],
    y=rolling_power_law['R2'],
    mode='lines',
    name='R²',
    line=dict(color='#FFA726', width=2),
    hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>R²</b>: %{y:.3f}<extra></extra>',
    yaxis='y2'
))

trend_fig.update_layout(
    plot_bgcolor='#262730',
    paper_bgcolor='#262730',
    font_color='#e0e0e0',
    hovermode='x unified',
    height=500,
    margin=dict(l=20, r=20, t=60, b=100),
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        linecolor='#3A3C4A',
        zerolinecolor='#3A3C4A',
        title='Date'
    ),
    yaxis=dict(
        title='Slope (b)',
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        linecolor='#3A3C4A',
        zerolinecolor='#3A3C4A',
        color='#00FFCC'
    ),
    yaxis2=dict(
        title='R²',
        overlaying='y',
        side='right',
        showgrid=False,
        range=[0, 1],  # R² is always between 0 and 1
        linecolor='#3A3C4A',
        zeroline=False,
        color='#FFA726'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor='rgba(38, 39, 48, 0.8)'
    ),
    hoverlabel=dict(
        bgcolor='#262730',
        bordercolor='#3A3C4A',
        font_color='#e0e0e0'
    )
)

st.plotly_chart(trend_fig, use_container_width=True)
