import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import r2_score

# Sample data
data = {
    'date': ['Aug 5 2023', 'Sep 5 2023', 'Oct 5 2023', 'Nov 5 2023', 'Dec 5 2023',
             'Jan 5 2024', 'Feb 5 2024', 'Mar 5 2024', 'Apr 5 2024', 'May 5 2024',
             'Jun 5 2024', 'Jul 5 2024', 'Aug 5 2024', 'Sep 5 2024', 'Oct 5 2024',
             'Nov 5 2024', 'Dec 5 2024', 'Jan 5 2025', 'Feb 5 2025', 'Mar 5 2025',
             'Apr 5 2025', 'May 5 2025', 'Jun 5 2025'],
    'openinterest': [1.21, 1.94, 4.69, 7.56, 32.19, 23.28, 19.35, 51.37, 39.39, 30.1,
                     71.24, 55.11, 76.75, 62.28, 80.17, 72.6, 131, 142.35, 97.3, 81.4,
                     78.29, 135.92, 128.85]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Set genesis date
genesis_date = pd.to_datetime('2021-11-07')
df['days_from_genesis'] = (df['date'] - genesis_date).dt.days

# Remove negative days (before genesis)
df = df[df['days_from_genesis'] >= 0]

# Power-law calculation function
def calculate_powerlaw(x_data, y_data):
    # Remove zero or negative values for log transformation
    valid_indices = (x_data > 0) & (y_data > 0)
    x_data, y_data = x_data[valid_indices], y_data[valid_indices]
    
    # Apply log transformation
    log_x = np.log10(x_data)
    log_y = np.log10(y_data)
    
    # Fit linear model in log-log space
    coeffs = np.polyfit(log_x, log_y, 1)
    b = coeffs[0]  # Slope
    a = 10 ** coeffs[1]  # Constant in linear space
    
    # Compute R^2 score
    y_pred = a * np.power(x_data, b)
    r2 = r2_score(log_y, np.log10(y_pred))
    
    return a, b, r2, x_data, y_data

# Calculate power-law
a, b, r2, x_data, y_data = calculate_powerlaw(
    df['days_from_genesis'].values,
    df['openinterest'].values
)

# Streamlit app
st.title('Open Interest Power-Law Analysis')
st.markdown("""
### Power-law fit for open interest over time
Using genesis date: 2021-11-07
""")

# Show parameters
col1, col2, col3 = st.columns(3)
col1.metric("Power-law exponent (slope)", f"{b:.3f}")
col2.metric("Coefficient (a)", f"{a:.3f}")
col3.metric("R² score", f"{r2:.3f}")

# Create plot
fig = go.Figure()

# Add actual data
fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['openinterest'],
    mode='lines+markers',
    name='Open Interest',
    line=dict(color='#00FFCC')
))

# Add power-law fit
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = a * np.power(x_fit, b)
fit_dates = [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]

fig.add_trace(go.Scatter(
    x=fit_dates,
    y=y_fit,
    mode='lines',
    name='Power-Law Fit',
    line=dict(color='orange', dash='dot')
))

# Add deviation bands
fig.add_trace(go.Scatter(
    x=fit_dates,
    y=y_fit * 0.4,  # -60%
    mode='lines',
    name='Lower Bound (-60%)',
    line=dict(color='lightgray', dash='dot')
))

fig.add_trace(go.Scatter(
    x=fit_dates,
    y=y_fit * 2.2,  # +120%
    mode='lines',
    name='Upper Bound (+120%)',
    line=dict(color='lightgray', dash='dot')
))

# Update layout
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Open Interest',
    yaxis_type='log',
    template='plotly_dark',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Log-log plot
st.markdown("### Log-log plot")
fig_log = go.Figure()

fig_log.add_trace(go.Scatter(
    x=x_data,
    y=y_data,
    mode='markers',
    name='Actual Data',
    marker=dict(color='#00FFCC')
))

fig_log.add_trace(go.Scatter(
    x=x_fit,
    y=y_fit,
    mode='lines',
    name='Power-Law Fit',
    line=dict(color='orange')
))

fig_log.update_layout(
    xaxis_title='Days from Genesis (log scale)',
    yaxis_title='Open Interest (log scale)',
    xaxis_type='log',
    yaxis_type='log',
    template='plotly_dark'
)

st.plotly_chart(fig_log, use_container_width=True)

# Show raw data
if st.checkbox('Show raw data'):
    st.dataframe(df)
