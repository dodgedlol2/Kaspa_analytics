import streamlit as st
from components.shared_components import (
    render_page_config,
    render_custom_css_with_sidebar,
    render_clean_header,
    render_beautiful_sidebar,
    render_simple_page_header
)
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Try to import utils - handle gracefully if not available
try:
    from utils import fit_power_law, load_price_data
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    st.error("Utils module not found. Please ensure utils.py is available with fit_power_law and load_price_data functions.")
    st.stop()

# MUST be first Streamlit command
render_page_config(page_title="Price Analysis - Kaspa Analytics Pro")

# Apply custom CSS with beautiful sidebar support
render_custom_css_with_sidebar()

# Render clean header
render_clean_header(
    user_name=None,  # Try "John Doe" to test user menu
    show_auth=True
)

# Render beautiful dropdown sidebar
render_beautiful_sidebar(current_page="Price")

# Data loading and processing
if 'price_df' not in st.session_state or 'price_genesis_date' not in st.session_state:
    try:
        st.session_state.price_df, st.session_state.price_genesis_date = load_price_data()
    except Exception as e:
        st.error(f"Failed to load price data: {str(e)}")
        st.stop()

price_df = st.session_state.price_df
genesis_date = st.session_state.price_genesis_date

try:
    a_price, b_price, r2_price = fit_power_law(price_df, y_col='Price')
except Exception as e:
    st.error(f"Failed to calculate price power law: {str(e)}")
    st.stop()

