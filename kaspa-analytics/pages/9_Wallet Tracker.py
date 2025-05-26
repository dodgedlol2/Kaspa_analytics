import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Configuration
API_BASE_URL = "https://api.kaspa.org"
st.set_page_config(page_title="Kaspa Address History", page_icon="⛓️", layout="wide")

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

def fetch_all_transactions_recursively(address, limit=500):
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

# UI Starts
st.title("Kaspa Address History Explorer")

st.markdown("""
**How to use:**
1. Enter a valid Kaspa address (starts with `kaspa:`)
2. Set how many transactions to fetch per batch (1–500)
3. Click "Load Transaction History" for single page or "Fetch All History" for full recursive history
""")

address = st.text_input("Kaspa Address:", value="kaspa:qyp4pmj4u48e2rq3976kjqx4mywlgera8rxufmary5xhwgj6a8c4lkgyxctpu92")
limit = st.number_input("Transactions per batch", min_value=1, max_value=500, value=50)

# Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_address' not in st.session_state:
    st.session_state.current_address = None

# Reset history on new address
if address != st.session_state.current_address:
    st.session_state.current_address = address
    st.session_state.history = []

def display_results(address, transactions):
    balance_data = make_api_request(f"/addresses/{address}/balance")
    if not balance_data:
        st.error("Could not fetch balance")
        return
    current_balance = float(safe_get(balance_data, 'balance', default=0)) / 1e8
    st.metric("Current Balance", f"{current_balance:,.8f} KAS")

    changes = extract_net_changes(transactions, address)
    txs_by_id = {tx['transaction_id']: tx for tx in changes}
    history = list(txs_by_id.values())

    history_with_balance = compute_balance_from_current(current_balance, history)
    df = pd.DataFrame(history_with_balance)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.sort_values('timestamp')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['balance'],
        name='Balance',
        fill='tozeroy',
        line=dict(color='blue')
    ))
    fig.update_layout(
        title="Balance Over Time",
        xaxis_title="Time",
        yaxis_title="KAS",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

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

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Load Transaction History"):
        with st.spinner("Fetching one page..."):
            tx_page = fetch_transactions_page(address, limit=limit)
            if tx_page:
                st.session_state.history = tx_page
                display_results(address, tx_page)
with col2:
    if st.button("Fetch All History"):
        with st.spinner("Recursively fetching all transactions..."):
            all_txs = fetch_all_transactions_recursively(address)
            if all_txs:
                st.session_state.history = all_txs
                display_results(address, all_txs)
