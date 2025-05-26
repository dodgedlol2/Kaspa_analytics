import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration
API_BASE_URL = "https://api.kaspa.org"
st.set_page_config(page_title="Kaspa Address History", page_icon="⛓️", layout="wide")

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

def safe_get(data, *keys, default=None):
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return data

def fetch_address_utxos(address):
    """Fetch all UTXOs for an address"""
    endpoint = f"/addresses/{address}/utxos"
    data = make_api_request(endpoint)
    if not data or not isinstance(data, list):
        return None
    return data

def fetch_transaction(tx_id):
    """Fetch full transaction details"""
    endpoint = f"/transactions/{tx_id}"
    return make_api_request(endpoint)

def reconstruct_address_history(address):
    """Reconstruct address history by analyzing UTXOs and their transactions"""
    utxos = fetch_address_utxos(address)
    if not utxos:
        return None
    
    history = []
    balance = 0
    
    # Process each UTXO to find the transactions that created them
    for utxo in utxos:
        if not isinstance(utxo, dict):
            continue
            
        tx_id = safe_get(utxo, 'transactionId', default=None)
        if not tx_id:
            continue
            
        # Get the transaction that created this UTXO
        tx = fetch_transaction(tx_id)
        if not tx:
            continue
            
        # Find our address in the outputs
        outputs = safe_get(tx, 'outputs', default=[])
        for out in outputs:
            if safe_get(out, 'script_public_key_address', default='') == address:
                amount = float(safe_get(out, 'amount', default=0)) / 1e8
                timestamp = safe_get(tx, 'block_time', default=None)
                
                if timestamp:
                    balance += amount
                    history.append({
                        'timestamp': timestamp,
                        'datetime': format_timestamp(timestamp),
                        'balance': balance,
                        'amount': amount,
                        'transaction_id': tx_id,
                        'direction': 'in'
                    })
    
    # Now try to find transactions where this address was the sender (inputs)
    # This is more complex and may require additional API endpoints
    
    # Sort by timestamp
    if history:
        history = sorted(history, key=lambda x: x['timestamp'])
    
    return history

def fetch_kaspa_price_history():
    """Fetch simplified price history (placeholder)"""
    # In production, replace with actual API call to CoinGecko or similar
    return [
        {'timestamp': int((datetime.now().timestamp() - i*86400)*1000), 'price': 0.05 + i*0.001}
        for i in range(30)
    ]

# Main App
st.title("Kaspa Address History Explorer")
st.markdown("Visualize address balance history by analyzing UTXOs")

address = st.text_input("Enter Kaspa Address:", 
                       value="kaspa:qqkqkzjvr7zwxxmjxjkmxxdwju9kjs6e9u82uh59z07vgaks6gg62v8707g73")

if st.button("Analyze Address History"):
    if address and address.startswith("kaspa:"):
        with st.spinner("Reconstructing address history from UTXOs..."):
            # First check balance
            balance_data = make_api_request(f"/addresses/{address}/balance")
            if not balance_data:
                st.error("Could not fetch address balance")
                st.stop()
            
            current_balance = float(safe_get(balance_data, 'balance', default=0)) / 1e8
            st.metric("Current Balance", f"{current_balance:,.8f} KAS")
            
            # Reconstruct history
            history = reconstruct_address_history(address)
            
            if not history:
                st.warning("No transaction history could be reconstructed")
                st.stop()
                
            # Create DataFrame
            history_df = pd.DataFrame(history)
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'].astype(int), unit='ms')
            history_df = history_df.sort_values('timestamp')
            
            # Get price history
            price_history = fetch_kaspa_price_history()
            price_df = pd.DataFrame(price_history)
            if 'timestamp' in price_df.columns:
                price_df['timestamp'] = pd.to_datetime(price_df['timestamp'].astype(int), unit='ms')
                price_df = price_df.sort_values('timestamp')
            
            # Create visualization
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add balance line
            fig.add_trace(
                go.Scatter(
                    x=history_df['timestamp'],
                    y=history_df['balance'],
                    name="Balance (KAS)",
                    line=dict(color='#4B8BBE'),
                    fill='tozeroy',
                    fillcolor='rgba(75, 139, 190, 0.1)'
                ),
                secondary_y=False
            )
            
            # Add price line if available
            if not price_df.empty and 'price' in price_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=price_df['timestamp'],
                        y=price_df['price'],
                        name="Price (USD)",
                        line=dict(color='#FFA500'),
                        yaxis="y2"
                    ),
                    secondary_y=True
                )
            
            # Update layout
            fig.update_layout(
                title=f"Address Balance History: {address[:15]}...",
                xaxis_title="Date",
                yaxis_title="Balance (KAS)",
                yaxis2_title="Price (USD)",
                hovermode="x unified",
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show transaction history
            st.subheader("Transaction History")
            st.dataframe(
                history_df[['datetime', 'amount', 'balance', 'transaction_id']].sort_values('datetime', ascending=False),
                column_config={
                    "datetime": "Date",
                    "amount": st.column_config.NumberColumn("Amount Received", format="%.8f KAS"),
                    "balance": st.column_config.NumberColumn("Balance", format="%.8f KAS"),
                    "transaction_id": "Transaction ID"
                },
                hide_index=True,
                use_container_width=True
            )
    else:
        st.error("Please enter a valid Kaspa address starting with 'kaspa:'")