# Simplified CSS without dropdown styling conflicts
st.markdown("""
<style>
    /* Price-specific styling that EXTENDS shared components */
    
    @keyframes shimmer {
        0% {
            background-position: -200% center;
            text-shadow: 0 0 10px rgba(241, 245, 249, 0.3);
        }
        50% {
            text-shadow: 
                0 0 20px rgba(0, 212, 255, 0.6),
                0 0 30px rgba(0, 212, 255, 0.4),
                0 0 40px rgba(0, 212, 255, 0.2);
        }
        100% {
            background-position: 200% center;
            text-shadow: 0 0 10px rgba(241, 245, 249, 0.3);
        }
    }
    
    @keyframes glow {
        0%, 100% {
            text-shadow: 
                0 0 10px rgba(241, 245, 249, 0.3),
                0 0 20px rgba(0, 212, 255, 0.2),
                0 0 30px rgba(0, 212, 255, 0.1);
        }
        50% {
            text-shadow: 
                0 0 20px rgba(241, 245, 249, 0.5),
                0 0 30px rgba(0, 212, 255, 0.4),
                0 0 40px rgba(0, 212, 255, 0.3),
                0 0 50px rgba(0, 212, 255, 0.2);
        }
    }
    
    /* Simple header section */
    .price-header-section {
        padding: 20px 40px 15px 40px;
        background: transparent;
        text-align: center;
        margin-bottom: 10px;
        margin-top: 20px;
    }
    
    .price-main-title {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: 0.5px;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #f1f5f9 0%, #00d4ff 50%, #f1f5f9 100%);
        background-size: 200% 100%;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s ease-in-out infinite;
        line-height: 1.2;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        margin-bottom: 16px !important;
        width: 100% !important;
        box-sizing: border-box !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 212, 255, 0.4) !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.15), 0 0 0 1px rgba(0, 212, 255, 0.2) !important;
        transform: translateY(-3px) !important;
        background: rgba(30, 41, 59, 0.6) !important;
    }
    
    .metric-label {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 10px !important;
    }
    
    .metric-value {
        color: #f1f5f9 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        margin-bottom: 6px !important;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
    }
    
    .metric-delta {
        font-size: 14px !important;
        font-weight: 700 !important;
        margin-bottom: 8px;
    }
    
    .metric-delta.positive {
        color: #00ff88 !important;
    }
    
    .metric-delta.negative {
        color: #ff4757 !important;
    }
    
    /* Chart styling */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
    }
    
    .stPlotlyChart .modebar {
        background: transparent !important;
        transform: translateY(10px) !important;
    }
    
    .stPlotlyChart .modebar-group {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Simple header section
st.markdown("""
<div class="price-header-section">
    <h1 class="price-main-title">Kaspa Price Analysis</h1>
</div>
""", unsafe_allow_html=True)

# Calculate current metrics for later use
current_price = price_df['Price'].iloc[-1]
last_date = price_df['Date'].iloc[-1]
thirty_days_ago = last_date - timedelta(days=30)
df_30_days_ago = price_df[price_df['Date'] >= thirty_days_ago]

if len(df_30_days_ago) > 0:
    price_30_days_ago = df_30_days_ago['Price'].iloc[0]
    price_pct_change = ((current_price - price_30_days_ago) / price_30_days_ago) * 100
else:
    price_pct_change = 0

# Helper functions for chart
def format_currency(value):
    """Format currency values for clean display"""
    if value >= 1:
        if value >= 1000:
            return f"${value/1000:.1f}k"
        elif value >= 100:
            return f"${value:.0f}"
        elif value >= 10:
            return f"${value:.1f}"
        else:
            return f"${value:.2f}"
    elif value >= 0.01:
        return f"${value:.3f}"
    elif value >= 0.001:
        return f"${value:.4f}"
    elif value >= 0.0001:
        return f"${value:.5f}"
    else:
        return f"${value:.1e}"

def generate_log_ticks(data_min, data_max):
    """Generate physics-style log tick marks with 1, 2, 5 pattern"""
    import math
    log_min = math.floor(math.log10(data_min))
    log_max = math.ceil(math.log10(data_max))
    
    major_ticks = []
    intermediate_ticks = []
    minor_ticks = []
    
    for i in range(log_min, log_max + 1):
        base = 10**i
        
        if data_min <= base <= data_max:
            major_ticks.append(base)
        
        for factor in [2, 5]:
            intermediate_val = factor * base
            if data_min <= intermediate_val <= data_max:
                intermediate_ticks.append(intermediate_val)
        
        for j in [3, 4, 6, 7, 8, 9]:
            minor_val = j * base
            if data_min <= minor_val <= data_max:
                minor_ticks.append(minor_val)
    
    return major_ticks, intermediate_ticks, minor_ticks

def create_chart_data(time_range, x_scale_type, y_scale, show_power_law):
    """Create chart data based on parameters"""
    # Data filtering based on time range
    last_date_val = price_df['Date'].iloc[-1]
    if time_range == "1W":
        start_date = last_date_val - timedelta(days=7)
    elif time_range == "1M":
        start_date = last_date_val - timedelta(days=30)
    elif time_range == "3M":
        start_date = last_date_val - timedelta(days=90)
    elif time_range == "6M":
        start_date = last_date_val - timedelta(days=180)
    elif time_range == "1Y":
        start_date = last_date_val - timedelta(days=365)
    else:
        start_date = price_df['Date'].iloc[0]

    filtered_df = price_df[price_df['Date'] >= start_date]
    
    if x_scale_type == "Log":
        x_values = filtered_df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
    else:
        x_values = filtered_df['Date']
        x_title = "Date"
    
    traces = []
    
    # Main price trace
    traces.append(go.Scatter(
        x=x_values,
        y=filtered_df['Price'],
        mode='lines',
        name='Kaspa Price (USD)',
        line=dict(color='#00d4ff', width=3, shape='spline', smoothing=0.3),
        hovertemplate='<b>%{fullData.name}</b><br>Date: %{text}<br>Price: $%{y:.6f}<br><extra></extra>',
        text=[d.strftime('%Y-%m-%d') for d in filtered_df['Date']],
        showlegend=True,
        visible=True
    ))
    
    # Power law traces
    if show_power_law == "Show":
        x_fit = filtered_df['days_from_genesis']
        y_fit = a_price * np.power(x_fit, b_price)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        traces.append(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name=f'Power Law Fit (R²={r2_price:.3f})',
            line=dict(color='#ff8c00', width=3, dash='solid'),
            showlegend=True,
            hovertemplate='<b>Power Law Fit</b><br>R² = %{customdata:.3f}<br>Value: $%{y:.6f}<br><extra></extra>',
            customdata=[r2_price] * len(fit_x),
            visible=True
        ))

        traces.append(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='Support (-60%)',
            line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
            showlegend=True,
            hoverinfo='skip',
            visible=True
        ))
        
        traces.append(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='Resistance (+120%)',
            line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
            fill='tonexty',
            fillcolor='rgba(100, 100, 100, 0.05)',
            showlegend=True,
            hoverinfo='skip',
            visible=True
        ))
    
    return traces, filtered_df, x_title

# Create all possible chart configurations
time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
x_scales = ["Linear", "Log"] 
y_scales = ["Linear", "Log"]
power_law_options = ["Hide", "Show"]

# Create the main figure with all traces
fig = go.Figure()

# We'll create traces for each combination and control visibility with buttons
all_traces = []
trace_configs = []

base_trace_count = 0
for time_range in time_ranges:
    for x_scale in x_scales:
        for y_scale in y_scales:
            for power_law in power_law_options:
                traces, filtered_df, x_title = create_chart_data(time_range, x_scale, y_scale, power_law)
                
                config = {
                    'time_range': time_range,
                    'x_scale': x_scale, 
                    'y_scale': y_scale,
                    'power_law': power_law,
                    'trace_indices': list(range(base_trace_count, base_trace_count + len(traces))),
                    'filtered_df': filtered_df,
                    'x_title': x_title
                }
                trace_configs.append(config)
                all_traces.extend(traces)
                base_trace_count += len(traces)

# Add all traces to figure (initially hidden)
for i, trace in enumerate(all_traces):
    trace.visible = False
    fig.add_trace(trace)

# Set default configuration and get proper layout settings
default_config_idx = None
for i, config in enumerate(trace_configs):
    if (config['time_range'] == 'All' and 
        config['x_scale'] == 'Log' and 
        config['y_scale'] == 'Log' and 
        config['power_law'] == 'Show'):
        default_config_idx = i
        break

if default_config_idx is not None:
    default_config = trace_configs[default_config_idx]
    for idx in default_config['trace_indices']:
        fig.data[idx].visible = True
    
    # Get the default layout settings
    default_filtered_df = default_config['filtered_df']
    default_y_min, default_y_max = default_filtered_df['Price'].min(), default_filtered_df['Price'].max()
    default_x_min, default_x_max = default_filtered_df['days_from_genesis'].min(), default_filtered_df['days_from_genesis'].max()
    
    # Generate default log ticks
    default_y_major, default_y_intermediate, default_y_minor = generate_log_ticks(default_y_min, default_y_max)
    default_y_tick_vals = sorted(default_y_major + default_y_intermediate)
    default_y_tick_text = [format_currency(val) for val in default_y_tick_vals]
    
    default_x_major, default_x_intermediate, default_x_minor = generate_log_ticks(default_x_min, default_x_max)
    default_x_tick_vals = sorted(default_x_major + default_x_intermediate)
    default_x_tick_text = [f"{int(val)}" for val in default_x_tick_vals]

# Create dropdown menu configurations
def create_visibility_array(target_config_idx):
    """Create visibility array for specific configuration"""
    visibility = [False] * len(all_traces)
    target_config = trace_configs[target_config_idx]
    for idx in target_config['trace_indices']:
        visibility[idx] = True
    return visibility

def create_update_args(target_config_idx):
    """Create complete update arguments including layout changes"""
    target_config = trace_configs[target_config_idx]
    filtered_df = target_config['filtered_df']
    
    # Calculate axis ranges for better view
    y_min, y_max = filtered_df['Price'].min(), filtered_df['Price'].max()
    y_padding = 0.1 * (y_max - y_min) if target_config['y_scale'] == 'Linear' else 0
    
    if target_config['x_scale'] == 'Log':
        x_min, x_max = filtered_df['days_from_genesis'].min(), filtered_df['days_from_genesis'].max()
        x_padding = 0.05 * (x_max - x_min)
        x_range = [x_min - x_padding, x_max + x_padding]
        x_title = "Days Since Genesis (Log Scale)"
        x_type = "log"
    else:
        x_min, x_max = filtered_df['Date'].min(), filtered_df['Date'].max()
        x_padding = timedelta(days=max(1, int((x_max - x_min).days * 0.02)))
        x_range = [x_min - x_padding, x_max + x_padding]
        x_title = "Date" 
        x_type = "date"
    
    if target_config['y_scale'] == 'Log':
        y_range = [y_min * 0.8, y_max * 1.2]
        y_type = "log"
        # Generate custom log ticks
        y_major_ticks, y_intermediate_ticks, y_minor_ticks = generate_log_ticks(y_min, y_max)
        y_tick_vals = sorted(y_major_ticks + y_intermediate_ticks)
        y_tick_text = [format_currency(val) for val in y_tick_vals]
        y_minor_dict = dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(255, 255, 255, 0.04)',
            tickmode='array',
            tickvals=y_minor_ticks
        )
        y_tickmode = 'array'
        y_gridcolor = 'rgba(255, 255, 255, 0.12)'
    else:
        y_range = [y_min - y_padding, y_max + y_padding]
        y_type = "linear"
        y_tick_vals = None
        y_tick_text = None
        y_minor_dict = dict()
        y_tickmode = 'auto'
        y_gridcolor = 'rgba(255, 255, 255, 0.08)'
    
    # Generate X-axis ticks for log scale
    if target_config['x_scale'] == 'Log':
        x_major_ticks, x_intermediate_ticks, x_minor_ticks = generate_log_ticks(x_min, x_max)
        x_tick_vals = sorted(x_major_ticks + x_intermediate_ticks)
        x_tick_text = [f"{int(val)}" for val in x_tick_vals]
        x_minor_dict = dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(255, 255, 255, 0.04)',
            tickmode='array',
            tickvals=x_minor_ticks
        )
        x_tickmode = 'array'
        x_gridcolor = 'rgba(255, 255, 255, 0.12)'
    else:
        x_tick_vals = None
        x_tick_text = None
        x_minor_dict = dict()
        x_tickmode = 'auto'
        x_gridcolor = 'rgba(255, 255, 255, 0.08)'
    
    return {
        'visible': create_visibility_array(target_config_idx),
    }, {
        'xaxis.type': x_type,
        'xaxis.range': x_range,
        'xaxis.title.text': x_title,
        'xaxis.tickmode': x_tickmode,
        'xaxis.tickvals': x_tick_vals,
        'xaxis.ticktext': x_tick_text,
        'xaxis.minor': x_minor_dict,
        'xaxis.gridcolor': x_gridcolor,
        'yaxis.type': y_type,
        'yaxis.range': y_range,
        'yaxis.tickmode': y_tickmode,
        'yaxis.tickvals': y_tick_vals,
        'yaxis.ticktext': y_tick_text,
        'yaxis.minor': y_minor_dict,
        'yaxis.gridcolor': y_gridcolor
    }

# Time Range Dropdown
time_range_buttons = []
for time_range in time_ranges:
    # Find config that matches current settings with this time range
    for i, config in enumerate(trace_configs):
        if (config['time_range'] == time_range and
            config['x_scale'] == 'Log' and  # Default to Log
            config['y_scale'] == 'Log' and  # Default to Log  
            config['power_law'] == 'Show'):  # Default to Show
            trace_args, layout_args = create_update_args(i)
            time_range_buttons.append({
                'label': time_range,
                'method': 'update',
                'args': [trace_args, layout_args]
            })
            break

# X-Scale Dropdown
x_scale_buttons = []
for x_scale in x_scales:
    for i, config in enumerate(trace_configs):
        if (config['time_range'] == 'All' and  # Default to All
            config['x_scale'] == x_scale and
            config['y_scale'] == 'Log' and    # Default to Log
            config['power_law'] == 'Show'):   # Default to Show
            trace_args, layout_args = create_update_args(i)
            x_scale_buttons.append({
                'label': x_scale,
                'method': 'update', 
                'args': [trace_args, layout_args]
            })
            break

# Y-Scale Dropdown
y_scale_buttons = []
for y_scale in y_scales:
    for i, config in enumerate(trace_configs):
        if (config['time_range'] == 'All' and  # Default to All
            config['x_scale'] == 'Log' and    # Default to Log
            config['y_scale'] == y_scale and
            config['power_law'] == 'Show'):   # Default to Show
            trace_args, layout_args = create_update_args(i)
            y_scale_buttons.append({
                'label': y_scale,
                'method': 'update',
                'args': [trace_args, layout_args]
            })
            break

# Power Law Dropdown
power_law_buttons = []
for power_law in power_law_options:
    for i, config in enumerate(trace_configs):
        if (config['time_range'] == 'All' and  # Default to All
            config['x_scale'] == 'Log' and    # Default to Log
            config['y_scale'] == 'Log' and    # Default to Log
            config['power_law'] == power_law):
            trace_args, layout_args = create_update_args(i)
            power_law_buttons.append({
                'label': power_law,
                'method': 'update',
                'args': [trace_args, layout_args]
            })
            break

# Update layout with dropdowns
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e2e8f0'),
    hovermode='x unified',
    height=700,
    margin=dict(l=30, r=30, t=120, b=10),
    
    # Add dropdown menus
    updatemenus=[
        # Time Range Dropdown
        dict(
            buttons=time_range_buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.02,
            xanchor="left",
            y=1.12,
            yanchor="top",
            bgcolor='rgba(30, 41, 59, 0.9)',
            bordercolor='rgba(100, 116, 139, 0.3)',
            borderwidth=1,
            font=dict(color='#f1f5f9', size=12)
        ),
        # X-Scale Dropdown  
        dict(
            buttons=x_scale_buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.25,
            xanchor="left", 
            y=1.12,
            yanchor="top",
            bgcolor='rgba(30, 41, 59, 0.9)',
            bordercolor='rgba(100, 116, 139, 0.3)',
            borderwidth=1,
            font=dict(color='#f1f5f9', size=12)
        ),
        # Y-Scale Dropdown
        dict(
            buttons=y_scale_buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.48,
            xanchor="left",
            y=1.12, 
            yanchor="top",
            bgcolor='rgba(30, 41, 59, 0.9)',
            bordercolor='rgba(100, 116, 139, 0.3)',
            borderwidth=1,
            font=dict(color='#f1f5f9', size=12)
        ),
        # Power Law Dropdown
        dict(
            buttons=power_law_buttons,
            direction="down", 
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.71,
            xanchor="left",
            y=1.12,
            yanchor="top",
            bgcolor='rgba(30, 41, 59, 0.9)',
            bordercolor='rgba(100, 116, 139, 0.3)', 
            borderwidth=1,
            font=dict(color='#f1f5f9', size=12)
        )
    ],
    
    # Add annotations for dropdown labels
    annotations=[
        dict(text="Time Period", x=0.02, y=1.15, xanchor='left', yanchor='bottom',
             font=dict(size=11, color='#94a3b8', family='Inter'), showarrow=False),
        dict(text="Time Scale", x=0.25, y=1.15, xanchor='left', yanchor='bottom', 
             font=dict(size=11, color='#94a3b8', family='Inter'), showarrow=False),
        dict(text="Price Scale", x=0.48, y=1.15, xanchor='left', yanchor='bottom',
             font=dict(size=11, color='#94a3b8', family='Inter'), showarrow=False), 
        dict(text="Power Law", x=0.71, y=1.15, xanchor='left', yanchor='bottom',
             font=dict(size=11, color='#94a3b8', family='Inter'), showarrow=False)
    ],
    
    xaxis=dict(
        title=dict(text="Days Since Genesis (Log Scale)", font=dict(size=13, color='#cbd5e1', weight=600), standoff=35),
        type="log",
        range=[default_x_min * 0.95, default_x_max * 1.05],
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.12)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
        tickmode='array',
        tickvals=default_x_tick_vals,
        ticktext=default_x_tick_text,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(255, 255, 255, 0.04)',
            tickmode='array',
            tickvals=default_x_minor
        )
    ),
    yaxis=dict(
        title=None,
        type="log",
        range=[default_y_min * 0.8, default_y_max * 1.2],
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.12)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
        tickmode='array',
        tickvals=default_y_tick_vals,
        ticktext=default_y_tick_text,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(255, 255, 255, 0.04)',
            tickmode='array',
            tickvals=default_y_minor
        )
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        borderwidth=0,
        font=dict(size=11)
    ),
    hoverlabel=dict(
        bgcolor='rgba(15, 20, 25, 0.95)',
        bordercolor='rgba(0, 212, 255, 0.5)',
        font=dict(color='#e2e8f0', size=11),
        align='left'
    )
)

# Display chart
with st.container():
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': f'kaspa_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}',
            'height': 700,
            'width': 1400,
            'scale': 2
        }
    })

# Calculate comprehensive metrics
if len(df_30_days_ago) > 0:
    price_30_days_ago_data = price_df[price_df['Date'] <= thirty_days_ago]
    if len(price_30_days_ago_data) > 10:
        try:
            a_price_30d, b_price_30d, r2_price_30d = fit_power_law(price_30_days_ago_data, y_col='Price')
        except:
            b_price_30d = b_price
            r2_price_30d = r2_price
    else:
        b_price_30d = b_price
        r2_price_30d = r2_price
    
    slope_pct_change = ((b_price - b_price_30d) / abs(b_price_30d)) * 100 if b_price_30d != 0 else 0
    r2_pct_change = ((r2_price - r2_price_30d) / r2_price_30d) * 100 if r2_price_30d != 0 else 0
else:
    slope_pct_change = 0
    r2_pct_change = 0

# Enhanced Metrics Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">POWER-LAW SLOPE</div>
        <div class="metric-value">{b_price:.4f}</div>
        <div class="metric-delta {'positive' if slope_pct_change >= 0 else 'negative'}">{slope_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col2:
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">MODEL ACCURACY (R²)</div>
        <div class="metric-value">{r2_price:.4f}</div>
        <div class="metric-delta {'positive' if r2_pct_change >= 0 else 'negative'}">{r2_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col3:
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">CURRENT PRICE</div>
        <div class="metric-value">${current_price:.6f}</div>
        <div class="metric-delta {'positive' if price_pct_change >= 0 else 'negative'}">{price_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col4:
    market_cap_estimate = current_price * 24e9
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">EST. MARKET CAP</div>
        <div class="metric-value">${market_cap_estimate/1e9:.2f}B</div>
        <div class="metric-delta {'positive' if price_pct_change >= 0 else 'negative'}">{price_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

# Footer
footer_html = """
<div style="text-align: center; padding: 40px 40px; margin-top: 32px; 
     background: rgba(15, 20, 25, 0.3); backdrop-filter: blur(20px);
     border-top: 1px solid rgba(255, 255, 255, 0.08);">
    <div style="max-width: 1200px; margin: 0 auto;">
        <p style="color: #64748b; font-size: 13px; margin-bottom: 16px;">
            Professional-grade cryptocurrency market analysis • Real-time data processing • Advanced predictive modeling
        </p>
        <div style="color: #475569; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">
            Last Updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + """ • 
            Built for institutional-grade analysis
        </div>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
