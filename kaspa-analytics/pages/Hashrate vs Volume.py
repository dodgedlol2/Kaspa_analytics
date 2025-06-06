import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data, load_volume_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Custom CSS - matching the style of your other pages
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
if 'df' not in st.session_state or 'genesis_date' not in st.session_state:
    try:
        st.session_state.df, st.session_state.genesis_date = load_data()
    except Exception as e:
        st.error(f"Failed to load hashrate data: {str(e)}")
        st.stop()

if 'volume_df' not in st.session_state:
    try:
        st.session_state.volume_df = load_volume_data()
    except Exception as e:
        st.error(f"Failed to load volume data: {str(e)}")
        st.stop()

df = st.session_state.df
genesis_date = st.session_state.genesis_date
volume_df = st.session_state.volume_df

# Merge data
df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
volume_df['Date'] = pd.to_datetime(volume_df['Date']).dt.normalize()

merged_df = pd.merge(
    df[['Date', 'Hashrate_PH']],
    volume_df[['Date', 'Volume_USD']],
    on='Date',
    how='inner'
).dropna()

# Calculate days since genesis
merged_df['Days_Since_Genesis'] = (merged_df['Date'] - genesis_date).dt.days + 1

# Create color gradient for last 7 points (teal to purple)
last_7 = merged_df.tail(7).copy()
purple_gradient = ['#00FFCC', '#40E0D0', '#80C0FF', '#A080FF', '#C040FF', '#E000FF', '#FF00FF']
last_7['color'] = purple_gradient

# Calculate power law fit
try:
    a, b, r2 = fit_power_law(merged_df, x_col='Hashrate_PH', y_col='Volume_USD')
