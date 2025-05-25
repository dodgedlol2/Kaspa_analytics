import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data, load_price_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Data loading and processing
if 'df' not in st.session_state or 'genesis_date' not in st.session_state:
    try:
        st.session_state.df, st.session_state.genesis_date = load_data()
        st.session_state.price_df, _ = load_price_data()
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

df = st.session_state.df
price_df = st.session_state.price_df
genesis_date = st.session_state.genesis_date

# Merge data and clean
df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
price_df['Date'] = pd.to_datetime(price_df['Date']).dt.normalize()
price_df = price_df.drop_duplicates('Date', keep='last')
merged_df = pd.merge(df, price_df[['Date', 'Price']], on='Date', how='left')

# Remove rows where either hashrate or price is missing
analysis_df = merged_df.dropna(subset=['Hashrate_PH', 'Price']).copy()

# Calculate days since genesis for log time scale
analysis_df['Days_Since_Genesis'] = (analysis_df['Date'] - genesis_date).dt.days + 1  # +1 to avoid log(0)

# Calculate power law for price vs hashrate relationship
try:
    a_relation, b_relation, r2_relation = fit_power_law(analysis_df, x_col='Hashrate_PH', y_col='Price')
    
    # Calculate expected price based on power law
    analysis_df['Expected_Price'] = a_relation * np.power(analysis_df['Hashrate_PH'], b_relation)
    
    # Calculate % deviation from expected price
    analysis_df['Price_Deviation_Pct'] = ((analysis_df['Price'] - analysis_df['Expected_Price']) / analysis_df['Expected_Price']) * 100
    
    # Create oscillator signal (smoothed deviation)
    analysis_df['Oscillator'] = analysis_df['Price_Deviation_Pct'].rolling(window=7, min_periods=1).mean()
except Exception as e:
    st.error(f"Failed to calculate power laws: {str(e)}")
    st.stop()

# Create color gradient for last 7 points (teal to purple)
last_7 = analysis_df.tail(7).copy()
purple_gradient = ['#00FFCC', '#40E0D0', '#80C0FF', '#A080FF', '#C040FF', '#E000FF', '#FF00FF']
last_7['color'] = purple_gradient

