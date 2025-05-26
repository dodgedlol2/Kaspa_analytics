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

def fetch_address_transactions(address):
    """Fetch all transactions for an address using the correct API endpoint"""
    transactions = []
    offset = 0
    limit = 50  # Adjust based on API limits
    
    while True:
        endpoint = f"/addresses/{address}/transactions"
        params = {"offset": offset, "limit": limit}
        data = make_api_request(endpoint, params=params)
        
        if not data or not isinstance(data, list):
            break
            
        transactions.extend(data)
        
        if len(data) < limit:
            break
            
        offset += limit
        
    return transactions

def process_transaction_history(transactions, address):
    """Process transactions into balance timeline"""
    balance = 0
    history = []
    
    # Sort transactions by timestamp (oldest first)
    sorted_txs = sorted(transactions, key=lambda x: safe_get(x, 'blockTime', default=0))
    
    for tx in sorted_txs:
        if not isinstance(tx, dict):
            continue
            
        tx_id = safe_get(tx, 'transactionId', default='')
        timestamp = safe_get(tx, 'blockTime', default=None)
        inputs = safe_get(tx, 'inputs', default=[])
        outputs = safe_get(tx, 'outputs', default=[])
        
        if not timestamp:
            continue
            
        # Calculate net change for this address
        net_change = 0
        
        # Check outputs (money received)
        for out in outputs:
            if safe_get(out, 'address', default='') == address:
                amount = float(safe_get(out, 'amount', default=0))
                net_change += amount
        
        # Check inputs (money sent)
        for inp in inputs:
            if safe_get(inp, 'address', default='') == address:
                amount = float(safe_get(inp, 'amount', default=0))
                net_change -= amount
        
        balance += net_change
        history.append({
            'timestamp': timestamp,
            'datetime': format_timestamp(timestamp),
            'balance': balance / 1e8,  # Convert from sompi to KAS
            'net_change': net_change / 1e8,
            'transaction_id': tx_id
        })
    
    return history

def fetch_kaspa_price_history():
    """Fetch simplified price history (in a real app, use a proper price API)"""
    # This is a placeholder - replace with actual API call
    return [
        {'timestamp': int((datetime.now().timestamp() - i*86400)*1000), 'price': 0.05 + i*0.001}
        for i in range(30)
    ]

# Main App
st.title("Kaspa Address History Explorer")
st.markdown("Visualize address balance history with price context")

address = st.text_input("Enter Kaspa Address:", 
                       value="kaspa:qqkqkzjvr7zwxxmjxjkmxxdwju9kjs6e9u82uh59z07vgaks6gg62v8707g73")

if st.button("Analyze Address History"):
    if address and address.startswith("kaspa:"):
        with st.spinner("Fetching address data..."):
            # First check if address is valid by getting balance
            balance_data = make_api_request(f"/addresses/{address}/balance")
            if not balance_data:
                st.error("Could not fetch address data. Please check the address and try again.")
                st.stop()
            
            current_balance = float(safe_get(balance_data, 'balance', default=0)) / 1e8
            st.metric("Current Balance", f"{current_balance:,.8f} KAS")
            
            # Get transaction history
            transactions = fetch_address_transactions(address)
            
            if not transactions:
                st.warning("No transactions found for this address")
                st.stop()
                
            # Process history
            history = process_transaction_history(transactions, address)
            
            if not history:
                st.warning("Could not process transaction history")
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
                height=600,
                showlegend=True
            )
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Show transaction history table
            st.subheader("Transaction History Details")
            st.dataframe(
                history_df[['datetime', 'net_change', 'balance', 'transaction_id']].sort_values('datetime', ascending=False),
                column_config={
                    "datetime": "Date",
                    "net_change": st.column_config.NumberColumn("Amount", format="%.8f KAS"),
                    "balance": st.column_config.NumberColumn("Balance", format="%.8f KAS"),
                    "transaction_id": "Transaction ID"
                },
                hide_index=True,
                use_container_width=True
            )
    else:
        st.error("Please enter a valid Kaspa address starting with 'kaspa:'")
