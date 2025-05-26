import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration
API_BASE_URL = "https://api.kaspa.org"
st.set_page_config(page_title="Kaspa Explorer", page_icon="⛓️", layout="wide")

# Helper functions
def make_api_request(endpoint, params=None, as_text=False):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.text if as_text else response.json()
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
    """Safely get nested dictionary values"""
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return data

def fetch_address_history(address):
    """Fetch transaction history for an address"""
    transactions = []
    offset = 0
    limit = 50
    
    while True:
        endpoint = f"/addresses/{address}/full-transactions"
        params = {"offset": offset, "limit": limit}
        data = make_api_request(endpoint, params=params)
        
        if not data or not isinstance(data, list):
            break
            
        transactions.extend(data)
        
        if len(data) < limit:
            break
            
        offset += limit
        
    return transactions

def process_history_data(transactions, address):
    """Process transaction history into balance timeline"""
    balance = 0
    history = []
    
    # Sort transactions by timestamp (oldest first)
    sorted_txs = sorted(transactions, key=lambda x: safe_get(x, 'transaction', 'block_time', default=0))
    
    for tx in sorted_txs:
        if not isinstance(tx, dict):
            continue
            
        tx_data = safe_get(tx, 'transaction', default={})
        inputs = safe_get(tx_data, 'inputs', default=[])
        outputs = safe_get(tx_data, 'outputs', default=[])
        timestamp = safe_get(tx_data, 'block_time', default=None)
        
        if not timestamp:
            continue
            
        # Calculate net change for this address
        net_change = 0
        
        # Check outputs (money received)
        for out in outputs:
            if safe_get(out, 'script_public_key_address', default='') == address:
                net_change += float(safe_get(out, 'amount', default=0))
        
        # Check inputs (money sent)
        for inp in inputs:
            if safe_get(inp, 'script_public_key_address', default='') == address:
                net_change -= float(safe_get(inp, 'previous_outpoint_amount', default=0))
        
        balance += net_change
        history.append({
            'timestamp': timestamp,
            'datetime': format_timestamp(timestamp),
            'balance': balance / 1e8,
            'net_change': net_change / 1e8,
            'transaction_id': safe_get(tx_data, 'verboseData', 'transactionId', default='')
        })
    
    return history

def fetch_price_history():
    """Fetch historical price data (simplified - would use actual API in production)"""
    # In a real app, you would fetch this from an actual price API
    # This is a simplified version for demonstration
    price_data = make_api_request("/info/price-history")
    if price_data and isinstance(price_data, list):
        return price_data
    
    # Fallback dummy data
    return [
        {'timestamp': int((datetime.now().timestamp() - i*86400)*1000), 'price': 0.05 + i*0.001}
        for i in range(30)
    ]

# App layout
st.title("Kaspa Blockchain Explorer")
st.markdown("A simple dashboard to explore Kaspa blockchain data")

# Tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Network Info", "Address Lookup", "Address History", "Block Info", "Transaction Info"])

with tab1:
    st.header("Network Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Coin Supply")
        with st.spinner("Loading supply data..."):
            supply_data = make_api_request("/info/coinsupply")
            if supply_data:
                circulating = float(safe_get(supply_data, 'circulatingSupply', default=0)) / 1e8
                max_supply = float(safe_get(supply_data, 'maxSupply', default=0)) / 1e8
                st.metric("Circulating Supply", f"{circulating:,.2f} KAS")
                st.metric("Max Supply", f"{max_supply:,.2f} KAS")
    
    with col2:
        st.subheader("Network Status")
        with st.spinner("Loading network data..."):
            network_data = make_api_request("/info/network")
            if network_data:
                st.metric("Block Count", safe_get(network_data, 'blockCount', default='N/A'))
                difficulty = safe_get(network_data, 'difficulty', default=0)
                st.metric("Difficulty", f"{float(difficulty):,.2f}" if difficulty != 'N/A' else 'N/A')
    
    with col3:
        st.subheader("Price & Market Data")
        with st.spinner("Loading price data..."):
            price_data = make_api_request("/info/price")
            if price_data and isinstance(price_data, dict):
                price = safe_get(price_data, 'price', default=0)
                st.metric("Price (USD)", f"${float(price):,.4f}")
            else:
                st.warning("Could not load price data")
            
            marketcap_data = make_api_request("/info/marketcap")
            if marketcap_data and isinstance(marketcap_data, dict):
                marketcap = safe_get(marketcap_data, 'marketcap', default=0)
                st.metric("Market Cap", f"${float(marketcap):,.0f}")

    st.subheader("Hashrate & Mining")
    col4, col5 = st.columns(2)
    
    with col4:
        with st.spinner("Loading hashrate data..."):
            hashrate = make_api_request("/info/hashrate", params={"stringOnly": True}, as_text=True)
            if hashrate:
                try:
                    # Clean the response (remove quotes if present)
                    hashrate_clean = hashrate.strip('"\'')
                    hashrate_value = float(hashrate_clean)
                    st.metric("Current Hashrate", f"{hashrate_value:,.2f} PH/s")
                except ValueError:
                    st.warning("Invalid hashrate data")
            else:
                st.warning("Could not load hashrate data")
    
    with col5:
        with st.spinner("Loading block reward data..."):
            blockreward = make_api_request("/info/blockreward", params={"stringOnly": True}, as_text=True)
            if blockreward:
                try:
                    # Clean the response (remove quotes if present)
                    blockreward_clean = blockreward.strip('"\'')
                    blockreward_value = float(blockreward_clean)
                    st.metric("Block Reward", f"{blockreward_value:,.2f} KAS")
                except ValueError:
                    st.warning("Invalid block reward data")
            else:
                st.warning("Could not load block reward data")

