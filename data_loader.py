import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load raw data from Excel file"""
    data = pd.read_excel(r"data/structured_call_data_modified.xlsx")
    return data

def process_datetime_columns(df):
    """Process date and time columns to create datetime objects"""
    df['call_date'] = df['call_date'].astype(str)
    df['call_time'] = df['call_time'].astype(str).str.strip()
    df['call_datetime'] = pd.to_datetime(df['call_date'] + ' ' + df['call_time'], errors='coerce')
    df['call_hour'] = df['call_datetime'].dt.hour
    return df

def load_and_process_data():
    """Load and process data with all transformations"""
    df = load_data()
    df = process_datetime_columns(df)
    return df