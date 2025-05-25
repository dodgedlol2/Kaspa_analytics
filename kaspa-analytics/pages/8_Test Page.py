import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuration
API_BASE_URL = "https://api.kaspa.org"
st.set_page_config(page_title="Kaspa Explorer", page_icon="⛓️", layout="wide")

# Helper functions
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
    """Safely get nested dictionary values"""
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return data

# App layout
st.title("Kaspa Blockchain Explorer")
st.markdown("A simple dashboard to explore Kaspa blockchain data")

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Network Info", "Address Lookup", "Block Info", "Transaction Info"])

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
            hashrate_data = make_api_request("/info/hashrate")
            if hashrate_data and isinstance(hashrate_data, dict):
                hashrate = safe_get(hashrate_data, 'hashrate', default=0)
                if isinstance(hashrate, (int, float)):
                    st.metric("Current Hashrate", f"{hashrate / 1e12:,.2f} TH/s")
                else:
                    st.warning("Invalid hashrate data")
    
    with col5:
        with st.spinner("Loading block reward data..."):
            blockreward_data = make_api_request("/info/blockreward")
            if blockreward_data and isinstance(blockreward_data, dict):
                blockreward = safe_get(blockreward_data, 'blockreward', default=0)
                if isinstance(blockreward, (int, float)):
                    st.metric("Block Reward", f"{blockreward / 1e8:,.2f} KAS")
                else:
                    st.warning("Invalid block reward data")

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

with tab4:
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
