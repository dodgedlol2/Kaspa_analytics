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
analysis_df = merged_df.dropna(subset=['Hashrate_PH', 'Price'])

# Calculate power law for price vs hashrate relationship
try:
    a_relation, b_relation, r2_relation = fit_power_law(analysis_df, x_col='Hashrate_PH', y_col='Price')
except Exception as e:
    st.error(f"Failed to calculate price-hashrate power law: {str(e)}")
    st.stop()

# Create color gradient for last 30 points
last_30 = analysis_df.tail(30).copy()
colors = ['#FF0000', '#FF4500', '#FF8C00', '#FFA500', '#FFD700', 
          '#FFFF00', '#ADFF2F', '#7CFC00', '#00FF00', '#00FA9A', 
          '#00FFFF', '#1E90FF', '#0000FF', '#8A2BE2', '#9400D3']
n_colors = len(colors)
last_30['color_index'] = range(len(last_30))
last_30['color'] = last_30['color_index'].apply(lambda x: colors[min(x, n_colors-1)])

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
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Price vs Hashrate Analysis</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container
    col_spacer_left, col1, col2, col3, col4, spacer1, spacer2, spacer3, spacer4, spacer5, spacer6, spacer7, spacer8, spacer9 = st.columns(
        [0.35, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 3]
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
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        time_scale_options = ["Linear", "Log"]
        time_scale = st.selectbox("Time Scale", time_scale_options,
                                index=0,
                                label_visibility="collapsed", key="time_scale_select")
    
    # Second divider - under the dropdown menus
    st.divider()

    # Create the main figure
    fig = go.Figure()

    # Add scatter trace for all price vs hashrate points (light gray)
    fig.add_trace(go.Scatter(
        x=analysis_df['Hashrate_PH'],
        y=analysis_df['Price'],
        mode='markers',
        name='Historical Data',
        marker=dict(
            color='rgba(150, 150, 150, 0.3)',
            size=6,
            line=dict(width=0.5, color='DarkSlateGrey')
        ),
        hovertemplate='<b>Hashrate</b>: %{x:.2f} PH/s<br><b>Price</b>: $%{y:.4f}<br><b>Date</b>: %{text}<extra></extra>',
        text=analysis_df['Date'].dt.strftime('%Y-%m-%d')
    ))

    # Add colored scatter trace for last 30 points
    for i, row in last_30.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Hashrate_PH']],
            y=[row['Price']],
            mode='markers',
            name=f"Recent ({row['Date'].strftime('%Y-%m-%d')})" if i == last_30.index[-1] else None,
            marker=dict(
                color=row['color'],
                size=10,
                line=dict(width=1, color='DarkSlateGrey')
            ),
            hovertemplate='<b>Hashrate</b>: %{x:.2f} PH/s<br><b>Price</b>: $%{y:.4f}<br><b>Date</b>: %{text}<extra></extra>',
            text=[row['Date'].strftime('%Y-%m-%d')],
            showlegend=False
        ))

    # Add price over time on secondary y-axis
    fig.add_trace(go.Scatter(
        x=analysis_df['Hashrate_PH'],
        y=analysis_df['Price'],
        mode='lines',
        name='Price Trend',
        line=dict(color='rgba(150, 150, 150, 0.7)', width=1.5),
        hovertemplate='<b>Hashrate</b>: %{x:.2f} PH/s<br><b>Price</b>: $%{y:.4f}<br><b>Date</b>: %{text}<extra></extra>',
        text=analysis_df['Date'].dt.strftime('%Y-%m-%d'),
        yaxis='y2'
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
        height=700,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Price vs Hashrate (USD/PH/s)',
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
        yaxis2=dict(
            title='Price Over Time (USD)',
            overlaying='y',
            side='right',
            type="log" if y_scale == "Log" else "linear",
            showgrid=False,
            linecolor='rgba(150, 150, 150, 0.5)',
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

    st.plotly_chart(fig, use_container_width=True)

# Stats
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(4)
with cols[0]:
    st.metric("Power-Law Slope", f"{b_relation:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2_relation:.3f}")
with cols[2]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
with cols[3]:
    st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")
st.markdown('</div>', unsafe_allow_html=True)
