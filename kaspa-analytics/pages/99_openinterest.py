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

def create_analysis(genesis_date_str, title_suffix):
    # Set genesis date
    genesis_date = pd.to_datetime(genesis_date_str)
    df_temp = df.copy()
    df_temp['days_from_genesis'] = (df_temp['date'] - genesis_date).dt.days
    
    # Remove negative days (before genesis)
    df_temp = df_temp[df_temp['days_from_genesis'] >= 0]
    
    # Calculate power-law
    a, b, r2, x_data, y_data = calculate_powerlaw(
        df_temp['days_from_genesis'].values,
        df_temp['openinterest'].values
    )
    
    return df_temp, a, b, r2, x_data, y_data, genesis_date

# Streamlit app
st.title('Open Interest Power-Law Analysis')

# Analysis 1: Genesis date 2021-11-07
st.markdown("""
### Power-law fit for open interest over time (Genesis: 2021-11-07)
""")

df1, a1, b1, r2_1, x_data1, y_data1, genesis_date1 = create_analysis('2021-11-07', '1')

# Show parameters for first analysis
col1, col2, col3 = st.columns(3)
col1.metric("Power-law exponent (slope)", f"{b1:.3f}")
col2.metric("Coefficient (a)", f"{a1:.3f}")
col3.metric("R² score", f"{r2_1:.3f}")

# Create plot for first analysis
fig1 = go.Figure()

# Add actual data
fig1.add_trace(go.Scatter(
    x=df1['date'],
    y=df1['openinterest'],
    mode='lines+markers',
    name='Open Interest',
    line=dict(color='#00FFCC')
))

# Add power-law fit
x_fit1 = np.linspace(min(x_data1), max(x_data1), 100)
y_fit1 = a1 * np.power(x_fit1, b1)
fit_dates1 = [genesis_date1 + pd.Timedelta(days=int(d)) for d in x_fit1]

fig1.add_trace(go.Scatter(
    x=fit_dates1,
    y=y_fit1,
    mode='lines',
    name='Power-Law Fit',
    line=dict(color='orange', dash='dot')
))

# Add deviation bands
fig1.add_trace(go.Scatter(
    x=fit_dates1,
    y=y_fit1 * 0.4,  # -60%
    mode='lines',
    name='Lower Bound (-60%)',
    line=dict(color='lightgray', dash='dot')
))

fig1.add_trace(go.Scatter(
    x=fit_dates1,
    y=y_fit1 * 2.2,  # +120%
    mode='lines',
    name='Upper Bound (+120%)',
    line=dict(color='lightgray', dash='dot')
))

# Update layout
fig1.update_layout(
    xaxis_title='Date',
    yaxis_title='Open Interest',
    yaxis_type='log',
    template='plotly_dark',
    hovermode='x unified',
    title='Genesis: 2021-11-07'
)

st.plotly_chart(fig1, use_container_width=True)

# Analysis 2: Genesis date 2022-11-28
st.markdown("""
### Power-law fit for open interest over time (Genesis: 2022-11-28)
""")

df2, a2, b2, r2_2, x_data2, y_data2, genesis_date2 = create_analysis('2022-11-28', '2')

# Show parameters for second analysis
col1, col2, col3 = st.columns(3)
col1.metric("Power-law exponent (slope)", f"{b2:.3f}")
col2.metric("Coefficient (a)", f"{a2:.3f}")
col3.metric("R² score", f"{r2_2:.3f}")

# Create plot for second analysis
fig2 = go.Figure()

# Add actual data
fig2.add_trace(go.Scatter(
    x=df2['date'],
    y=df2['openinterest'],
    mode='lines+markers',
    name='Open Interest',
    line=dict(color='#00FFCC')
))

# Add power-law fit
x_fit2 = np.linspace(min(x_data2), max(x_data2), 100)
y_fit2 = a2 * np.power(x_fit2, b2)
fit_dates2 = [genesis_date2 + pd.Timedelta(days=int(d)) for d in x_fit2]

fig2.add_trace(go.Scatter(
    x=fit_dates2,
    y=y_fit2,
    mode='lines',
    name='Power-Law Fit',
    line=dict(color='orange', dash='dot')
))

# Add deviation bands
fig2.add_trace(go.Scatter(
    x=fit_dates2,
    y=y_fit2 * 0.4,  # -60%
    mode='lines',
    name='Lower Bound (-60%)',
    line=dict(color='lightgray', dash='dot')
))

fig2.add_trace(go.Scatter(
    x=fit_dates2,
    y=y_fit2 * 2.2,  # +120%
    mode='lines',
    name='Upper Bound (+120%)',
    line=dict(color='lightgray', dash='dot')
))

# Update layout
fig2.update_layout(
    xaxis_title='Date',
    yaxis_title='Open Interest',
    yaxis_type='log',
    template='plotly_dark',
    hovermode='x unified',
    title='Genesis: 2022-11-28'
)

st.plotly_chart(fig2, use_container_width=True)

# Comparison section
st.markdown("### Comparison of Both Genesis Dates")

comparison_data = {
    'Genesis Date': ['2021-11-07', '2022-11-28'],
    'Power-law Exponent (b)': [f"{b1:.3f}", f"{b2:.3f}"],
    'Coefficient (a)': [f"{a1:.3f}", f"{a2:.3f}"],
    'R² Score': [f"{r2_1:.3f}", f"{r2_2:.3f}"],
    'Data Points': [len(df1), len(df2)]
}

comparison_df = pd.DataFrame(comparison_data)
st.table(comparison_df)

# Log-log plots
st.markdown("### Log-log plots comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Genesis: 2021-11-07")
    fig_log1 = go.Figure()
    
    fig_log1.add_trace(go.Scatter(
        x=x_data1,
        y=y_data1,
        mode='markers',
        name='Actual Data',
        marker=dict(color='#00FFCC')
    ))
    
    fig_log1.add_trace(go.Scatter(
        x=x_fit1,
        y=y_fit1,
        mode='lines',
        name='Power-Law Fit',
        line=dict(color='orange')
    ))
    
    fig_log1.update_layout(
        xaxis_title='Days from Genesis (log scale)',
        yaxis_title='Open Interest (log scale)',
        xaxis_type='log',
        yaxis_type='log',
        template='plotly_dark',
        height=400
    )
    
    st.plotly_chart(fig_log1, use_container_width=True)

with col2:
    st.markdown("#### Genesis: 2022-11-28")
    fig_log2 = go.Figure()
    
    fig_log2.add_trace(go.Scatter(
        x=x_data2,
        y=y_data2,
        mode='markers',
        name='Actual Data',
        marker=dict(color='#00FFCC')
    ))
    
    fig_log2.add_trace(go.Scatter(
        x=x_fit2,
        y=y_fit2,
        mode='lines',
        name='Power-Law Fit',
        line=dict(color='orange')
    ))
    
    fig_log2.update_layout(
        xaxis_title='Days from Genesis (log scale)',
        yaxis_title='Open Interest (log scale)',
        xaxis_type='log',
        yaxis_type='log',
        template='plotly_dark',
        height=400
    )
    
    st.plotly_chart(fig_log2, use_container_width=True)

# Show raw data
if st.checkbox('Show raw data'):
    st.markdown("#### Data with Genesis: 2021-11-07")
    st.dataframe(df1)
    st.markdown("#### Data with Genesis: 2022-11-28")
    st.dataframe(df2)
