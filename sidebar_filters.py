import streamlit as st
def create_sidebar_filters(df):
    """Create sidebar filters for location and scheme"""
    location_filter = st.sidebar.multiselect(
        "Location",
        options=df['location'].unique(),
        default=[]   # 👈 start with nothing selected
    )
    scheme_filter = st.sidebar.multiselect(
        "Scheme",
        options=df['scheme_requested'].unique(),
        default=[]   # 👈 start with nothing selected
    )
    
    return location_filter, scheme_filter

def apply_filters(df, location_filter, scheme_filter):
    """Apply selected filters to the dataframe"""
    filtered_df = df.copy()
    
    # Apply only if user selects something
    if location_filter:
        filtered_df = filtered_df[filtered_df['location'].isin(location_filter)]
    
    if scheme_filter:
        filtered_df = filtered_df[filtered_df['scheme_requested'].isin(scheme_filter)]
    
    return filtered_df
