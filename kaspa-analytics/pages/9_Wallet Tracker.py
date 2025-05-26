import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
from utils import load_price_data

# Configuration
API_BASE_URL = "https://api.kaspa.org"
st.set_page_config(page_title="Kaspa Address History", page_icon="⛓️", layout="wide")

# Custom CSS - matching the second page's style
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
    .stDataFrame {
        background-color: #262730 !important;
        border: 1px solid #3A3C4A !important;
        border-radius: 8px !important;
    }
    .stDataFrame th {
        background-color: #3A3C4A !important;
        color: #e0e0e0 !important;
    }
    .stDataFrame td {
        background-color: #262730 !important;
        color: #e0e0e0 !important;
    }
    .stButton button {
        background-color: #262730 !important;
        color: #e0e0e0 !important;
        border: 1px solid #3A3C4A !important;
        border-radius: 4px !important;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        border-color: #00FFCC !important;
        color: #00FFCC !important;
    }
    .stTextInput input {
        background-color: #262730 !important;
        color: #e0e0e0 !important;
        border: 1px solid #3A3C4A !important;
        border-radius: 4px !important;
    }
    .stNumberInput input {
        background-color: #262730 !important;
        color: #e0e0e0 !important;
        border: 1px solid #3A3C4A !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

def safe_get(data, *keys, default=None):
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return data

def make_api_request(endpoint, params=None):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None

def format_timestamp(timestamp_ms):
    try:
        if isinstance(timestamp_ms, (int, float, str)):
            if isinstance(timestamp_ms, str) and timestamp_ms.isdigit():
                timestamp_ms = int(timestamp_ms)
            return datetime.fromtimestamp(int(timestamp_ms)/1000).strftime('%Y-%m-%d %H:%M:%S')
        return "N/A"
    except:
        return "N/A"

def fetch_transactions_page(address, limit=50, before=None):
    endpoint = f"/addresses/{address}/full-transactions-page"
    params = {
        "limit": limit,
        "resolve_previous_outpoints": "light",
        "acceptance": "accepted"
    }
    if before is not None:
        params["before"] = before
    return make_api_request(endpoint, params=params)

def extract_net_changes(transactions, address):
    history = []
    for tx in transactions:
        inputs = safe_get(tx, 'inputs', default=[])
        outputs = safe_get(tx, 'outputs', default=[])
        timestamp = safe_get(tx, 'block_time', default=None)
        tx_id = safe_get(tx, 'transaction_id', default='')

        if not timestamp:
            continue

        net_change = 0
        for out in outputs:
            out_address = safe_get(out, 'script_public_key_address', default='')
            if out_address == address:
                amount = float(safe_get(out, 'amount', default=0)) / 1e8
                net_change += amount

        for inp in inputs:
            in_address = safe_get(inp, 'previous_outpoint_address', default='')
            if in_address == address:
                amount = float(safe_get(inp, 'previous_outpoint_amount', default=0)) / 1e8
                net_change -= amount

        history.append({
            'timestamp': timestamp,
            'datetime': format_timestamp(timestamp),
            'net_change': net_change,
            'transaction_id': tx_id,
            'direction': 'in' if net_change > 0 else 'out'
        })

    return history

def compute_balance_from_current(current_balance, history):
    history = sorted(history, key=lambda x: x['timestamp'], reverse=True)
    balance = current_balance
    for tx in history:
        tx['balance'] = balance
        balance -= tx['net_change']
    return history[::-1]

def fetch_all_transactions(address, limit=500):
    all_transactions = []
    seen_ids = set()
    before = None

    while True:
        tx_batch = fetch_transactions_page(address, limit=limit, before=before)
        if not tx_batch:
            break

        new_tx = [tx for tx in tx_batch if safe_get(tx, 'transaction_id') not in seen_ids]
        if not new_tx:
            break

        all_transactions.extend(new_tx)
        seen_ids.update(safe_get(tx, 'transaction_id') for tx in new_tx)
        before = min([safe_get(tx, 'block_time') for tx in new_tx if safe_get(tx, 'block_time')])

    return all_transactions

def fetch_kaspa_price_history():
    """Fetch historical KAS price data from Google Sheets"""
    try:
        # Use the existing price data loading mechanism
        if 'price_df' not in st.session_state or 'price_genesis_date' not in st.session_state:
            price_df, genesis_date = load_price_data()
            st.session_state.price_df = price_df
            st.session_state.price_genesis_date = genesis_date
        else:
            price_df = st.session_state.price_df
            genesis_date = st.session_state.price_genesis_date
        
        # Convert to the format expected by the rest of the code
        price_history = []
        for index, row in price_df.iterrows():
            # Convert date to timestamp in milliseconds
            timestamp = int(row['Date'].timestamp() * 1000)
            price_history.append({
                'timestamp': timestamp,
                'datetime': row['Date'].strftime('%Y-%m-%d'),
                'price': row['Price']
            })
        
        return price_history
    except Exception as e:
        st.error(f"Failed to fetch price history: {str(e)}")
        return None

# UI Starts
st.markdown('<div class="title-spacing"><h2>Kaspa Address History Explorer</h2></div>', unsafe_allow_html=True)
st.divider()

st.markdown("""
**How to use:**
1. Enter a valid Kaspa address (starts with `kaspa:`)
2. Set how many transactions to fetch per batch (1-500)
3. Click "Fetch Full History" to load all transactions
""")

address = st.text_input("Kaspa Address:", value="kaspa:qyp4pmj4u48e2rq3976kjqx4mywlgera8rxufmary5xhwgj6a8c4lkgyxctpu92")
limit = st.number_input("Transactions per batch", min_value=1, max_value=500, value=50)

# Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_address' not in st.session_state:
    st.session_state.current_address = None
if 'price_history' not in st.session_state:
    st.session_state.price_history = None

# Reset history on new address
if address != st.session_state.current_address:
    st.session_state.current_address = address
    st.session_state.history = []

def display_results(address, transactions):
    # Fetch current balance
    balance_data = make_api_request(f"/addresses/{address}/balance")
    if not balance_data:
        st.error("Could not fetch balance")
        return
    current_balance = float(safe_get(balance_data, 'balance', default=0)) / 1e8
    
    # Fetch price history if not already loaded
    if st.session_state.price_history is None:
        with st.spinner("Fetching price history..."):
            st.session_state.price_history = fetch_kaspa_price_history()
    
    # Process transactions
    changes = extract_net_changes(transactions, address)
    txs_by_id = {tx['transaction_id']: tx for tx in changes}
    history = list(txs_by_id.values())
    history_with_balance = compute_balance_from_current(current_balance, history)
    
    # Create DataFrame
    df = pd.DataFrame(history_with_balance)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.sort_values('timestamp')
    
    # Create daily balance history
    if not df.empty:
        min_date = df['timestamp'].min().date()
        max_date = df['timestamp'].max().date()
        date_range = pd.date_range(start=min_date, end=max_date, freq='D')
        
        daily_balance = []
        current_balance_val = 0
        tx_idx = 0
        
        for date in date_range:
            # Apply all transactions up to this date
            while tx_idx < len(df) and df.iloc[tx_idx]['timestamp'].date() <= date.date():
                current_balance_val = df.iloc[tx_idx]['balance']
                tx_idx += 1
            
            daily_balance.append({
                'date': date,
                'balance': current_balance_val
            })
        
        balance_df = pd.DataFrame(daily_balance)
        
        # Merge with price data if available
        if st.session_state.price_history:
            price_df = pd.DataFrame(st.session_state.price_history)
            price_df['date'] = pd.to_datetime(price_df['datetime'])
            price_df = price_df[['date', 'price']]
            
            merged_df = pd.merge(balance_df, price_df, on='date', how='left')
            merged_df['price'] = merged_df['price'].ffill().bfill()
        else:
            merged_df = balance_df
            merged_df['price'] = np.nan
    
    # Metrics
    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.metric("Current Balance", f"{current_balance:,.8f} KAS")
    with cols[1]:
        total_in = df[df['direction'] == 'in']['net_change'].sum()
        st.metric("Total Received", f"{total_in:,.8f} KAS")
    with cols[2]:
        total_out = abs(df[df['direction'] == 'out']['net_change'].sum())
        st.metric("Total Sent", f"{total_out:,.8f} KAS")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chart
    fig = go.Figure()
    
    # Add balance trace (primary y-axis)
    fig.add_trace(go.Scatter(
        x=merged_df['date'],
        y=merged_df['balance'],
        mode='lines',
        name='Balance (KAS)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Balance</b>: %{y:.8f} KAS<extra></extra>'
    ))
    
    # Add price trace (secondary y-axis) if available
    if 'price' in merged_df and not merged_df['price'].isna().all():
        fig.add_trace(go.Scatter(
            x=merged_df['date'],
            y=merged_df['price'],
            mode='lines',
            name='Price (USD)',
            line=dict(color='rgba(150, 150, 150, 0.7)', width=1.2),
            hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>',
            yaxis='y2'
        ))
    
    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=600,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Balance (KAS)',
        xaxis_title='Date',
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.1,
                bgcolor='#262730',
                bordercolor="#3A3C4A",
                borderwidth=1
            ),
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
            type="linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            minor=dict(
                ticklen=6,
                gridcolor='rgba(255, 255, 255, 0.05)',
                gridwidth=0.5
            ),
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A',
            color='#00FFCC'
        ),
        yaxis2=dict(
            title='Price (USD)',
            overlaying='y',
            side='right',
            showgrid=False,
            linecolor='rgba(150, 150, 150, 0.5)',
            zeroline=False,
            color='rgba(150, 150, 150, 0.7)'
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
    
    # Transaction details
    st.subheader("Transaction Details")
    st.dataframe(
        df.sort_values('timestamp', ascending=False),
        column_config={
            "datetime": "Date",
            "net_change": st.column_config.NumberColumn("Amount", format="%+.8f KAS"),
            "balance": st.column_config.NumberColumn("Balance", format="%.8f KAS"),
            "transaction_id": "Transaction ID",
            "direction": "Direction"
        },
        hide_index=True,
        use_container_width=True
    )

# Main button
if st.button("Fetch Full History"):
    with st.spinner("Fetching all transactions (this may take a while)..."):
        all_txs = fetch_all_transactions(address, limit=limit)
        if all_txs:
            st.session_state.history = all_txs
            display_results(address, all_txs)
