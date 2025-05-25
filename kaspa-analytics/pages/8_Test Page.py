import streamlit as st
import requests
import json
import pandas as pd

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
        st.error(f"API request failed: {e}")
        return None

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
        supply_data = make_api_request("/info/coinsupply")
        if supply_data:
            st.metric("Circulating Supply", f"{float(supply_data['circulatingSupply']) / 1e8:,.2f} KAS")
            st.metric("Max Supply", f"{float(supply_data['maxSupply']) / 1e8:,.2f} KAS")
    
    with col2:
        st.subheader("Network Status")
        network_data = make_api_request("/info/network")
        if network_data:
            st.metric("Block Count", network_data['blockCount'])
            st.metric("Difficulty", f"{network_data['difficulty']:,.2f}")
    
    with col3:
        st.subheader("Price & Market Data")
        price_data = make_api_request("/info/price")
        if price_data:
            st.metric("Price (USD)", f"${price_data['price']:,.4f}")
        
        marketcap_data = make_api_request("/info/marketcap")
        if marketcap_data:
            st.metric("Market Cap", f"${marketcap_data['marketcap']:,.0f}")

    st.subheader("Hashrate & Mining")
    col4, col5 = st.columns(2)
    
    with col4:
        hashrate_data = make_api_request("/info/hashrate")
        if hashrate_data:
            st.metric("Current Hashrate", f"{hashrate_data['hashrate'] / 1e12:,.2f} TH/s")
    
    with col5:
        blockreward_data = make_api_request("/info/blockreward")
        if blockreward_data:
            st.metric("Block Reward", f"{blockreward_data['blockreward'] / 1e8:,.2f} KAS")

with tab2:
    st.header("Address Information")
    
    address = st.text_input("Enter a Kaspa address (e.g. kaspa:qq...):", 
                          value="kaspa:qqkqkzjvr7zwxxmjxjkmxxdwju9kjs6e9u82uh59z07vgaks6gg62v8707g73")
    
    if st.button("Lookup Address"):
        if address.startswith("kaspa:"):
            # Get balance
            balance_data = make_api_request(f"/addresses/{address}/balance")
            if balance_data:
                st.metric("Balance", f"{balance_data['balance'] / 1e8:,.8f} KAS")
            
            # Get UTXOs
            st.subheader("UTXOs (Unspent Transaction Outputs)")
            utxos_data = make_api_request(f"/addresses/{address}/utxos")
            if utxos_data:
                utxos_df = pd.DataFrame(utxos_data)
                utxos_df['amount'] = utxos_df['utxoEntry'].apply(lambda x: float(x['amount'][0]) / 1e8
                st.dataframe(utxos_df[['address', 'amount']].style.format({'amount': '{:,.8f}'}), 
                             height=300)
            
            # Get transaction count
            tx_count = make_api_request(f"/addresses/{address}/transactions-count")
            if tx_count:
                st.metric("Transaction Count", tx_count['total'])
        else:
            st.error("Please enter a valid Kaspa address starting with 'kaspa:'")

with tab3:
    st.header("Block Information")
    
    block_id = st.text_input("Enter a Block Hash:", 
                           value="18c7afdf8f447ca06adb8b4946dc45f5feb1188c7d177da6094dfbc760eca699")
    
    if st.button("Get Block Info"):
        block_data = make_api_request(f"/blocks/{block_id}", params={"includeTransactions": True})
        if block_data:
            col6, col7 = st.columns(2)
            
            with col6:
                st.metric("Block Height", block_data['verboseData']['blueScore'])
                st.metric("Timestamp", pd.to_datetime(int(block_data['header']['timestamp']), unit='ms')
                st.metric("Difficulty", f"{block_data['verboseData']['difficulty'][0]:,.2f}")
            
            with col7:
                st.metric("Transaction Count", len(block_data['transactions']))
                st.metric("Hash", block_data['verboseData']['hash'])
            
            st.subheader("Transactions in Block")
            txs = block_data['transactions']
            tx_df = pd.DataFrame([{
                'id': tx['verboseData']['transactionId'],
                'mass': tx['mass'],
                'inputs': len(tx['inputs']),
                'outputs': len(tx['outputs'])
            } for tx in txs])
            st.dataframe(tx_df)

with tab4:
    st.header("Transaction Information")
    
    tx_id = st.text_input("Enter a Transaction ID:", 
                         value="b9382bdee4aa364acf73eda93914eaae61d0e78334d1b8a637ab89ef5e224e41")
    
    if st.button("Get Transaction Info"):
        tx_data = make_api_request(f"/transactions/{tx_id}")
        if tx_data:
            col8, col9 = st.columns(2)
            
            with col8:
                st.metric("Transaction ID", tx_data['transaction_id'])
                st.metric("Mass", tx_data['mass'])
                st.metric("Block Time", pd.to_datetime(tx_data['block_time'], unit='ms'))
            
            with col9:
                st.metric("Inputs", len(tx_data['inputs']))
                st.metric("Outputs", len(tx_data['outputs']))
            
            st.subheader("Inputs")
            inputs_df = pd.DataFrame(tx_data['inputs'])
            st.dataframe(inputs_df[['previous_outpoint_hash', 'previous_outpoint_index', 'previous_outpoint_amount']])
            
            st.subheader("Outputs")
            outputs_df = pd.DataFrame(tx_data['outputs'])
            st.dataframe(outputs_df[['script_public_key_address', 'amount']])
