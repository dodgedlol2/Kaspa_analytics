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
    current_balance = 0
    
    if not transactions or not isinstance(transactions, list):
        return history
    
    # First pass: Calculate current balance by summing all outputs and subtracting inputs
    for tx in reversed(transactions):  # Process from newest to oldest
        inputs = safe_get(tx, 'inputs', default=[])
        outputs = safe_get(tx, 'outputs', default=[])
        
        for out in outputs:
            out_address = safe_get(out, 'script_public_key_address', default='')
            if out_address == address:
                current_balance += float(safe_get(out, 'amount', default=0)) / 1e8
        
        for inp in inputs:
            prev_address = safe_get(inp, 'previous_outpoint_address', default='')
            if prev_address == address:
                current_balance -= float(safe_get(inp, 'previous_outpoint_amount', default=0)) / 1e8
    
    # Second pass: Build history by working backwards
    for tx in reversed(transactions):
        tx_data = tx
        if not tx_data:
            continue
            
        inputs = safe_get(tx_data, 'inputs', default=[])
        outputs = safe_get(tx_data, 'outputs', default=[])
        timestamp = safe_get(tx_data, 'block_time', default=None)
        tx_id = safe_get(tx_data, 'transaction_id', default='')
        
        if not timestamp:
            continue
            
        # Calculate net change for this transaction
        net_change = 0
        
        # Subtract outputs first (since we're working backwards)
        for out in outputs:
            out_address = safe_get(out, 'script_public_key_address', default='')
            if out_address == address:
                amount = float(safe_get(out, 'amount', default=0)) / 1e8
                net_change -= amount
                current_balance -= amount
        
        # Add inputs (since we're working backwards)
        for inp in inputs:
            prev_address = safe_get(inp, 'previous_outpoint_address', default='')
            if prev_address == address:
                amount = float(safe_get(inp, 'previous_outpoint_amount', default=0)) / 1e8
                net_change += amount
                current_balance += amount
        
        history.append({
            'timestamp': timestamp,
            'datetime': format_timestamp(timestamp),
            'balance': current_balance,
            'net_change': net_change,
            'transaction_id': tx_id,
            'direction': 'in' if net_change > 0 else 'out'
        })
    
    # Reverse to show oldest first
    return list(reversed(history))

# Main App
st.title("Kaspa Address History Explorer")

st.markdown("""
**How to use:**
1. Enter a valid Kaspa address (starts with `kaspa:`)
2. Set how many transactions to fetch per batch (1-500)
3. Click "Load Transaction History"
""")

# Use the preferred example address
address = st.text_input("Kaspa Address:", 
                       value="kaspa:qypaf4exd6qkf7mw9zy8saaawvnc44fusnsdy4azq0xss9adj4387vqr6k865vk")

limit = st.number_input("Transactions per batch", 
                      min_value=1, max_value=500, value=50,
                      help="Number of transactions to fetch at once (1-500)")

# Initialize session state
if 'current_address' not in st.session_state:
    st.session_state.current_address = None
    st.session_state.pagination_state = {
        'before': None,
        'after': None,
        'history': []
    }

# Reset pagination if address changes
if address != st.session_state.current_address:
    st.session_state.current_address = address
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
                st.json(transactions[0] if transactions else {})
                st.stop()
            
            # Update history and pagination state
            st.session_state.pagination_state['history'].extend(new_history)
            
            # Get timestamps for pagination
            timestamps = [tx['block_time'] for tx in transactions if 'block_time' in tx]
            if timestamps:
                oldest_tx = min(timestamps)
                newest_tx = max(timestamps)
                st.session_state.pagination_state['before'] = oldest_tx
                st.session_state.pagination_state['after'] = newest_tx
            
            # Create DataFrame from all history
            all_history = st.session_state.pagination_state['history']
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
                    line=dict(color='#00FFCC'),
                    fill='tozeroy',
                    hovertemplate='Date: %{x|%Y-%m-%d}<br>Balance: %{y:,.2f} KAS<extra></extra>'
                )
            )
            fig.update_layout(
                title="Balance Over Time",
                xaxis_title="Date",
                yaxis_title="Balance (KAS)",
                hovermode="x unified",
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='white')
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
                    "transaction_id": st.column_config.LinkColumn(
                        "Transaction ID",
                        help="Link to Kaspa Explorer",
                        display_text="View on Explorer",
                        url="https://explorer.kaspa.org/txs/{transaction_id}"
                    ),
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
                    st.experimental_rerun()
            with next_col:
                if st.button("Load Newer Transactions ▶"):
                    st.session_state.pagination_state['before'] = None
                    st.experimental_rerun()
    else:
        st.error("Please enter a valid Kaspa address starting with 'kaspa:'")