with tab2:
    st.header("Address Information")
    
    address = st.text_input("Enter a Kaspa address (e.g. kaspa:qq...):", 
                          value="kaspa:qqkqkzjvr7zwxxmjxjkmxxdwju9kjs6e9u82uh59z07vgaks6gg62v8707g73")
    
    if st.button("Lookup Address"):
        if address and address.startswith("kaspa:"):
            with st.spinner("Fetching address data..."):
                # Get balance
                balance_data = make_api_request(f"/addresses/{address}/balance")
                if balance_data and isinstance(balance_data, dict):
                    balance = float(safe_get(balance_data, 'balance', default=0)) / 1e8
                    st.metric("Balance", f"{balance:,.8f} KAS")
                else:
                    st.warning("Could not load balance data")
                
                # Get UTXOs
                st.subheader("UTXOs (Unspent Transaction Outputs)")
                utxos_data = make_api_request(f"/addresses/{address}/utxos")
                if utxos_data and isinstance(utxos_data, list):
                    try:
                        utxos_list = []
                        for utxo in utxos_data:
                            if isinstance(utxo, dict) and 'utxoEntry' in utxo:
                                amount_str = safe_get(utxo, 'utxoEntry', 'amount', default=['0'])[0]
                                amount = float(amount_str) / 1e8
                                utxos_list.append({
                                    'address': safe_get(utxo, 'address', default=''),
                                    'amount': amount
                                })
                        if utxos_list:
                            utxos_df = pd.DataFrame(utxos_list)
                            st.dataframe(utxos_df.style.format({'amount': '{:,.8f}'}))
                        else:
                            st.info("No UTXOs found for this address")
                    except Exception as e:
                        st.error(f"Error processing UTXOs: {str(e)}")
                
                # Get transaction count
                tx_count = make_api_request(f"/addresses/{address}/transactions-count")
                if tx_count and isinstance(tx_count, dict):
                    st.metric("Transaction Count", safe_get(tx_count, 'total', default=0))
        else:
            st.error("Please enter a valid Kaspa address starting with 'kaspa:'")

with tab3:
    st.header("Address History & Price Analysis")
    
    address = st.text_input("Enter a Kaspa address to view history:", 
                          value="kaspa:qqkqkzjvr7zwxxmjxjkmxxdwju9kjs6e9u82uh59z07vgaks6gg62v8707g73",
                          key="history_address")
    
    if st.button("View Address History"):
        if address and address.startswith("kaspa:"):
            with st.spinner("Fetching address history..."):
                # Get transaction history
                transactions = fetch_address_history(address)
                
                if transactions and isinstance(transactions, list):
                    # Process history data
                    history = process_history_data(transactions, address)
                    
                    if history:
                        # Create DataFrame
                        history_df = pd.DataFrame(history)
                        history_df['timestamp'] = pd.to_datetime(history_df['timestamp'].astype(int), unit='ms')
                        history_df = history_df.sort_values('timestamp')
                        
                        # Get price history
                        price_history = fetch_price_history()
                        price_df = pd.DataFrame(price_history)
                        if 'timestamp' in price_df.columns:
                            price_df['timestamp'] = pd.to_datetime(price_df['timestamp'].astype(int), unit='ms')
                            price_df = price_df.sort_values('timestamp')
                        
                        # Create combined plot
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
                            title=f"Address Balance History with Price: {address[:15]}...",
                            xaxis_title="Date",
                            yaxis_title="Balance (KAS)",
                            yaxis2_title="Price (USD)",
                            hovermode="x unified",
                            height=600
                        )
                        
                        # Display the plot
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show transaction history table
                        st.subheader("Transaction History")
                        st.dataframe(
                            history_df[['datetime', 'net_change', 'balance', 'transaction_id']].sort_values('datetime', ascending=False),
                            column_config={
                                "datetime": "Date",
                                "net_change": st.column_config.NumberColumn("Amount", format="%.8f"),
                                "balance": st.column_config.NumberColumn("Balance", format="%.8f"),
                                "transaction_id": "Transaction ID"
                            }
                        )
                    else:
                        st.warning("No transaction history found for this address")
                else:
                    st.error("Could not fetch transaction history")
        else:
            st.error("Please enter a valid Kaspa address starting with 'kaspa:'")

