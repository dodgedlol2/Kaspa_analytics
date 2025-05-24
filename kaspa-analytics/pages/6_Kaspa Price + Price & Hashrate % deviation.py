import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_price_data, load_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Data loading and processing
if 'price_df' not in st.session_state or 'price_genesis_date' not in st.session_state:
    try:
        st.session_state.price_df, st.session_state.price_genesis_date = load_price_data()
        # Load hashrate data for the oscillator
        st.session_state.hashrate_df, _ = load_data()
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

price_df = st.session_state.price_df
hashrate_df = st.session_state.hashrate_df
genesis_date = st.session_state.price_genesis_date

# Merge price and hashrate data
hashrate_df['Date'] = pd.to_datetime(hashrate_df['Date']).dt.normalize()
price_df['Date'] = pd.to_datetime(price_df['Date']).dt.normalize()
merged_df = pd.merge(price_df, hashrate_df[['Date', 'Hashrate_PH']], on='Date', how='left')
merged_df = merged_df.dropna(subset=['Price', 'Hashrate_PH']).copy()

# Calculate power laws
try:
    # Price power law
    a_price, b_price, r2_price = fit_power_law(price_df, y_col='Price')
    
    # Price/Hashrate ratio power law
    merged_df['Price_Hashrate_Ratio'] = merged_df['Price'] / merged_df['Hashrate_PH']
    merged_df['Days_Since_Genesis'] = (merged_df['Date'] - genesis_date).dt.days + 1
    a_ratio, b_ratio, r2_ratio = fit_power_law(merged_df, x_col='Days_Since_Genesis', y_col='Price_Hashrate_Ratio')
    
    # Calculate expected ratio and deviation
    merged_df['Expected_Ratio'] = a_ratio * np.power(merged_df['Days_Since_Genesis'], b_ratio)
    merged_df['Ratio_Deviation_Pct'] = ((merged_df['Price_Hashrate_Ratio'] - merged_df['Expected_Ratio']) / merged_df['Expected_Ratio']) * 100
    
except Exception as e:
    st.error(f"Failed to calculate power laws: {str(e)}")
    st.stop()

