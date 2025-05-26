import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np
from utils import load_price_data
from tenacity import retry, stop_after_attempt, wait_exponential

# Configuration
API_BASE_URL = "https://api.kaspa.org"
st.set_page_config(page_title="Kaspa Wallet Tracker", page_icon="⛓️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .st-emotion-cache-6qob1r { background-color: #262730 !important; }
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
    .metrics-container {
        width: calc(100% - 40px) !important;
        margin-left: 20px !important;
        margin-right: 20px !important;
        margin-top: 10px !important;
        margin-bottom: 0px !important;
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
    .progress-bar-container {
        margin-bottom: 20px;
    }
    .progress-text {
        font-size: 14px;
        color: #e0e0e0;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

def safe_get(data, *keys, default=None):
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return default

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def make_api_request(endpoint, params=None):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params, timeout=30)
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

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_transactions_page(address, limit=500, before=None, after=None):
    endpoint = f"/addresses/{address}/full-transactions-page"
    params = {
        "limit": limit,
        "resolve_previous_outpoints": "light",
        "acceptance": "accepted"
    }
    if before is not None:
        params["before"] = before
    if after is not None:
        params["after"] = after
    return make_api_request(endpoint, params=params)

def fetch_all_transactions_complete(address, max_transactions=10000, start_date=None, end_date=None):
    """Fetch ALL transactions for an address using reliable sequential requests"""
    all_transactions = []
    seen_ids = set()
    before = None
    limit = 500  # Max allowed by API
    total_fetched = 0
    
    # Convert dates to timestamps if provided
    start_ts = int(datetime.combine(start_date, datetime.min.time()).timestamp() * 1000) if start_date else None
    end_ts = int(datetime.combine(end_date, datetime.max.time()).timestamp() * 1000) if end_date else None
    
    # Create progress container
    progress_container = st.empty()
    
    while True:
        # Update progress
        progress_container.markdown(
            f"""
            <div class="progress-bar-container">
                <div class="progress-text">Fetching transactions... {total_fetched} fetched</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Fetch next batch
        batch = fetch_transactions_page(address, limit=limit, before=before)
        if not batch:
            break
            
        # Filter out duplicates and apply date range
        new_transactions = []
        for tx in batch:
            tx_id = safe_get(tx, 'transaction_id')
            tx_time = safe_get(tx, 'block_time')
            
            if tx_id in seen_ids:
                continue
                
            if start_ts and tx_time and tx_time < start_ts:
                continue
                
            if end_ts and tx_time and tx_time > end_ts:
                continue
                
            new_transactions.append(tx)
            seen_ids.add(tx_id)
        
        if not new_transactions:
            break
            
        # Add to our collection
        all_transactions.extend(new_transactions)
        total_fetched += len(new_transactions)
        
        # Set up for next request
        before = min(tx['block_time'] for tx in new_transactions if 'block_time' in tx)
        
        # Safety check
        if total_fetched >= max_transactions:
            st.warning(f"Reached maximum of {max_transactions} transactions. Some may be missing.")
            break
    
    progress_container.empty()
    
    # Sort by timestamp ascending
    all_transactions.sort(key=lambda x: safe_get(x, 'block_time', 0))
    return all_transactions

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

def fetch_kaspa_price_history():
    """Fetch historical KAS price data"""
    try:
        if 'price_df' not in st.session_state or 'price_genesis_date' not in st.session_state:
            price_df, genesis_date = load_price_data()
            st.session_state.price_df = price_df
            st.session_state.price_genesis_date = genesis_date
        else:
            price_df = st.session_state.price_df
            genesis_date = st.session_state.price_genesis_date
        
        price_history = []
        for index, row in price_df.iterrows():
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

def calculate_average_purchase_price_over_time(transactions, price_history):
    """Calculate average purchase price over time with each transaction"""
    if not price_history or not transactions:
        return None
        
    price_df = pd.DataFrame(price_history)
    price_df['date'] = pd.to_datetime(price_df['timestamp'], unit='ms')
    
    transactions_sorted = sorted(transactions, key=lambda x: x['timestamp'])
    
    total_kas = 0
    total_cost = 0
    avg_price_history = []
    
    for tx in transactions_sorted:
        if tx['direction'] == 'in' and tx['net_change'] > 0:
            tx_date = datetime.fromtimestamp(tx['timestamp']/1000)
            
            price_row = price_df[price_df['date'] <= tx_date].sort_values('date', ascending=False).head(1)
            
            if not price_row.empty:
                price = price_row.iloc[0]['price']
                kas_amount = tx['net_change']
                total_kas += kas_amount
                total_cost += kas_amount * price
                
                if total_kas > 0:
                    current_avg = total_cost / total_kas
                else:
                    current_avg = 0
                
                avg_price_history.append({
                    'timestamp': tx['timestamp'],
                    'datetime': tx['datetime'],
                    'avg_purchase_price': current_avg,
                    'transaction_id': tx['transaction_id'],
                    'kas_amount': kas_amount,
                    'price_at_purchase': price
                })
    
    return avg_price_history

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
    
    # Calculate average purchase price over time
    if st.session_state.avg_price_history is None:
        with st.spinner("Calculating average purchase price history..."):
            st.session_state.avg_price_history = calculate_average_purchase_price_over_time(
                history_with_balance, 
                st.session_state.price_history
            )
    
    avg_price_df = pd.DataFrame(st.session_state.avg_price_history) if st.session_state.avg_price_history else pd.DataFrame()
    if not avg_price_df.empty:
        avg_price_df['timestamp'] = pd.to_datetime(avg_price_df['timestamp'], unit='ms')
    
    # Current average purchase price
    current_avg_price = avg_price_df['avg_purchase_price'].iloc[-1] if not avg_price_df.empty else None
    
    # Create daily balance history
    if not df.empty:
        if st.session_state.price_history:
            first_price_date = pd.to_datetime(min([p['timestamp'] for p in st.session_state.price_history]), unit='ms').date()
        else:
            first_price_date = df['timestamp'].min().date()
            
        min_date = first_price_date
        max_date = df['timestamp'].max().date()
        date_range = pd.date_range(start=min_date, end=max_date, freq='D')
        
        daily_balance = []
        current_balance_val = 0
        tx_idx = 0
        
        for date in date_range:
            while tx_idx < len(df) and df.iloc[tx_idx]['timestamp'].date() <= date.date():
                current_balance_val = df.iloc[tx_idx]['balance']
                tx_idx += 1
            
            daily_balance.append({
                'date': date,
                'balance': current_balance_val
            })
        
        balance_df = pd.DataFrame(daily_balance)
        
        if st.session_state.price_history:
            price_df = pd.DataFrame(st.session_state.price_history)
            price_df['date'] = pd.to_datetime(price_df['timestamp'], unit='ms')
            price_df = price_df[['date', 'price']]
            
            merged_df = pd.merge(balance_df, price_df, on='date', how='left')
            merged_df['price'] = merged_df['price'].ffill().bfill()
            
            if not avg_price_df.empty:
                avg_price_daily = avg_price_df.resample('D', on='timestamp').last().reset_index()
                avg_price_daily = avg_price_daily[['timestamp', 'avg_purchase_price']]
                avg_price_daily = avg_price_daily.rename(columns={'timestamp': 'date'})
                merged_df = pd.merge(merged_df, avg_price_daily, on='date', how='left')
                merged_df['avg_purchase_price'] = merged_df['avg_purchase_price'].ffill()
        else:
            merged_df = balance_df
            merged_df['price'] = np.nan
    
    # Metrics
    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        st.metric("Current Balance", f"{current_balance:,.8f} KAS")
    with cols[1]:
        total_in = df[df['direction'] == 'in']['net_change'].sum()
        st.metric("Total Received", f"{total_in:,.8f} KAS")
    with cols[2]:
        total_out = abs(df[df['direction'] == 'out']['net_change'].sum())
        st.metric("Total Sent", f"{total_out:,.8f} KAS")
    with cols[3]:
        if current_avg_price is not None:
            st.metric("Current Avg Price", f"${current_avg_price:.4f}")
        else:
            st.metric("Current Avg Price", "N/A")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=merged_df['date'],
        y=merged_df['balance'],
        mode='lines',
        name='Balance (KAS)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Balance</b>: %{y:.8f} KAS<extra></extra>'
    ))
    
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
    
    if 'avg_purchase_price' in merged_df and not merged_df['avg_purchase_price'].isna().all():
        fig.add_trace(go.Scatter(
            x=merged_df['date'],
            y=merged_df['avg_purchase_price'],
            mode='lines',
            name='Avg Purchase Price (USD)',
            line=dict(color="#FFA500", width=1.5, dash="dash"),
            hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Avg Price</b>: $%{y:.4f}<extra></extra>',
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
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
        ),
        yaxis=dict(
            type="linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
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
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if not avg_price_df.empty:
        st.subheader("Average Purchase Price History")
        
        avg_fig = go.Figure()
        
        avg_fig.add_trace(go.Scatter(
            x=avg_price_df['timestamp'],
            y=avg_price_df['avg_purchase_price'],
            mode='lines+markers',
            name='Average Purchase Price',
            line=dict(color="#FFA500", width=2),
            marker=dict(size=6, color="#FFA500"),
            hovertemplate='<b>Date</b>: %{x|%Y-%m-%d %H:%M:%S}<br><b>Avg Price</b>: $%{y:.4f}<extra></extra>'
        ))
        
        avg_fig.add_trace(go.Scatter(
            x=avg_price_df['timestamp'],
            y=avg_price_df['price_at_purchase'],
            mode='markers',
            name='Purchase Price at Time',
            marker=dict(size=6, color="#00FFCC"),
            hovertemplate='<b>Date</b>: %{x|%Y-%m-%d %H:%M:%S}<br><b>Price</b>: $%{y:.4f}<extra></extra>'
        ))
        
        avg_fig.update_layout(
            plot_bgcolor='#262730',
            paper_bgcolor='#262730',
            font_color='#e0e0e0',
            hovermode='x unified',
            height=400,
            margin=dict(l=20, r=20, t=40, b=40),
            yaxis_title='Price (USD)',
            xaxis_title='Date',
            showlegend=True
        )
        
        st.plotly_chart(avg_fig, use_container_width=True)
    
    st.subheader("Transaction Details")
    
    if not avg_price_df.empty:
        avg_price_tx = avg_price_df[['transaction_id', 'avg_purchase_price', 'price_at_purchase']]
        df = pd.merge(df, avg_price_tx, on='transaction_id', how='left')
    
    st.dataframe(
        df.sort_values('timestamp', ascending=False),
        column_config={
            "datetime": "Date",
            "net_change": st.column_config.NumberColumn("Amount", format="%+.8f KAS"),
            "balance": st.column_config.NumberColumn("Balance", format="%.8f KAS"),
            "transaction_id": "Transaction ID",
            "direction": "Direction",
            "avg_purchase_price": st.column_config.NumberColumn("Avg Price", format="$%.4f"),
            "price_at_purchase": st.column_config.NumberColumn("Price at Tx", format="$%.4f")
        },
        hide_index=True,
        use_container_width=True
    )

# UI Starts
st.markdown('<div class="title-spacing"><h2>Kaspa Wallet Tracker</h2></div>', unsafe_allow_html=True)
st.divider()

# Address input
address = st.text_input("Kaspa Address:", value="kaspa:qyp4pmj4u48e2rq3976kjqx4mywlgera8rxufmary5xhwgj6a8c4lkgyxctpu92")

# Filters
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", datetime.now() - timedelta(days=365))
with col2:
    end_date = st.date_input("End date", datetime.now())

max_txs = st.slider("Maximum transactions to fetch", 100, 20000, 5000, step=100)

# Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_address' not in st.session_state:
    st.session_state.current_address = None
if 'price_history' not in st.session_state:
    st.session_state.price_history = None
if 'avg_price_history' not in st.session_state:
    st.session_state.avg_price_history = None

# Reset history on new address
if address != st.session_state.current_address:
    st.session_state.current_address = address
    st.session_state.history = []
    st.session_state.avg_price_history = None

# Main button
if st.button("Fetch Full History", type="primary"):
    if not address.startswith('kaspa:'):
        st.error("Please enter a valid Kaspa address starting with 'kaspa:'")
    else:
        with st.spinner("Initializing transaction fetch..."):
            all_txs = fetch_all_transactions_complete(
                address, 
                max_transactions=max_txs,
                start_date=start_date,
                end_date=end_date
            )
            if all_txs:
                st.session_state.history = all_txs
                st.session_state.avg_price_history = None
                display_results(address, all_txs)
                st.success(f"Successfully fetched {len(all_txs)} transactions")
            else:
                st.error("No transactions found or failed to fetch")

# Display cached results if available
if st.session_state.history and st.session_state.current_address == address:
    display_results(address, st.session_state.history)
