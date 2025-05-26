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
    """Fetch full transaction history using the discovered endpoint"""
    endpoint = f"/addresses/{address}/full-transactions"
    params = {
        "limit": limit,
        "offset": offset,
        "resolve_previous_outpoints": "full"  # Get full input details
    }
    return make_api_request(endpoint, params=params)

def process_transaction_history(transactions, address):
    """Process transactions into balance timeline"""
    balance = 0
    history = []
    
    if not transactions or not isinstance(transactions, list):
        return history
    
    # Sort transactions by timestamp (oldest first)
    sorted_txs = sorted(transactions, key=lambda x: safe_get(x, 'transaction', 'block_time', default=0))
    
    for tx in sorted_txs:
        if not isinstance(tx, dict):
            continue
            
        tx_data = safe_get(tx, 'transaction', default={})
        inputs = safe_get(tx_data, 'inputs', default=[])
        outputs = safe_get(tx_data, 'outputs', default=[])
        timestamp = safe_get(tx_data, 'block_time', default=None)
        tx_id = safe_get(tx_data, 'verboseData', 'transactionId', default='')
        
        if not timestamp:
            continue
            
        # Calculate net change for this address
        net_change = 0
        
        # Check outputs (money received)
        for out in outputs:
            if safe_get(out, 'script_public_key_address', default='') == address:
                amount = float(safe_get(out, 'amount', default=0)) / 1e8  # Convert to KAS
                net_change += amount
        
        # Check inputs (money sent)
        for inp in inputs:
            # Check if this input comes from our address
            prev_out = safe_get(inp, 'previous_outpoint', 'verboseData', 'scriptPublicKeyAddress', default='')
            if prev_out == address:
                amount = float(safe_get(inp, 'previous_outpoint', 'amount', default=0)) / 1e8
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
st.markdown("Complete transaction history using Kaspa API")

address = st.text_input("Enter Kaspa Address:", 
                       value="kaspa:qr6pqdkru9fgwlm8yyqzp7cww9vj7auuq5vratzy4ev3luzj79t5ycvp8euuf")

limit = st.number_input("Transactions per batch", min_value=1, max_value=500, value=50)
offset = st.number_input("Starting offset", min_value=0, value=0)

if st.button("Load Transaction History"):
    if address and address.startswith("kaspa:"):
        with st.spinner(f"Fetching transactions {offset} to {offset+limit}..."):
            # Get current balance first
            balance_data = make_api_request(f"/addresses/{address}/balance")
            if not balance_data:
                st.error("Failed to fetch balance data")
                st.stop()
                
            current_balance = float(safe_get(balance_data, 'balance', default=0)) / 1e8
            st.metric("Current Balance", f"{current_balance:,.8f} KAS")
            
            # Get transaction history
            transactions = fetch_full_transactions(address, limit=limit, offset=offset)
            
            if not transactions:
                st.warning("No transactions found for this address")
                st.stop()
                
            # Process history
            history = process_transaction_history(transactions, address)
            
            if not history:
                st.warning("No valid transactions found")
                st.stop()
                
            # Create DataFrame
            history_df = pd.DataFrame(history)
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'].astype(int), unit='ms')
            history_df = history_df.sort_values('timestamp')
            
            # Create visualization
            fig = go.Figure()
            
            # Add balance line
            fig.add_trace(
                go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['balance'],
                    name="Balance (KAS)",
                    line=dict(color='#4B8BBE'),
                    fill='tozeroy',
                    fillcolor='rgba(75, 139, 190, 0.1)'
                )
            )
            
            # Add transaction markers
            fig.add_trace(
                go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['balance'],
                    mode='markers',
                    name="Transactions",
                    marker=dict(
                        color=history_df['net_change'].apply(lambda x: 'green' if x > 0 else 'red'),
                        size=8,
                        line=dict(width=1, color='DarkSlateGrey')
                    ),
                    hovertext=history_df['net_change'].apply(lambda x: f"{x:+.8f} KAS")
                )
            )
            
            # Update layout
            fig.update_layout(
                title=f"Address Balance History: {address[:15]}...",
                xaxis_title="Date",
                yaxis_title="Balance (KAS)",
                hovermode="x unified",
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show transaction details
            st.subheader("Transaction Details")
            st.dataframe(
                history_df[['datetime', 'net_change', 'balance', 'transaction_id', 'direction']]
                .sort_values('datetime', ascending=False)
                .style.apply(lambda x: ['color: green' if v > 0 else 'color: red' for v in x], subset=['net_change']),
                column_config={
                    "datetime": "Date",
                    "net_change": st.column_config.NumberColumn("Amount", format="%+.8f KAS"),
                    "balance": st.column_config.NumberColumn("Balance", format="%.8f KAS"),
                    "transaction_id": "Transaction ID",
                    "direction": "Direction"
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )
            
            # Pagination controls
            col1, col2 = st.columns(2)
            with col1:
                if offset > 0:
                    if st.button("Previous Page"):
                        offset = max(0, offset - limit)
                        st.experimental_rerun()
            with col2:
                if len(transactions) == limit:
                    if st.button("Next Page"):
                        offset += limit
                        st.experimental_rerun()
    else:
        st.error("Please enter a valid Kaspa address starting with 'kaspa:'")