# Custom CSS - updated with oscillator-specific styling
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
    .oscillator-chart {
        margin-top: -30px !important;
        height: 250px !important;
    }
    .positive-deviation {
        color: #00FFCC !important;
    }
    .negative-deviation {
        color: #FF00FF !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Hashrate with Price Deviation Oscillator</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container
    col_spacer_left, col1, col2, col3, col4, spacer1, spacer2, spacer3, spacer4, spacer5, spacer6 = st.columns(
        [0.35, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 3]
    )

    with col1:
        st.markdown('<div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Hashrate Scale", y_scale_options,
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
        if 'time_range' not in st.session_state:
            st.session_state.time_range = "All"
        time_range = st.selectbox("Time Range", time_ranges,
                                  index=time_ranges.index(st.session_state.time_range),
                                  label_visibility="collapsed", key="time_range_select")
    
    with col4:
        st.markdown('<div class="control-label">Show Power Law</div>', unsafe_allow_html=True)
        show_power_law = st.selectbox("Show Power Law", ["Hide", "Show"],
                                      index=1,
                                      label_visibility="collapsed", key="power_law_select")
    
    # Second divider - under the dropdown menus
    st.divider()

    # Filter data based on time range
    last_date = analysis_df['Date'].iloc[-1]
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
        start_date = analysis_df['Date'].iloc[0]

    filtered_df = analysis_df[analysis_df['Date'] >= start_date]

    # Determine x-axis values
    if x_scale_type == "Log":
        x_values = filtered_df['Days_Since_Genesis']
        x_title = "Days Since Genesis (Log Scale)"
        tickformat = None
        hoverformat = None
    else:
        x_values = filtered_df['Date']
        x_title = "Date"
        tickformat = "%b %Y"
        hoverformat = "%b %d, %Y"

    # Create main figure
    fig = go.Figure()

    # Add hashrate trace (primary y-axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=filtered_df['Date']
    ))

    # Add price trace (secondary y-axis)
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

    if show_power_law == "Show":
        # Add expected price trace (secondary y-axis)
        fig.add_trace(go.Scatter(
            x=x_values,
            y=filtered_df['Expected_Price'],
            mode='lines',
            name='Expected Price (Power Law)',
            line=dict(color='#FFA726', dash='dot', width=2),
            hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Expected Price</b>: $%{y:.4f}<extra></extra>',
            text=filtered_df['Date'],
            yaxis='y2'
        ))

    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=500,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Hashrate (PH/s)',
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

    # ====== OSCILLATOR CHART ======
    st.markdown('<div class="title-spacing"><h4>Price Deviation Oscillator (% from Power Law)</h4></div>', unsafe_allow_html=True)
    
    oscillator_fig = go.Figure()
    
    # Add zero line
    oscillator_fig.add_shape(
        type="line",
        x0=x_values.iloc[0],
        x1=x_values.iloc[-1],
        y0=0,
        y1=0,
        line=dict(color="rgba(255, 255, 255, 0.5)", width=1, dash="dot"),
    )
    
    # Add overbought/oversold levels
    oscillator_fig.add_shape(
        type="line",
        x0=x_values.iloc[0],
        x1=x_values.iloc[-1],
        y0=50,
        y1=50,
        line=dict(color="rgba(255, 0, 0, 0.3)", width=1, dash="dot"),
    )
    oscillator_fig.add_shape(
        type="line",
        x0=x_values.iloc[0],
        x1=x_values.iloc[-1],
        y0=-50,
        y1=-50,
        line=dict(color="rgba(0, 255, 0, 0.3)", width=1, dash="dot"),
    )
    
    # Add oscillator trace (bar chart)
    oscillator_fig.add_trace(go.Bar(
        x=x_values,
        y=filtered_df['Price_Deviation_Pct'],
        name='Daily Deviation',
        marker=dict(
            color=np.where(filtered_df['Price_Deviation_Pct'] >= 0, 
                         'rgba(0, 255, 204, 0.7)', 
                         'rgba(255, 0, 255, 0.7)'),
            line=dict(
                width=0
            )
        ),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Deviation</b>: %{y:.1f}%<extra></extra>',
        text=filtered_df['Date']
    ))
    
    # Add smoothed oscillator line
    oscillator_fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Oscillator'],
        mode='lines',
        name='7D Avg Deviation',
        line=dict(color='#FFA726', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>7D Avg Deviation</b>: %{y:.1f}%<extra></extra>',
        text=filtered_df['Date']
    ))
    
    # Add colored markers for last 7 points
    last_7_filtered = filtered_df.tail(7)
    for i, row in last_7_filtered.iterrows():
        oscillator_fig.add_trace(go.Scatter(
            x=[x_values.loc[i]] if x_scale_type != "Log" else [row['Days_Since_Genesis']],
            y=[row['Price_Deviation_Pct']],
            mode='markers',
            marker=dict(
                color=purple_gradient[i % len(purple_gradient)],
                size=8,
                line=dict(width=1.5, color='DarkSlateGrey')
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    oscillator_fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=250,
        margin=dict(l=20, r=20, t=30, b=50),
        yaxis_title='Deviation (%)',
        xaxis_title=x_title,
        xaxis=dict(
            type="log" if x_scale_type == "Log" else None,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A',
            tickformat=tickformat
        ),
        yaxis=dict(
            type="linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A',
            range=[-100, 100]  # Fixed range for better comparison
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
        ),
        bargap=0
    )
    
    st.plotly_chart(oscillator_fig, use_container_width=True, className="oscillator-chart")

# Stats
current_deviation = analysis_df['Price_Deviation_Pct'].iloc[-1]
current_oscillator = analysis_df['Oscillator'].iloc[-1]

st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(6)
with cols[0]:
    st.metric("Current Hashrate", f"{analysis_df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
with cols[1]:
    st.metric("Current Price", f"${analysis_df['Price'].iloc[-1]:.4f}")
with cols[2]:
    st.metric("Expected Price", f"${analysis_df['Expected_Price'].iloc[-1]:.4f}")
with cols[3]:
    deviation_color = "positive-deviation" if current_deviation >= 0 else "negative-deviation"
    st.markdown(f'<div class="stMetric"><div data-testid="stMetricLabel" class="st-emotion-cache-1xw8zd6 e115fcil1"><div>Current Deviation</div></div><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e115fcil0"><div class="{deviation_color}">{current_deviation:.1f}%</div></div></div>', unsafe_allow_html=True)
with cols[4]:
    oscillator_color = "positive-deviation" if current_oscillator >= 0 else "negative-deviation"
    st.markdown(f'<div class="stMetric"><div data-testid="stMetricLabel" class="st-emotion-cache-1xw8zd6 e115fcil1"><div>7D Avg Oscillator</div></div><div data-testid="stMetricValue" class="st-emotion-cache-1xarl3l e115fcil0"><div class="{oscillator_color}">{current_oscillator:.1f}%</div></div></div>', unsafe_allow_html=True)
with cols[5]:
    st.metric("Power-Law R²", f"{r2_relation:.3f}")
st.markdown('</div>', unsafe_allow_html=True)
