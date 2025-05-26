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

def fetch_transactions_page(address, limit=50, before=None, after=None):
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

def extract_net_changes(transactions, address):
    """Extract net changes (without calculating balance)"""
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
    """Given current balance and net_changes in reverse order, compute full balance history"""
    # Reverse the list so we subtract net_changes backward in time
    history = sorted(history, key=lambda x: x['timestamp'], reverse=True)

    balance = current_balance
    for tx in history:
        tx['balance'] = balance
        balance -= tx['net_change']
    return history[::-1]  # Return in chronological order

# Main App
st.title("Kaspa Address History Explorer")

st.markdown("""
**How to use:**
1. Enter a valid Kaspa address (starts with `kaspa:`)
2. Set how many transactions to fetch per batch (1–500)
3. Click "Load Transaction History"
""")

address = st.text_input("Kaspa Address:", value="kaspa:qyp4pmj4u48e2rq3976kjqx4mywlgera8rxufmary5xhwgj6a8c4lkgyxctpu92")
limit = st.number_input("Transactions per batch", min_value=1, max_value=500, value=50)

# Session State Init
if 'current_address' not in st.session_state:
    st.session_state.current_address = None
    st.session_state.pagination_state = {
        'before': None,
        'after': None,
        'history': []
    }

# Reset if new address
if address != st.session_state.current_address:
    st.session_state.current_address = address
    st.session_state.pagination_state = {
        'before': None,
        'after': None,
        'history': []
    }

if st.button("Load Transaction History"):
    if address and address.startswith("kaspa:"):
        with st.spinner("Fetching data..."):
            # Get current balance
            balance_data = make_api_request(f"/addresses/{address}/balance")
            if not balance_data:
                st.error("Could not fetch balance")
                st.stop()
            current_balance = float(safe_get(balance_data, 'balance', default=0)) / 1e8
            st.metric("Current Balance", f"{current_balance:,.8f} KAS")

            transactions = fetch_transactions_page(
                address,
                limit=limit,
                before=st.session_state.pagination_state['before'],
                after=st.session_state.pagination_state['after']
            )

            if not transactions:
                st.warning("No transactions returned")
                st.stop()

            # Get timestamps for pagination
            timestamps = [safe_get(tx, 'block_time') for tx in transactions]
            if timestamps:
                st.session_state.pagination_state['before'] = min(timestamps)
                st.session_state.pagination_state['after'] = max(timestamps)

            # Process transactions
            new_changes = extract_net_changes(transactions, address)
            st.session_state.pagination_state['history'].extend(new_changes)

            # De-duplicate by transaction ID
            unique_history = {tx['transaction_id']: tx for tx in st.session_state.pagination_state['history']}
            all_history = list(unique_history.values())

            # Recompute balances from current balance
            history_with_balance = compute_balance_from_current(current_balance, all_history)

            df = pd.DataFrame(history_with_balance)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.sort_values('timestamp')

            # Plot
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

            # Table
            st.subheader("Transaction Details")
            st.dataframe(
                df.sort_values('timestamp', ascending=False),
                column_config={
                    "datetime": "Date",
                    "net_change": st.column_config.NumberColumn(
                        "Amount", format="%+.8f KAS"
                    ),
                    "balance": st.column_config.NumberColumn(
                        "Balance", format="%.8f KAS"
                    ),
                    "transaction_id": "Transaction ID",
                    "direction": "Direction"
                },
                hide_index=True,
                use_container_width=True
            )

            # Pagination
            st.write("Pagination Controls")
            prev_col, next_col = st.columns(2)
            with prev_col:
                if st.button("◀ Load Older Transactions"):
                    st.session_state.pagination_state['after'] = None
                    st.experimental_rerun()
            with next_col:
                if st.button("Load Newer Transactions ▶"):
                    st.session_state.pagination_state['before'] = None
                    st.experimental_rerun()
    else:
        st.error("Please enter a valid Kaspa address starting with 'kaspa:'")

