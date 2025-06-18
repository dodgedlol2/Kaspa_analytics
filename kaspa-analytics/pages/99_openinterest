import streamlit as st
import plotly.graph_objects as go
import pandas as pd

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

# Convert date strings to datetime
df['date'] = pd.to_datetime(df['date'])
df['days_from_start'] = (df['date'] - df['date'].min()).dt.days + 1  # +1 to avoid log(0)

# Create log-log plot
st.title('Open Interest Log-Log Plot')
st.markdown('### Open Interest vs. Time (Log-Log Scale)')

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['days_from_start'],
    y=df['openinterest'],
    mode='lines+markers',
    name='Open Interest',
    text=df['date'].dt.strftime('%b %d %Y'),
    hovertemplate='Date: %{text}<br>Days from start: %{x}<br>Open Interest: %{y}'
))

# Set log scale on both axes
fig.update_layout(
    xaxis_type='log',
    yaxis_type='log',
    xaxis_title='Days from start (log scale)',
    yaxis_title='Open Interest (log scale)',
    hovermode='x unified',
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

# Show raw data if desired
if st.checkbox('Show raw data'):
    st.dataframe(df[['date', 'openinterest']])