except Exception as e:
    st.error(f"Failed to calculate power law: {str(e)}")
    st.stop()

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Hashrate vs Trading Volume Analysis</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container
    col_spacer_left, col1, col2, col3, col4, col5, col6, spacer1, spacer2, spacer3, spacer4 = st.columns(
        [0.35, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 3]
    )

    with col1:
        st.markdown('<div class="control-label">Volume Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Volume Scale", y_scale_options,
                               index=1,
                               label_visibility="collapsed", key="y_scale_select")

    with col2:
        st.markdown('<div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale_type = st.selectbox("Hashrate Scale", x_scale_options,
                                index=1,
                                label_visibility="collapsed", key="x_scale_select")

    with col3:
        st.markdown('<div class="control-label">Power Law Fit</div>', unsafe_allow_html=True)
        power_law_options = ["Hide", "Show"]
        show_power_law = st.selectbox("Power Law Fit", power_law_options,
                                      index=1,
                                      label_visibility="collapsed", key="power_law_select")
    
    with col4:
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        time_scale_options = ["Linear", "Log"]
        time_scale = st.selectbox("Time Scale", time_scale_options,
                                  index=0,
                                  label_visibility="collapsed", key="time_scale_select")
    
    # Second divider - under the dropdown menus
    st.divider()

    # Create the main figure
    fig = go.Figure()

    # Add scatter trace for all points (original teal color)
    fig.add_trace(go.Scatter(
        x=merged_df['Hashrate_PH'],
        y=merged_df['Volume_USD'],
        mode='markers',
        name='Volume vs Hashrate',
        marker=dict(
            color='#00FFCC',
            size=8,
            opacity=0.7,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hovertemplate='<b>Hashrate</b>: %{x:.2f} PH/s<br><b>Volume</b>: $%{y:,.0f}<br><b>Date</b>: %{text}<extra></extra>',
        text=merged_df['Date'].dt.strftime('%Y-%m-%d')
    ))

    # Add colored scatter trace for last 7 points (teal to purple gradient)
    for i, row in last_7.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Hashrate_PH']],
            y=[row['Volume_USD']],
            mode='markers',
            name=f"Recent ({row['Date'].strftime('%Y-%m-%d')})" if i == last_7.index[-1] else None,
            marker=dict(
                color=row['color'],
                size=12,
                opacity=0.9,
                line=dict(width=1.5, color='DarkSlateGrey')
            ),
            hovertemplate='<b>Hashrate</b>: %{x:.2f} PH/s<br><b>Volume</b>: $%{y:,.0f}<br><b>Date</b>: %{text}<extra></extra>',
            text=[row['Date'].strftime('%Y-%m-%d')],
            showlegend=False
        ))

    if show_power_law == "Show":
        # Generate fitted values
        x_fit = np.linspace(merged_df['Hashrate_PH'].min(), merged_df['Hashrate_PH'].max(), 100)
        y_fit = a * np.power(x_fit, b)
        
        fig.add_trace(go.Scatter(
            x=x_fit,
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2:.3f})',
            line=dict(color='#FFA726', dash='dot', width=2)
        ))

        # Add deviation bands
        fig.add_trace(go.Scatter(
            x=x_fit,
            y=y_fit * 0.4,
            mode='lines',
            name='-60% Deviation',
            line=dict(color='rgba(255, 255, 255, 0.5)', dash='dot', width=1),
            hoverinfo='skip',
            fill=None
        ))
        fig.add_trace(go.Scatter(
            x=x_fit,
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
        hovermode='closest',
        height=600,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Trading Volume (USD)',
        xaxis_title='Hashrate (PH/s)',
        xaxis=dict(
            type="log" if x_scale_type == "Log" else "linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            minor=dict(
                ticklen=6,
                gridcolor='rgba(255, 255, 255, 0.05)',
                gridwidth=0.5
            ),
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
            zerolinecolor='#3A3C4A'
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

    # ====== RATIO CHART ======
    st.markdown('<div class="title-spacing"><h4>Volume/Hashrate Ratio</h4></div>', unsafe_allow_html=True)
    
    # Calculate ratio
    merged_df['Volume_Hashrate_Ratio'] = merged_df['Volume_USD'] / merged_df['Hashrate_PH']
    
    # Calculate power law for ratio vs time
    try:
        a_ratio_time, b_ratio_time, r2_ratio_time = fit_power_law(
            merged_df, 
            x_col='Days_Since_Genesis', 
            y_col='Volume_Hashrate_Ratio'
        )
    except Exception as e:
        st.error(f"Failed to calculate ratio power law: {str(e)}")
        st.stop()
    
    ratio_fig = go.Figure()
    
    # Determine x-axis values based on time scale selection
    if time_scale == "Log":
        x_values = merged_df['Days_Since_Genesis']
        x_title = 'Days Since Genesis (Log Scale)'
        hover_template = '<b>Days</b>: %{x:.1f}<br><b>Date</b>: %{customdata}<br><b>Ratio</b>: %{y:.2f}<extra></extra>'
    else:
        x_values = merged_df['Date']
        x_title = 'Date'
        hover_template = '<b>Date</b>: %{x|%Y-%m-%d}<br><b>Ratio</b>: %{y:.2f}<extra></extra>'
    
    # Main ratio line
    ratio_fig.add_trace(go.Scatter(
        x=x_values,
        y=merged_df['Volume_Hashrate_Ratio'],
        mode='lines+markers',
        name='Volume/Hashrate Ratio',
        line=dict(color='#00FFCC', width=2),
        marker=dict(size=5, color='#00FFCC'),
        hovertemplate=hover_template,
        customdata=merged_df['Date'].dt.strftime('%Y-%m-%d')
    ))
    
    # Add colored markers for last 7 points
    for i, row in last_7.iterrows():
        x_val = row['Days_Since_Genesis'] if time_scale == "Log" else row['Date']
        ratio_fig.add_trace(go.Scatter(
            x=[x_val],
            y=[row['Volume_Hashrate_Ratio']],
            mode='markers',
            marker=dict(
                color=row['color'],
                size=8,
                line=dict(width=1.5, color='DarkSlateGrey')
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add power law fit if enabled
    if show_power_law == "Show":
        # Generate fitted values for ratio chart
        if time_scale == "Log":
            x_fit_ratio = np.logspace(
                np.log10(merged_df['Days_Since_Genesis'].min()), 
                np.log10(merged_df['Days_Since_Genesis'].max()), 
                100
            )
            y_fit_ratio = a_ratio_time * np.power(x_fit_ratio, b_ratio_time)
            
            ratio_fig.add_trace(go.Scatter(
                x=x_fit_ratio,
                y=y_fit_ratio,
                mode='lines',
                name=f'Ratio Power-Law Fit (R²={r2_ratio_time:.3f})',
                line=dict(color='#FFA726', dash='dot', width=2)
            ))
        else:
            # For linear time scale, use date numeric values but display as dates
            date_numeric = (merged_df['Date'] - merged_df['Date'].min()).dt.days + 1
            x_fit_ratio = np.linspace(1, date_numeric.max(), 100)
            y_fit_ratio = a_ratio_time * np.power(x_fit_ratio, b_ratio_time)
            
            # Convert numeric days back to dates
            fit_dates = merged_df['Date'].min() + pd.to_timedelta(x_fit_ratio - 1, unit='D')
            
            ratio_fig.add_trace(go.Scatter(
                x=fit_dates,
                y=y_fit_ratio,
                mode='lines',
                name=f'Ratio Power-Law Fit (R²={r2_ratio_time:.3f})',
                line=dict(color='#FFA726', dash='dot', width=2)
            ))
    
    ratio_fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=250,
        margin=dict(l=20, r=20, t=30, b=50),
        yaxis_title='Volume/Hashrate Ratio (USD/PH/s)',
        xaxis_title=x_title,
        xaxis=dict(
            type="log" if time_scale == "Log" else "linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
        ),
        yaxis=dict(
            type="linear",  # Ratio is better visualized on linear scale
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
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
    
    st.plotly_chart(ratio_fig, use_container_width=True)

# Stats
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1]:
    st.metric("Volume-HR Fit (R²)", f"{r2:.3f}")
with cols[2]:
    st.metric("Ratio-Time Slope", f"{b_ratio_time:.3f}")
with cols[3]:
    st.metric("Ratio-Time Fit (R²)", f"{r2_ratio_time:.3f}")
with cols[4]:
    st.metric("Current Ratio", f"${merged_df['Volume_Hashrate_Ratio'].iloc[-1]:.2f}/PH/s")
st.markdown('</div>', unsafe_allow_html=True)