with tab4:
    st.header("Block Information")
    
    block_id = st.text_input("Enter a Block Hash:", 
                           value="18c7afdf8f447ca06adb8b4946dc45f5feb1188c7d177da6094dfbc760eca699")
    
    if st.button("Get Block Info"):
        if block_id:
            with st.spinner("Fetching block data..."):
                block_data = make_api_request(f"/blocks/{block_id}", params={"includeTransactions": True})
                if block_data and isinstance(block_data, dict):
                    col6, col7 = st.columns(2)
                    
                    with col6:
                        blue_score = safe_get(block_data, 'verboseData', 'blueScore', default='N/A')
                        timestamp = safe_get(block_data, 'header', 'timestamp', default='N/A')
                        difficulty = safe_get(block_data, 'verboseData', 'difficulty', default=[0])
                        if isinstance(difficulty, list) and len(difficulty) > 0:
                            difficulty = difficulty[0]
                        else:
                            difficulty = 0
                        
                        st.metric("Block Height", blue_score)
                        st.metric("Timestamp", format_timestamp(timestamp))
                        st.metric("Difficulty", f"{float(difficulty):,.2f}")
                    
                    with col7:
                        transactions = safe_get(block_data, 'transactions', default=[])
                        st.metric("Transaction Count", len(transactions))
                        st.metric("Hash", safe_get(block_data, 'verboseData', 'hash', default='N/A'))
                    
                    st.subheader("Transactions in Block")
                    if transactions and isinstance(transactions, list):
                        try:
                            tx_list = []
                            for tx in transactions:
                                if isinstance(tx, dict):
                                    tx_list.append({
                                        'id': safe_get(tx, 'verboseData', 'transactionId', default=''),
                                        'mass': safe_get(tx, 'mass', default=''),
                                        'inputs': len(safe_get(tx, 'inputs', default=[])),
                                        'outputs': len(safe_get(tx, 'outputs', default=[]))
                                    })
                            if tx_list:
                                tx_df = pd.DataFrame(tx_list)
                                st.dataframe(tx_df)
                            else:
                                st.info("No transactions in this block")
                        except Exception as e:
                            st.error(f"Error processing transactions: {str(e)}")
                else:
                    st.error("Could not fetch block data")

with tab5:
    st.header("Transaction Information")
    
    tx_id = st.text_input("Enter a Transaction ID:", 
                         value="b9382bdee4aa364acf73eda93914eaae61d0e78334d1b8a637ab89ef5e224e41")
    
    if st.button("Get Transaction Info"):
        if tx_id:
            with st.spinner("Fetching transaction data..."):
                tx_data = make_api_request(f"/transactions/{tx_id}")
                if tx_data and isinstance(tx_data, dict):
                    col8, col9 = st.columns(2)
                    
                    with col8:
                        st.metric("Transaction ID", safe_get(tx_data, 'transaction_id', default='N/A'))
                        st.metric("Mass", safe_get(tx_data, 'mass', default='N/A'))
                        st.metric("Block Time", format_timestamp(safe_get(tx_data, 'block_time', default=0)))
                    
                    with col9:
                        st.metric("Inputs", len(safe_get(tx_data, 'inputs', default=[])))
                        st.metric("Outputs", len(safe_get(tx_data, 'outputs', default=[])))
                    
                    st.subheader("Inputs")
                    inputs = safe_get(tx_data, 'inputs', default=[])
                    if inputs and isinstance(inputs, list):
                        try:
                            input_list = []
                            for inp in inputs:
                                if isinstance(inp, dict):
                                    input_list.append({
                                        'previous_outpoint_hash': safe_get(inp, 'previous_outpoint_hash', default=''),
                                        'previous_outpoint_index': safe_get(inp, 'previous_outpoint_index', default=''),
                                        'previous_outpoint_amount': float(safe_get(inp, 'previous_outpoint_amount', default=0)) / 1e8
                                    })
                            if input_list:
                                inputs_df = pd.DataFrame(input_list)
                                st.dataframe(inputs_df.style.format({'previous_outpoint_amount': '{:,.8f}'}))
                        except Exception as e:
                            st.error(f"Error processing inputs: {str(e)}")
                    else:
                        st.info("No inputs found")
                    
                    st.subheader("Outputs")
                    outputs = safe_get(tx_data, 'outputs', default=[])
                    if outputs and isinstance(outputs, list):
                        try:
                            output_list = []
                            for out in outputs:
                                if isinstance(out, dict):
                                    output_list.append({
                                        'address': safe_get(out, 'script_public_key_address', default=''),
                                        'amount': float(safe_get(out, 'amount', default=0)) / 1e8
                                    })
                            if output_list:
                                outputs_df = pd.DataFrame(output_list)
                                st.dataframe(outputs_df.style.format({'amount': '{:,.8f}'}))
                        except Exception as e:
                            st.error(f"Error processing outputs: {str(e)}")
                    else:
                        st.info("No outputs found")
                else:
                    st.error("Could not fetch transaction data")
