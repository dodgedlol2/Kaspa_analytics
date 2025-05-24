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
analysis_df['Price_Hashrate_Ratio'] = analysis_df['Price'] / analysis_df['Hashrate_PH']

# Calculate power law for price vs hashrate relationship
try:
    a_relation, b_relation, r2_relation = fit_power_law(analysis_df, x_col='Hashrate_PH', y_col='Price')
except Exception as e:
    st.error(f"Failed to calculate price-hashrate power law: {str(e)}")
    st.stop()

# Create color gradient for last 7 points (teal to purple)
last_7 = analysis_df.tail(7).copy()
purple_gradient = ['#00FFCC', '#40E0D0', '#80C0FF', '#A080FF', '#C040FF', '#E000FF', '#FF00FF']
last_7['color'] = purple_gradient

# Custom CSS - consistent styling
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
    .ratio-chart {
        margin-top: -30px !important;
        height: 250px !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Price vs Hashrate Analysis</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container
    col_spacer_left, col1, col2, col3, col4, spacer1, spacer2, spacer3, spacer4, spacer5, spacer6, spacer7, spacer8 = st.columns(
        [0.35, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 3]
    )

    with col1:
        st.markdown('<div class="control-label">Price Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Price Scale", y_scale_options,
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
        st.markdown('<div class="control-label">Ratio Scale</div>', unsafe_allow_html=True)
        ratio_scale_options = ["Linear", "Log"]
        ratio_scale = st.selectbox("Ratio Scale", ratio_scale_options,
                                   index=1,
                                   label_visibility="collapsed", key="ratio_scale_select")
    
    # Second divider - under the dropdown menus
    st.divider()

    # Create the main figure
    fig = go.Figure()

    # Add scatter trace for all price vs hashrate points (original teal color)
    fig.add_trace(go.Scatter(
        x=analysis_df['Hashrate_PH'],
        y=analysis_df['Price'],
        mode='markers',
        name='Price vs Hashrate',
        marker=dict(
            color='#00FFCC',
            size=8,
            opacity=0.7,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hovertemplate='<b>Hashrate</b>: %{x:.2f} PH/s<br><b>Price</b>: $%{y:.4f}<br><b>Date</b>: %{text}<extra></extra>',
        text=analysis_df['Date'].dt.strftime('%Y-%m-%d')
    ))

    # Add colored scatter trace for last 7 points (teal to purple gradient)
    for i, row in last_7.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Hashrate_PH']],
            y=[row['Price']],
            mode='markers',
            name=f"Recent ({row['Date'].strftime('%Y-%m-%d')})" if i == last_7.index[-1] else None,
            marker=dict(
                color=row['color'],
                size=12,
                opacity=0.9,
                line=dict(width=1.5, color='DarkSlateGrey')
            ),
            hovertemplate='<b>Hashrate</b>: %{x:.2f} PH/s<br><b>Price</b>: $%{y:.4f}<br><b>Date</b>: %{text}<extra></extra>',
            text=[row['Date'].strftime('%Y-%m-%d')],
            showlegend=False
        ))

    if show_power_law == "Show":
        # Generate fitted values
        x_fit = np.linspace(analysis_df['Hashrate_PH'].min(), analysis_df['Hashrate_PH'].max(), 100)
        y_fit = a_relation * np.power(x_fit, b_relation)
        
        fig.add_trace(go.Scatter(
            x=x_fit,
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2_relation:.3f})',
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
        height=500,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Price (USD)',
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
    st.markdown('<div class="title-spacing"><h4>Price/Hashrate Ratio</h4></div>', unsafe_allow_html=True)
    
    ratio_fig = go.Figure()
    
    ratio_fig.add_trace(go.Scatter(
        x=analysis_df['Date'],
        y=analysis_df['Price_Hashrate_Ratio'],
        mode='lines+markers',
        name='Price/Hashrate Ratio',
        line=dict(color='#00FFCC', width=2),
        marker=dict(size=5, color='#00FFCC'),
        hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Ratio</b>: %{y:.6f}<extra></extra>'
    ))
    
    # Add colored markers for last 7 points
    for i, row in last_7.iterrows():
        ratio_fig.add_trace(go.Scatter(
            x=[row['Date']],
            y=[row['Price_Hashrate_Ratio']],
            mode='markers',
            marker=dict(
                color=row['color'],
                size=8,
                line=dict(width=1.5, color='DarkSlateGrey')
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    ratio_fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=250,
        margin=dict(l=20, r=20, t=30, b=50),
        yaxis_title='Price/Hashrate Ratio (USD/PH/s)',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
        ),
        yaxis=dict(
            type="log" if ratio_scale == "Log" else "linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
        ),
        hoverlabel=dict(
            bgcolor='#262730',
            bordercolor='#3A3C4A',
            font_color='#e0e0e0'
        )
    )
    
    st.plotly_chart(ratio_fig, use_container_width=True, className="ratio-chart")

# Stats
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    st.metric("Power-Law Slope", f"{b_relation:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2_relation:.3f}")
with cols[2]:
    current_ratio = analysis_df['Price_Hashrate_Ratio'].iloc[-1]
    st.metric("Current Ratio", f"{current_ratio:.6f}")
with cols[3]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
with cols[4]:
    st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")
st.markdown('</div>', unsafe_allow_html=True)
