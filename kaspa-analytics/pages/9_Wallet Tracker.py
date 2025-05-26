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

def fetch_full_transactions(address, limit=50, offset=0):
    """Fetch full transaction history"""
    endpoint = f"/addresses/{address}/full-transactions"
    params = {
        "limit": limit,
        "offset": offset,
        "resolve_previous_outpoints": "full"
    }
    return make_api_request(endpoint, params=params)

def process_transaction_history(transactions, address):
    """Process transactions into balance timeline"""
    history = []
    balance = 0
    
    if not transactions or not isinstance(transactions, list):
        return history
    
    for tx in transactions:
        if not isinstance(tx, dict):
            continue
            
        tx_id = safe_get(tx, 'transaction_id')
        block_time = safe_get(tx, 'block_time')
        inputs = safe_get(tx, 'inputs', [])
        outputs = safe_get(tx, 'outputs', [])
        
        if not block_time:
            continue
            
        net_change = 0
        
        # Process outputs (receives)
        for out in outputs:
            out_address = safe_get(out, 'script_public_key_address', '')
            if out_address == address:
                amount = float(safe_get(out, 'amount', 0)) / 1e8
                net_change += amount
        
        # Process inputs (sends)
        for inp in inputs:
            prev_address = safe_get(inp, 'previous_outpoint_address', '')
            if prev_address == address:
                amount = float(safe_get(inp, 'previous_outpoint_amount', 0)) / 1e8
                net_change -= amount
        
        balance += net_change
        history.append({
            'timestamp': block_time,
            'datetime': format_timestamp(block_time),
            'balance': balance,
            'net_change': net_change,
            'transaction_id': tx_id,
            'direction': 'in' if net_change > 0 else 'out'
        })
    
    return history

# Main App
st.title("Kaspa Address History Explorer")

address = st.text_input("Kaspa Address:", 
                       value="kaspa:qyp4pmj4u48e2rq3976kjqx4mywlgera8rxufmary5xhwgj6a8c4lkgyxctpu92")

limit = st.number_input("Transactions per batch", min_value=1, max_value=500, value=50)
offset = st.number_input("Starting offset", min_value=0, value=0)

if st.button("Load Transaction History"):
    if address and address.startswith("kaspa:"):
        with st.spinner(f"Fetching transactions {offset} to {offset+limit}..."):
            # Get current balance
            balance_data = make_api_request(f"/addresses/{address}/balance")
            if not balance_data:
                st.error("Failed to fetch balance data")
                st.stop()
                
            current_balance = float(safe_get(balance_data, 'balance', 0)) / 1e8
            st.metric("Current Balance", f"{current_balance:,.8f} KAS")
            
            # Get transactions
            transactions = fetch_full_transactions(address, limit=limit, offset=offset)
            
            if not transactions:
                st.warning("No transactions found in API response")
                st.stop()
                
            # Process history
            history = process_transaction_history(transactions, address)
            
            if not history:
                st.warning("No balance-changing transactions found for this address")
                st.stop()
                
            # Create DataFrame
            history_df = pd.DataFrame(history)
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
                        format="%+.8f KAS"
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
            
            # Pagination
            st.write("Pagination Controls")
            prev_col, next_col = st.columns(2)
            with prev_col:
                if offset > 0:
                    if st.button("◀ Previous Page"):
                        offset = max(0, offset - limit)
                        st.experimental_rerun()
            with next_col:
                if len(transactions) == limit:
                    if st.button("Next Page ▶"):
                        offset += limit
                        st.experimental_rerun()
    else:
        st.error("Please enter a valid Kaspa address starting with 'kaspa:'")
