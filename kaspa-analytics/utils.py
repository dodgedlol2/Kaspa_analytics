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
    
    # Load price data
    price_sheet_id = "1rMBuWn0CscUZkcKy2gleH85rXSO6U4YOSk3Sz2KuR_s"
    price_worksheet_name = "kaspa_daily_price"
    worksheet = gc.open_by_key(price_sheet_id).worksheet(price_worksheet_name)
    data = worksheet.get_all_values()
    
    # Create DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[['Date', 'Price']]
    
    # Clean data
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df['Price'] = df['Price'].astype(float)
    
    # Calculate metrics
    genesis_date = pd.to_datetime('2021-11-07', utc=True)
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    
    return df, genesis_date

# ===== MARKET CAP FUNCTIONS =====
@st.cache_data(ttl=3600)
def load_marketcap_data():
    gc = get_gspread_client()
    
    # Load market cap data - adjust these to match your sheet
    marketcap_sheet_id = "15BZcsswJPZZF2MQ6S_m9CtbHPtVJVcET_VjZ9_aJ8nY"  # Replace with your actual sheet ID
    marketcap_worksheet_name = "kaspa_market_cap"  # e.g. "kaspa_marketcap"
    worksheet = gc.open_by_key(marketcap_sheet_id).worksheet(marketcap_worksheet_name)
    data = worksheet.get_all_values()
    
    # Create DataFrame - adjust columns based on your data structure
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[['Date', 'MarketCap']]  # Ensure these column names match your sheet
    
    # Clean data
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df['MarketCap'] = df['MarketCap'].astype(float)
    
    # Calculate metrics
    genesis_date = pd.to_datetime('2021-11-07', utc=True)
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    
    # Convert market cap to billions for better readability
    df['MarketCap_B'] = df['MarketCap'] / 1e9
    
    return df, genesis_date

# ===== SHARED ANALYSIS FUNCTIONS =====
def fit_power_law(df, y_col='Hashrate_PH'):
    """General power law fitting function that works for hashrate, price, and market cap"""
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

def calculate_growth_metrics(df, y_col):
    """Calculate periodic growth rates and volatility"""
    df = df.copy()
    df['daily_change'] = df[y_col].pct_change()
    df['weekly_change'] = df[y_col].pct_change(7)
    df['monthly_change'] = df[y_col].pct_change(30)
    
    metrics = {
        'last_value': df[y_col].iloc[-1],
        'daily_volatility': df['daily_change'].std(),
        'weekly_growth': df['weekly_change'].mean(),
        'monthly_growth': df['monthly_change'].mean()
    }
    return metrics
