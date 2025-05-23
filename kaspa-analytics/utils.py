import pandas as pd
import numpy as np
import gspread
from google.oauth2 import service_account
from sklearn.metrics import r2_score
import streamlit as st

# Shared authentication function
def get_gspread_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return gspread.authorize(credentials)

# ===== HASH RATE FUNCTIONS =====
@st.cache_data(ttl=3600)
def load_data():
    gc = get_gspread_client()
    
    # Load hashrate data
    sheet_id = "1NPwQh2FQKVES7OYUzKQLKwuOrRuIivGhOtQWZZ-Sp80"
    worksheet = gc.open_by_key(sheet_id).worksheet("kaspa_daily_hashrate (3)")
    data = worksheet.get_all_values()
    
    # Create DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[['Date', 'Hashrate (H/s)']]
    
    # Clean data
    df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y', utc=True)
    df['Hashrate (H/s)'] = df['Hashrate (H/s)'].astype(float)
    
    # Calculate metrics
    genesis_date = pd.to_datetime('2021-11-07', utc=True)
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    df['Hashrate_PH'] = df['Hashrate (H/s)'] / 1e15
    
    return df, genesis_date

# ===== PRICE FUNCTIONS =====
@st.cache_data(ttl=3600)
def load_price_data():
    gc = get_gspread_client()
    
    # Load price data - you'll need to provide these details
    price_sheet_id = "YOUR_PRICE_SHEET_ID"  # Replace with your actual sheet ID
    price_worksheet_name = "YOUR_WORKSHEET_NAME"  # Replace with your worksheet name
    worksheet = gc.open_by_key(price_sheet_id).worksheet(price_worksheet_name)
    data = worksheet.get_all_values()
    
    # Create DataFrame - adjust columns based on your actual data structure
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[['Date', 'Price']]  # Adjust these column names to match your data
    
    # Clean data
    df['Date'] = pd.to_datetime(df['Date'], utc=True)  # Adjust format if needed
    df['Price'] = df['Price'].astype(float)
    
    # Calculate metrics
    genesis_date = pd.to_datetime('2021-11-07', utc=True)  # Same genesis as hashrate
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    
    return df, genesis_date

# ===== SHARED ANALYSIS FUNCTIONS =====
def fit_power_law(df, y_col='Hashrate_PH'):
    """General power law fitting function that works for both hashrate and price"""
    x_data = df['days_from_genesis'].values
    y_data = df[y_col].values
    
    valid_indices = (x_data > 0) & (y_data > 0)
    x_data, y_data = x_data[valid_indices], y_data[valid_indices]
    
    log_x = np.log10(x_data)
    log_y = np.log10(y_data)
    
    coeffs = np.polyfit(log_x, log_y, 1)
    b = coeffs[0]
    a = 10 ** coeffs[1]
    
    y_pred = a * np.power(x_data, b)
    r2 = r2_score(np.log10(y_data), np.log10(y_pred))
    
    return a, b, r2
