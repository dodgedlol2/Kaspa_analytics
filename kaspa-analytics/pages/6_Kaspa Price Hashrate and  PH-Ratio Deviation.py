import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from utils import load_data, load_price_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Define power law fitting function
def fit_power_law(df, x_col='days_from_genesis', y_col='Hashrate_PH'):
    """Fit power law y = a*x^b to data"""
    x_data = df[x_col].values
    y_data = df[y_col].values
    
    # Power law function
    def power_law(x, a, b):
        return a * np.power(x, b)
    
    # Fit the data
    try:
        params, _ = curve_fit(power_law, x_data, y_data, maxfev=5000)
        a, b = params
        
        # Calculate R-squared
        residuals = y_data - power_law(x_data, a, b)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y_data - np.mean(y_data))**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        return a, b, r_squared
    except Exception as e:
        st.error(f"Power law fitting failed: {str(e)}")
        return None, None, None

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

# Normalize timestamps to daily resolution
df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
price_df['Date'] = pd.to_datetime(price_df['Date']).dt.normalize()

# Remove duplicate dates (keep last)
price_df = price_df.drop_duplicates('Date', keep='last')

# Merge data
merged_df = pd.merge(df, price_df[['Date', 'Price']], on='Date', how='left')

# Calculate price/hashrate ratio and days since genesis
analysis_df = merged_df.dropna(subset=['Hashrate_PH', 'Price']).copy()
analysis_df['Price_Hashrate_Ratio'] = analysis_df['Price'] / analysis_df['Hashrate_PH']
analysis_df['Days_Since_Genesis'] = (analysis_df['Date'] - genesis_date).dt.days + 1  # +1 to avoid log(0)

# Calculate power law fit for the ratio
try:
    # Fit power law to the ratio vs time
    a_ratio, b_ratio, r2_ratio = fit_power_law(analysis_df, x_col='Days_Since_Genesis', y_col='Price_Hashrate_Ratio')
    if None in [a_ratio, b_ratio, r2_ratio]:
        st.error("Failed to calculate ratio power law fit")
        st.stop()
        
    # Calculate expected ratio values based on power law
    analysis_df['Expected_Ratio'] = a_ratio * np.power(analysis_df['Days_Since_Genesis'], b_ratio)
    
    # Calculate percentage deviation from expected ratio
    analysis_df['Ratio_Deviation_Pct'] = ((analysis_df['Price_Hashrate_Ratio'] - analysis_df['Expected_Ratio']) / analysis_df['Expected_Ratio']) * 100
    
    # Calculate Bollinger Band-like standard deviation bands
    rolling_window = min(30, len(analysis_df))  # Use 30-day window or all data if less
    analysis_df['Deviation_MA'] = analysis_df['Ratio_Deviation_Pct'].rolling(rolling_window).mean()
    analysis_df['Deviation_Std'] = analysis_df['Ratio_Deviation_Pct'].rolling(rolling_window).std()
    analysis_df['Upper_Band'] = analysis_df['Deviation_MA'] + (2 * analysis_df['Deviation_Std'])
    analysis_df['Lower_Band'] = analysis_df['Deviation_MA'] - (2 * analysis_df['Deviation_Std'])
    
except Exception as e:
    st.error(f"Failed to calculate ratio power law: {str(e)}")
    st.stop()

# Create color gradient for last 7 points (teal to purple)
last_7 = analysis_df.tail(7).copy()
purple_gradient = ['#00FFCC', '#40E0D0', '#80C0FF', '#A080FF', '#C040FF', '#E000FF', '#FF00FF']
last_7['color'] = purple_gradient

# Custom CSS remains the same as before...

# ====== MAIN CHART CONTAINER ======
# (Same as before until the oscillator section)

    # ====== OSCILLATOR CHART ======
    st.markdown('<div class="title-spacing"><h4>Price/Hashrate Ratio Deviation from Trend (%)</h4></div>', unsafe_allow_html=True)
    
    osc_fig = go.Figure()
    
    # Determine x-axis values based on time scale selection
    if x_scale_type == "Log":
        x_osc = filtered_analysis_df['Days_Since_Genesis']
        x_osc_title = 'Days Since Genesis (Log Scale)'
    else:
        x_osc = filtered_analysis_df['Date']
        x_osc_title = 'Date'
    
    # Add zero line
    osc_fig.add_shape(
        type="line",
        x0=x_osc.iloc[0], x1=x_osc.iloc[-1],
        y0=0, y1=0,
        line=dict(color="rgba(255,255,255,0.5)", width=1, dash="dot")
    )
    
    # Add Bollinger-style bands
    osc_fig.add_trace(go.Scatter(
        x=x_osc,
        y=filtered_analysis_df['Upper_Band'],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    osc_fig.add_trace(go.Scatter(
        x=x_osc,
        y=filtered_analysis_df['Lower_Band'],
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(100, 100, 100, 0.2)',
        name='±2σ Range',
        hoverinfo='skip'
    ))
    
    # Add deviation line
    osc_fig.add_trace(go.Scatter(
        x=x_osc,
        y=filtered_analysis_df['Ratio_Deviation_Pct'],
        mode='lines',
        name='Deviation %',
        line=dict(color='#00FFCC', width=2),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Deviation</b>: %{y:.1f}%<extra></extra>',
        text=filtered_analysis_df['Date']
    ))
    
    # Add moving average line
    osc_fig.add_trace(go.Scatter(
        x=x_osc,
        y=filtered_analysis_df['Deviation_MA'],
        mode='lines',
        name='30D Avg',
        line=dict(color='rgba(255,165,0,0.7)', width=1, dash='dot'),
        hovertemplate='<b>30D Avg</b>: %{y:.1f}%<extra></extra>'
    ))
    
    # Add colored markers for last 7 points
    last_7_filtered = filtered_analysis_df.tail(7)
    for i, row in last_7_filtered.iterrows():
        x_val = row['Days_Since_Genesis'] if x_scale_type == "Log" else row['Date']
        osc_fig.add_trace(go.Scatter(
            x=[x_val],
            y=[row['Ratio_Deviation_Pct']],
            mode='markers',
            marker=dict(
                color=purple_gradient[i % len(purple_gradient)],
                size=8,
                line=dict(width=1.5, color='DarkSlateGrey')
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    osc_fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=200,
        margin=dict(l=20, r=20, t=30, b=50),
        yaxis_title='Deviation from Trend (%)',
        xaxis_title=x_osc_title,
        xaxis=dict(
            type="log" if x_scale_type == "Log" else None,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='#3A3C4A',
            zeroline=False
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
    
    st.plotly_chart(osc_fig, use_container_width=True, className="oscillator-chart")

# Stats
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(4)
with cols[0]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
with cols[1]:
    st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")
with cols[2]:
    current_deviation = analysis_df['Ratio_Deviation_Pct'].iloc[-1]
    st.metric("Current Deviation", f"{current_deviation:.1f}%")
with cols[3]:
    st.metric("Ratio Trend (R²)", f"{r2_ratio:.3f}")
st.markdown('</div>', unsafe_allow_html=True)
