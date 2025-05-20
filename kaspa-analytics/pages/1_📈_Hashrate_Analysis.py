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

# Convert dates to datetime if not already
df['Date'] = pd.to_datetime(df['Date'])
min_date = df['Date'].min()
max_date = df['Date'].max()

# Add range slider for date selection
st.sidebar.markdown("### Date Range Selector")
date_range = st.sidebar.slider(
    "Select Date Range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# Filter data based on selected range
filtered_df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]

# [Rest of your existing CSS and control setup remains the same...]

# ====== ENHANCED CHART CONTAINER ======
with st.container(border=True):
    # [Your existing title and controls code remains the same...]

    # Create figure with enhanced grid
    fig = go.Figure()

    # Determine x-axis values based on scale type using filtered data
    if x_scale_type == "Log":
        x_values = filtered_df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
    else:
        x_values = filtered_df['Date']
        x_title = "Date"

    # Main trace using filtered data
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color='#00FFCC', width=2),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=filtered_df['Date']
    ))

    # Power-law fit (always shown) - using filtered date range
    x_fit = np.linspace(filtered_df['days_from_genesis'].min(), filtered_df['days_from_genesis'].max(), 100)
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
        line=dict(color='orange', dash='dot', width=1.5)
    ))
    
    # Deviation bands (only shown when toggled)
    if show_bands:
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='-60% Deviation',
            line=dict(color='rgba(150, 150, 150, 0.8)', dash='dot', width=1),
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='+120% Deviation',
            line=dict(color='rgba(150, 150, 150, 0.8)', dash='dot', width=1),
            hoverinfo='skip'
        ))

    # Add range slider to the bottom of the chart
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.05,
                bgcolor='rgba(150,150,150,0.2)'
            ),
            type="log" if x_scale_type == "Log" else None,
            # [Rest of your existing xaxis config...]
        ),
        # [Rest of your existing layout config...]
    )

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)

# [Rest of your existing code for metrics cards...]
