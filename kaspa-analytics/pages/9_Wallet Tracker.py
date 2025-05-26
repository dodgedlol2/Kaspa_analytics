import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Configuration
API_BASE_URL = "https://api.kaspa.org"
st.set_page_config(page_title="Kaspa Address History", page_icon="⛓️", layout="wide")

def safe_get(data, *keys, default=None):
    """Safely get nested dictionary values"""
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
    """Fetch transaction history using the paged endpoint"""
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
        
    response = make_api_request(endpoint, params=params)
    return response

def process_transaction_history(transactions, address):
    """Process transactions into balance timeline"""
    history = []
    balance = 0
    
    if not transactions or not isinstance(transactions, list):
        return history
    
    for tx in transactions:
        tx_data = tx  # The structure is different with the paged endpoint
        if not tx_data:
            continue
            
        inputs = safe_get(tx_data, 'inputs', default=[])
        outputs = safe_get(tx_data, 'outputs', default=[])
        timestamp = safe_get(tx_data, 'block_time', default=None)
        tx_id = safe_get(tx_data, 'transaction_id', default='')
        
        if not timestamp:
            continue
            
        net_change = 0
        
        # Process outputs (receives)
        for out in outputs:
            out_address = safe_get(out, 'script_public_key_address', default='')
            if out_address == address:
                amount = float(safe_get(out, 'amount', default=0)) / 1e8
                net_change += amount
        
        # Process inputs (sends)
        for inp in inputs:
            prev_address = safe_get(inp, 'previous_outpoint_address', default='')
            if prev_address == address:
                amount = float(safe_get(inp, 'previous_outpoint_amount', default=0)) / 1e8
                net_change -= amount
        
        balance += net_change
        history.append({
            'timestamp': timestamp,
            'datetime': format_timestamp(timestamp),
            'balance': balance,
            'net_change': net_change,
            'transaction_id': tx_id,
            'direction': 'in' if net_change > 0 else 'out'
        })
    
    return history

# Main App
st.title("Kaspa Address History Explorer")

st.markdown("""
**How to use:**
1. Enter a valid Kaspa address (starts with `kaspa:`)
2. Set how many transactions to fetch per batch (1-500)
3. Click "Load Transaction History"
""")

address = st.text_input("Kaspa Address:", 
                       value="kaspa:qyp4pmj4u48e2rq3976kjqx4mywlgera8rxufmary5xhwgj6a8c4lkgyxctpu92")

limit = st.number_input("Transactions per batch", 
                      min_value=1, max_value=500, value=50,
                      help="Number of transactions to fetch at once (1-500)")

# Store pagination state in session
if 'pagination_state' not in st.session_state:
    st.session_state.pagination_state = {
        'before': None,
        'after': None,
        'history': []
    }

if st.button("Load Transaction History"):
    if address and address.startswith("kaspa:"):
        with st.spinner(f"Fetching transactions..."):
            # Get current balance
            balance_data = make_api_request(f"/addresses/{address}/balance")
            if not balance_data:
                st.error("Failed to fetch balance data")
                st.stop()
                
            current_balance = float(safe_get(balance_data, 'balance', default=0)) / 1e8
            st.metric("Current Balance", f"{current_balance:,.8f} KAS")
            
            # Get transactions
            transactions = fetch_transactions_page(
                address, 
                limit=limit,
                before=st.session_state.pagination_state['before'],
                after=st.session_state.pagination_state['after']
            )
            
            if not transactions:
                st.warning("No transactions found in API response")
                st.stop()
                
            # Process history
            new_history = process_transaction_history(transactions, address)
            
            if not new_history:
                st.warning("""
                No valid transactions processed. This could mean:
                - The address has no transaction history
                - The transactions don't match our processing logic
                - The API response format changed
                """)
                st.json(transactions[0] if transactions else {})  # Show raw data for debugging
                st.stop()
            
            # Update history and pagination state
            st.session_state.pagination_state['history'].extend(new_history)
            
            # Sort by timestamp (oldest first)
            all_history = sorted(st.session_state.pagination_state['history'], 
                                key=lambda x: x['timestamp'])
            
            # Update pagination markers
            if transactions:
                oldest_tx = min(tx['block_time'] for tx in transactions if 'block_time' in tx)
                newest_tx = max(tx['block_time'] for tx in transactions if 'block_time' in tx)
                st.session_state.pagination_state['before'] = oldest_tx
                st.session_state.pagination_state['after'] = newest_tx
            
            # Create DataFrame
            history_df = pd.DataFrame(all_history)
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'].astype(int), unit='ms')
            history_df = history_df.sort_values('timestamp')
            
            # Visualization
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['balance'],
                    name="Balance",
                    line=dict(color='blue'),
                    fill='tozeroy'
                )
            )
            fig.update_layout(
                title="Balance Over Time",
                xaxis_title="Date",
                yaxis_title="Balance (KAS)",
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Transaction table
            st.subheader("Transaction Details")
            st.dataframe(
                history_df.sort_values('datetime', ascending=False),
                column_config={
                    "datetime": "Date",
                    "net_change": st.column_config.NumberColumn(
                        "Amount", 
                        format="%+.8f KAS",
                        help="Positive = received, Negative = sent"
                    ),
                    "balance": st.column_config.NumberColumn(
                        "Balance", 
                        format="%.8f KAS"
                    ),
                    "transaction_id": "Transaction ID",
                    "direction": "Direction"
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Pagination controls
            st.write("Pagination Controls")
            prev_col, next_col = st.columns(2)
            with prev_col:
                if st.button("◀ Load Older Transactions"):
                    st.session_state.pagination_state['after'] = None
                    st.session_state.pagination_state['before'] = oldest_tx
                    st.experimental_rerun()
            with next_col:
                if st.button("Load Newer Transactions ▶"):
                    st.session_state.pagination_state['before'] = None
                    st.session_state.pagination_state['after'] = newest_tx
                    st.experimental_rerun()
    else:
        st.error("Please enter a valid Kaspa address starting with 'kaspa:'")
