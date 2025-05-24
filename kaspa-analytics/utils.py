import pandas as pd
import numpy as np
import gspread
from google.oauth2 import service_account
from scipy.stats import linregress
import streamlit as st

# Shared authentication function
def get_gspread_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return gspread.authorize(credentials)

# ===== DATA LOADING FUNCTIONS =====
@st.cache_data(ttl=3600)
def load_data():
    gc = get_gspread_client()
    sheet_id = "1NPwQh2FQKVES7OYUzKQLKwuOrRuIivGhOtQWZZ-Sp80"
    worksheet = gc.open_by_key(sheet_id).worksheet("kaspa_daily_hashrate (3)")
    data = worksheet.get_all_values()
    
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[['Date', 'Hashrate (H/s)']]
    
    df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y', utc=True)
    df['Hashrate (H/s)'] = df['Hashrate (H/s)'].astype(float)
    
    genesis_date = pd.to_datetime('2021-11-07', utc=True)
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    df['Hashrate_PH'] = df['Hashrate (H/s)'] / 1e15
    
    return df, genesis_date

@st.cache_data(ttl=3600)
def load_price_data():
    gc = get_gspread_client()
    price_sheet_id = "1rMBuWn0CscUZkcKy2gleH85rXSO6U4YOSk3Sz2KuR_s"
    price_worksheet_name = "kaspa_daily_price"
    worksheet = gc.open_by_key(price_sheet_id).worksheet(price_worksheet_name)
    data = worksheet.get_all_values()
    
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[['Date', 'Price']]
    
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df['Price'] = df['Price'].astype(float)
    
    genesis_date = pd.to_datetime('2021-11-07', utc=True)
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    
    return df, genesis_date

@st.cache_data(ttl=3600)
def load_volume_data():
    gc = get_gspread_client()
    volume_sheet_id = "1IdAmETrtZ8_lCuSQwEyDLtMIGiQbJFOyGGpMa9_hxZc"
    volume_worksheet_name = "KAS_VOLUME_ETC"
    worksheet = gc.open_by_key(volume_sheet_id).worksheet(volume_worksheet_name)
    data = worksheet.get_all_values()
    
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[['date', 'price', 'total_volume']]
    df = df.rename(columns={
        'date': 'Date',
        'price': 'Price',
        'total_volume': 'Volume_USD'
    })
    
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Volume_USD'] = pd.to_numeric(df['Volume_USD'], errors='coerce')
    df = df.dropna()
    
    genesis_date = pd.to_datetime('2021-11-07', utc=True)
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    
    return df.sort_values('Date').reset_index(drop=True)

@st.cache_data(ttl=3600)
def load_marketcap_data():
    gc = get_gspread_client()
    marketcap_sheet_id = "15BZcsswJPZZF2MQ6S_m9CtbHPtVJVcET_VjZ9_aJ8nY"
    marketcap_worksheet_name = "kaspa_market_cap"
    worksheet = gc.open_by_key(marketcap_sheet_id).worksheet(marketcap_worksheet_name)
    data = worksheet.get_all_values()
    
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[['Date', 'MarketCap']]
    
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df['MarketCap'] = df['MarketCap'].astype(float)
    
    genesis_date = pd.to_datetime('2021-11-07', utc=True)
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    df['MarketCap_B'] = df['MarketCap'] / 1e9
    
    return df, genesis_date

# ===== ANALYSIS FUNCTIONS =====
def fit_power_law(df, y_col='Hashrate_PH', x_col=None):
    """
    Fits a power law y = a*x^b to the data
    Maintains backward compatibility while adding new functionality
    
    Args:
        df: DataFrame containing the data
        y_col: Column name for dependent variable
        x_col: Optional column name for independent variable (default: 'days_from_genesis')
    """
    # Handle backward compatibility
    if x_col is None:
        x_col = 'days_from_genesis'
    
    # Filter out invalid values
    valid_data = df[(df[x_col] > 0) & (df[y_col] > 0)].copy()
    
    if len(valid_data) < 2:
        raise ValueError("Not enough valid data points for power law fitting")
    
    # Perform linear regression on log-transformed data
    slope, intercept, r_value, _, _ = linregress(
        np.log(valid_data[x_col]),
        np.log(valid_data[y_col]))
    
    # Convert back to power law coefficients
    a = np.exp(intercept)
    b = slope
    r2 = r_value**2
    
    return a, b, r2

def calculate_growth_metrics(df, value_col='Price', date_col='Date'):
    """Calculate periodic growth rates and volatility"""
    df = df.sort_values(date_col).copy()
    
    metrics = {
        'current_value': df[value_col].iloc[-1],
        'daily_return': df[value_col].pct_change().iloc[-1],
        'weekly_return': df[value_col].pct_change(7).iloc[-1],
        'monthly_return': df[value_col].pct_change(30).iloc[-1],
        'annualized_volatility': df[value_col].pct_change().std() * np.sqrt(365)
    }
    
    return metrics
