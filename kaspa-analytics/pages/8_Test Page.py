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
        return datetime.fromtimestamp(int(timestamp_ms)/1000).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "N/A"

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
                circulating = float(supply_data.get('circulatingSupply', 0)) / 1e8
                max_supply = float(supply_data.get('maxSupply', 0)) / 1e8
                st.metric("Circulating Supply", f"{circulating:,.2f} KAS")
                st.metric("Max Supply", f"{max_supply:,.2f} KAS")
    
    with col2:
        st.subheader("Network Status")
        with st.spinner("Loading network data..."):
            network_data = make_api_request("/info/network")
            if network_data:
                st.metric("Block Count", network_data.get('blockCount', 'N/A'))
                st.metric("Difficulty", f"{float(network_data.get('difficulty', 0)):,.2f}")
    
    with col3:
        st.subheader("Price & Market Data")
        with st.spinner("Loading price data..."):
            price_data = make_api_request("/info/price")
            if price_data and isinstance(price_data, dict):
                st.metric("Price (USD)", f"${float(price_data.get('price', 0)):,.4f}")
            else:
                st.warning("Could not load price data")
            
            marketcap_data = make_api_request("/info/marketcap")
            if marketcap_data and isinstance(marketcap_data, dict):
                st.metric("Market Cap", f"${float(marketcap_data.get('marketcap', 0)):,.0f}")

    st.subheader("Hashrate & Mining")
    col4, col5 = st.columns(2)
    
    with col4:
        with st.spinner("Loading hashrate data..."):
            hashrate_data = make_api_request("/info/hashrate")
            if hashrate_data and isinstance(hashrate_data, dict):
                st.metric("Current Hashrate", f"{float(hashrate_data.get('hashrate', 0)) / 1e12:,.2f} TH/s")
    
    with col5:
        with st.spinner("Loading block reward data..."):
            blockreward_data = make_api_request("/info/blockreward")
            if blockreward_data and isinstance(blockreward_data, dict):
                st.metric("Block Reward", f"{float(blockreward_data.get('blockreward', 0)) / 1e8:,.2f} KAS")

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
                    balance = float(balance_data.get('balance', 0)) / 1e8
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
                                amount = float(utxo['utxoEntry'].get('amount', ['0'])[0]) / 1e8
                                utxos_list.append({
                                    'address': utxo.get('address', ''),
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
                    st.metric("Transaction Count", tx_count.get('total', 0))
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
                        blue_score = block_data.get('verboseData', {}).get('blueScore', 'N/A')
                        timestamp = block_data.get('header', {}).get('timestamp', 'N/A')
                        difficulty = block_data.get('verboseData', {}).get('difficulty', [0])[0]
                        
                        st.metric("Block Height", blue_score)
                        st.metric("Timestamp", format_timestamp(timestamp))
                        st.metric("Difficulty", f"{float(difficulty):,.2f}")
                    
                    with col7:
                        transactions = block_data.get('transactions', [])
                        st.metric("Transaction Count", len(transactions))
                        st.metric("Hash", block_data.get('verboseData', {}).get('hash', 'N/A'))
                    
                    st.subheader("Transactions in Block")
                    if transactions:
                        try:
                            tx_list = []
                            for tx in transactions:
                                if isinstance(tx, dict):
                                    tx_list.append({
                                        'id': tx.get('verboseData', {}).get('transactionId', ''),
                                        'mass': tx.get('mass', ''),
                                        'inputs': len(tx.get('inputs', [])),
                                        'outputs': len(tx.get('outputs', []))
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
                        st.metric("Transaction ID", tx_data.get('transaction_id', 'N/A'))
                        st.metric("Mass", tx_data.get('mass', 'N/A'))
                        st.metric("Block Time", format_timestamp(tx_data.get('block_time', 0)))
                    
                    with col9:
                        st.metric("Inputs", len(tx_data.get('inputs', [])))
                        st.metric("Outputs", len(tx_data.get('outputs', [])))
                    
                    st.subheader("Inputs")
                    inputs = tx_data.get('inputs', [])
                    if inputs:
                        try:
                            input_list = []
                            for inp in inputs:
                                if isinstance(inp, dict):
                                    input_list.append({
                                        'previous_outpoint_hash': inp.get('previous_outpoint_hash', ''),
                                        'previous_outpoint_index': inp.get('previous_outpoint_index', ''),
                                        'previous_outpoint_amount': float(inp.get('previous_outpoint_amount', 0)) / 1e8
                                    })
                            if input_list:
                                inputs_df = pd.DataFrame(input_list)
                                st.dataframe(inputs_df.style.format({'previous_outpoint_amount': '{:,.8f}'}))
                        except Exception as e:
                            st.error(f"Error processing inputs: {str(e)}")
                    else:
                        st.info("No inputs found")
                    
                    st.subheader("Outputs")
                    outputs = tx_data.get('outputs', [])
                    if outputs:
                        try:
                            output_list = []
                            for out in outputs:
                                if isinstance(out, dict):
                                    output_list.append({
                                        'address': out.get('script_public_key_address', ''),
                                        'amount': float(out.get('amount', 0)) / 1e8
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