# Custom CSS - same styling as hashrate page for consistency
st.markdown("""
<style>
    /* Your existing CSS styles here */
    .oscillator-container {
        height: 150px !important;
        margin-top: -30px !important;
    }
    .combined-chart {
        height: 700px !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Price with Hashrate Ratio Oscillator</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container - adding oscillator toggle
    col_spacer_left, col1, col2, col3, col4, col5, spacer1, spacer2, spacer3, spacer4, spacer5, spacer6, spacer7, spacer8 = st.columns(
        [0.35, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 3]
    )

    with col1:
        st.markdown('<div class="control-label">Price Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Price Scale", y_scale_options,
                               index=1 if st.session_state.get("price_y_scale", True) else 0,
                               label_visibility="collapsed", key="price_y_scale_select")

    with col2:
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale_type = st.selectbox("Time Scale", x_scale_options,
                                index=0,
                                label_visibility="collapsed", key="price_x_scale_select")

    with col3:
        st.markdown('<div class="control-label">Period</div>', unsafe_allow_html=True)
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        if 'price_time_range' not in st.session_state:
            st.session_state.price_time_range = "All"
        time_range = st.selectbox("Time Range", time_ranges,
                                  index=time_ranges.index(st.session_state.price_time_range),
                                  label_visibility="collapsed", key="price_time_range_select")

    with col4:
        st.markdown('<div class="control-label">Power Law Fit</div>', unsafe_allow_html=True)
        power_law_options = ["Hide", "Show"]
        show_power_law = st.selectbox("Power Law Fit", power_law_options,
                                      index=0,
                                      label_visibility="collapsed", key="price_power_law_select")
    
    with col5:
        st.markdown('<div class="control-label">Show Oscillator</div>', unsafe_allow_html=True)
        oscillator_options = ["Hide", "Show"]
        show_oscillator = st.selectbox("Show Oscillator", oscillator_options,
                                      index=1,
                                      label_visibility="collapsed", key="oscillator_select")
    
    # Second divider - under the dropdown menus
    st.divider()

    # Filter data based on time range
    last_date = price_df['Date'].iloc[-1]
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
        start_date = price_df['Date'].iloc[0]

    filtered_df = merged_df[merged_df['Date'] >= start_date]

    # Create figure with secondary y-axis for oscillator
    fig = go.Figure()

    # Add price trace
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['Price'],
        mode='lines',
        name='Price (USD)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>'
    ))

    # Add power law fit if enabled
    if show_power_law == "Show":
        x_fit = filtered_df['days_from_genesis']
        y_fit = a_price * np.power(x_fit, b_price)
        fit_x = filtered_df['Date']

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2_price:.3f})',
            line=dict(color='#FFA726', dash='dot', width=2)
        ))

    # Add oscillator if enabled
    if show_oscillator == "Show":
        # Add zero line for oscillator
        fig.add_shape(
            type="line",
            x0=filtered_df['Date'].min(),
            y0=0,
            x1=filtered_df['Date'].max(),
            y1=0,
            line=dict(color="rgba(255,255,255,0.5)", width=1, dash="dot"),
            yref="y2"
        )

        # Add oscillator bars
        colors = ['rgba(0, 255, 0, 0.7)' if x >= 0 else 'rgba(255, 0, 0, 0.7)' for x in filtered_df['Ratio_Deviation_Pct']]
        fig.add_trace(go.Bar(
            x=filtered_df['Date'],
            y=filtered_df['Ratio_Deviation_Pct'],
            name='Deviation %',
            marker_color=colors,
            hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Deviation</b>: %{y:.1f}%<extra></extra>',
            yaxis="y2"
        ))

    # Update layout with secondary y-axis if oscillator is shown
    layout_kwargs = {
        "plot_bgcolor": '#262730',
        "paper_bgcolor": '#262730',
        "font_color": '#e0e0e0',
        "hovermode": 'x unified',
        "height": 700,
        "margin": dict(l=20, r=20, t=60, b=100),
        "yaxis": {
            "title": 'Price (USD)',
            "type": "log" if y_scale == "Log" else "linear",
            "showgrid": True,
            "gridwidth": 1,
            "gridcolor": 'rgba(255, 255, 255, 0.1)',
            "minor": dict(ticklen=6, gridcolor='rgba(255, 255, 255, 0.05)', gridwidth=0.5),
            "linecolor": '#3A3C4A',
            "zerolinecolor": '#3A3C4A'
        },
        "xaxis": {
            "title": "Date",
            "rangeslider": dict(visible=True, thickness=0.1, bgcolor='#262730', bordercolor="#3A3C4A", borderwidth=1),
            "type": "log" if x_scale_type == "Log" else None,
            "showgrid": True,
            "gridwidth": 1,
            "gridcolor": 'rgba(255, 255, 255, 0.1)',
            "minor": dict(ticklen=6, gridcolor='rgba(255, 255, 255, 0.05)', gridwidth=0.5),
            "linecolor": '#3A3C4A',
            "zerolinecolor": '#3A3C4A'
        },
        "legend": dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(38, 39, 48, 0.8)'
        ),
        "hoverlabel": dict(
            bgcolor='#262730',
            bordercolor='#3A3C4A',
            font_color='#e0e0e0'
        )
    }

    if show_oscillator == "Show":
        layout_kwargs["yaxis2"] = {
            "title": "Deviation %",
            "overlaying": "y",
            "side": "right",
            "showgrid": False,
            "zeroline": True,
            "zerolinecolor": 'rgba(255,255,255,0.5)',
            "zerolinewidth": 1,
            "range": [min(filtered_df['Ratio_Deviation_Pct'].min(), -20), max(filtered_df['Ratio_Deviation_Pct'].max(), 20)],
            "fixedrange": True
        }

    fig.update_layout(**layout_kwargs)

    st.plotly_chart(fig, use_container_width=True, className="combined-chart")

# Stats
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    st.metric("Power-Law Slope", f"{b_price:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2_price:.3f}")
with cols[2]:
    current_deviation = merged_df['Ratio_Deviation_Pct'].iloc[-1]
    st.metric("Current Deviation", f"{current_deviation:.1f}%", 
              delta_color="inverse" if current_deviation < 0 else "normal")
with cols[3]:
    st.metric("Ratio Fit (R²)", f"{r2_ratio:.3f}")
with cols[4]:
    st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")
st.markdown('</div>', unsafe_allow_html=True)
