import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data, load_price_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Reuse the same data loading logic from your existing page
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
analysis_df['Price_Hashrate_Ratio'] = analysis_df['Price'] / analysis_df['Hashrate_PH']
analysis_df['Days_Since_Genesis'] = (analysis_df['Date'] - genesis_date).dt.days + 1

# Calculate power law for ratio vs time relationship
try:
    a_ratio_time, b_ratio_time, r2_ratio_time = fit_power_law(analysis_df, x_col='Days_Since_Genesis', y_col='Price_Hashrate_Ratio')
    
    # Calculate expected ratio based on power law
    analysis_df['Expected_Ratio'] = a_ratio_time * np.power(analysis_df['Days_Since_Genesis'], b_ratio_time)
    
    # Calculate % difference from power law
    analysis_df['Ratio_Difference_Pct'] = ((analysis_df['Price_Hashrate_Ratio'] - analysis_df['Expected_Ratio']) / analysis_df['Expected_Ratio']) * 100
    
except Exception as e:
    st.error(f"Failed to calculate power laws: {str(e)}")
    st.stop()

# Custom CSS - reuse your existing styling
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
    .oscillator-container {
        height: 200px !important;
        margin-top: -20px !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN PRICE CHART ======
st.markdown('<div class="title-spacing"><h2>Kaspa Price with Hashrate Ratio Oscillator</h2></div>', unsafe_allow_html=True)
st.divider()

# Price chart
price_fig = go.Figure()

# Add price trace
price_fig.add_trace(go.Scatter(
    x=analysis_df['Date'],
    y=analysis_df['Price'],
    mode='lines',
    name='Price (USD)',
    line=dict(color='#00FFCC', width=2),
    hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>'
))

# Add recent price points with gradient colors
last_7 = analysis_df.tail(7).copy()
purple_gradient = ['#00FFCC', '#40E0D0', '#80C0FF', '#A080FF', '#C040FF', '#E000FF', '#FF00FF']
last_7['color'] = purple_gradient

for i, row in last_7.iterrows():
    price_fig.add_trace(go.Scatter(
        x=[row['Date']],
        y=[row['Price']],
        mode='markers',
        marker=dict(
            color=row['color'],
            size=10,
            line=dict(width=1.5, color='DarkSlateGrey')
        ),
        showlegend=False,
        hoverinfo='skip'
    ))

price_fig.update_layout(
    plot_bgcolor='#262730',
    paper_bgcolor='#262730',
    font_color='#e0e0e0',
    hovermode='x unified',
    height=400,
    margin=dict(l=20, r=20, t=60, b=80),
    yaxis_title='Price (USD)',
    xaxis_title='Date',
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        linecolor='#3A3C4A',
        zerolinecolor='#3A3C4A'
    ),
    yaxis=dict(
        type="log",
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
        x=1
    )
)

st.plotly_chart(price_fig, use_container_width=True)

# ====== OSCILLATOR CHART ======
st.markdown('<div class="title-spacing"><h4>Price/Hashrate Ratio Deviation from Power Law</h4></div>', unsafe_allow_html=True)

oscillator_fig = go.Figure()

# Add zero line
oscillator_fig.add_shape(
    type="line",
    x0=analysis_df['Date'].min(),
    y0=0,
    x1=analysis_df['Date'].max(),
    y1=0,
    line=dict(color="rgba(255,255,255,0.5)", width=1, dash="dot")
)

# Add oscillator bars
colors = ['rgba(0, 255, 0, 0.7)' if x >= 0 else 'rgba(255, 0, 0, 0.7)' for x in analysis_df['Ratio_Difference_Pct']]
oscillator_fig.add_trace(go.Bar(
    x=analysis_df['Date'],
    y=analysis_df['Ratio_Difference_Pct'],
    name='Deviation %',
    marker_color=colors,
    hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Deviation</b>: %{y:.1f}%<extra></extra>'
))

# Add recent points with gradient colors
for i, row in last_7.iterrows():
    oscillator_fig.add_trace(go.Scatter(
        x=[row['Date']],
        y=[row['Ratio_Difference_Pct']],
        mode='markers',
        marker=dict(
            color=row['color'],
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
    height=200,
    margin=dict(l=20, r=20, t=30, b=50),
    yaxis_title='Deviation from Power Law (%)',
    xaxis_title='Date',
    xaxis=dict(
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
        zerolinecolor='#3A3C4A'
    ),
    bargap=0
)

st.plotly_chart(oscillator_fig, use_container_width=True, className="oscillator-container")

# Stats
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    current_deviation = analysis_df['Ratio_Difference_Pct'].iloc[-1]
    st.metric("Current Deviation", f"{current_deviation:.1f}%", 
              delta_color="inverse" if current_deviation < 0 else "normal")
with cols[1]:
    st.metric("Power-Law Slope", f"{b_ratio_time:.3f}")
with cols[2]:
    st.metric("Power-Law Fit (R²)", f"{r2_ratio_time:.3f}")
with cols[3]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
with cols[4]:
    st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")
st.markdown('</div>', unsafe_allow_html=True)
