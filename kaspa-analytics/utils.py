import pandas as pd
import numpy as np
import gspread
from google.oauth2 import service_account
from sklearn.metrics import r2_score
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
    """Load hashrate data with caching"""
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

@st.cache_data(ttl=3600)
def load_price_data():
    """Load price data with caching"""
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

@st.cache_data(ttl=3600)
def load_volume_data():
    """Load volume data with caching"""
    gc = get_gspread_client()
    
    # Load volume data
    volume_sheet_id = "1IdAmETrtZ8_lCuSQwEyDLtMIGiQbJFOyGGpMa9_hxZc"
    volume_worksheet_name = "KAS_VOLUME_ETC"
    worksheet = gc.open_by_key(volume_sheet_id).worksheet(volume_worksheet_name)
    data = worksheet.get_all_values()
    
    # Create DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Clean data
    df = df[['date', 'price', 'total_volume']]
    df = df.rename(columns={
        'date': 'Date',
        'price': 'Price',
        'total_volume': 'Volume_USD'
    })
    
    # Convert data types
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Volume_USD'] = pd.to_numeric(df['Volume_USD'], errors='coerce')
    
    # Remove rows with missing data
    df = df.dropna()
    
    # Calculate metrics
    genesis_date = pd.to_datetime('2021-11-07', utc=True)
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    
    return df.sort_values('Date').reset_index(drop=True)

@st.cache_data(ttl=3600)
def load_marketcap_data():
    """Load market cap data with caching"""
    gc = get_gspread_client()
    
    # Load market cap data
    marketcap_sheet_id = "15BZcsswJPZZF2MQ6S_m9CtbHPtVJVcET_VjZ9_aJ8nY"
    marketcap_worksheet_name = "kaspa_market_cap"
    worksheet = gc.open_by_key(marketcap_sheet_id).worksheet(marketcap_worksheet_name)
    data = worksheet.get_all_values()
    
    # Create DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[['Date', 'MarketCap']]
    
    # Clean data
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df['MarketCap'] = df['MarketCap'].astype(float)
    
    # Calculate metrics
    genesis_date = pd.to_datetime('2021-11-07', utc=True)
    df['days_from_genesis'] = (df['Date'] - genesis_date).dt.days
    df = df[df['days_from_genesis'] >= 0]
    df['MarketCap_B'] = df['MarketCap'] / 1e9
    
    return df, genesis_date

# ===== ANALYSIS FUNCTIONS =====
def fit_power_law(df, x_col='days_from_genesis', y_col='Hashrate_PH'):
    """
    Fits a power law y = a*x^b to the data
    Args:
        df: DataFrame containing the data
        x_col: Column name for independent variable (default: 'days_from_genesis')
        y_col: Column name for dependent variable (default: 'Hashrate_PH')
    Returns:
        a, b, r2: Power law coefficients and R-squared value
    """
    # Filter out invalid values
    valid_data = df[(df[x_col] > 0) & (df[y_col] > 0)].copy()
    
    if len(valid_data) < 2:
        raise ValueError("Not enough valid data points for power law fitting")
    
    # Perform linear regression on log-transformed data
    slope, intercept, r_value, _, _ = linregress(
        np.log(valid_data[x_col]),
        np.log(valid_data[y_col])
    
    # Convert back to power law coefficients
    a = np.exp(intercept)
    b = slope
    r2 = r_value**2
    
    return a, b, r2

def calculate_growth_metrics(df, value_col='Price', date_col='Date'):
    """
    Calculate periodic growth rates and volatility
    Args:
        df: DataFrame containing the data
        value_col: Column name containing the values to analyze
        date_col: Column name containing dates (must be datetime)
    Returns:
        Dictionary of growth metrics
    """
    df = df.sort_values(date_col).copy()
    
    metrics = {
        'current_value': df[value_col].iloc[-1],
        'daily_return': df[value_col].pct_change().iloc[-1],
        'weekly_return': df[value_col].pct_change(7).iloc[-1],
        'monthly_return': df[value_col].pct_change(30).iloc[-1],
        'annualized_volatility': df[value_col].pct_change().std() * np.sqrt(365),
        'max_drawdown': (df[value_col] / df[value_col].cummax() - 1).min(),
        'sharpe_ratio': (df[value_col].pct_change().mean() / 
                         df[value_col].pct_change().std()) * np.sqrt(365)
    }
    
    return metrics

def merge_datasets(include_price=True, include_hashrate=True, include_marketcap=True, include_volume=True):
    """
    Merge multiple datasets into one comprehensive DataFrame
    Returns:
        Merged DataFrame with selected metrics
    """
    dfs = []
    
    if include_hashrate:
        hashrate_df, _ = load_data()
        hashrate_df = hashrate_df[['Date', 'Hashrate_PH']]
        dfs.append(hashrate_df)
    
    if include_price:
        price_df, _ = load_price_data()
        price_df = price_df[['Date', 'Price']]
        dfs.append(price_df)
    
    if include_marketcap:
        marketcap_df, _ = load_marketcap_data()
        marketcap_df = marketcap_df[['Date', 'MarketCap_B']]
        dfs.append(marketcap_df)
    
    if include_volume:
        volume_df = load_volume_data()
        volume_df = volume_df[['Date', 'Volume_USD']]
        dfs.append(volume_df)
    
    # Merge all datasets
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='Date', how='outer')
    
    # Forward fill missing values for continuity
    merged_df = merged_df.sort_values('Date').ffill().dropna()
    
    return merged_df

def calculate_correlations(df):
    """
    Calculate correlation matrix between numeric columns
    Args:
        df: DataFrame containing the data
    Returns:
        Correlation matrix DataFrame
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    return df[numeric_cols].corr()
