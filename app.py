import streamlit as st
import pandas as pd
from data_loader import load_and_process_data
from sidebar_filters import create_sidebar_filters, apply_filters
from metrics_display import display_key_metrics
from tabs.usage_insights import render_usage_insights_tab
from tabs.scheme_demand import render_scheme_demand_tab
from tabs.citizen_pain_points import render_citizen_pain_points_tab
from tabs.sentiment_satisfaction import render_sentiment_satisfaction_tab

st.set_page_config(
    page_title="Voice Bot Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;   
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # Load data
    df = load_and_process_data()    
    # Create sidebar filters
    location_filter, scheme_filter = create_sidebar_filters(df)
    
    # Apply filters to data
    filtered_df = apply_filters(df, location_filter, scheme_filter)
    
    # Dashboard title
    st.markdown("<h1 style='margin-top:0; margin-bottom:1rem;'>Voice Bot Analytics Dashboard</h1>", unsafe_allow_html=True)

    # Display key metrics
    display_key_metrics(filtered_df)
    tab1, tab2, tab3, tab4 = st.tabs([
        "Usage Insights", 
        "Scheme Demand & Awareness", 
        "Citizen Pain Points", 
        "Sentiment & Satisfaction"
    ])

    print("filter data : ", filtered_df.head(5))
    print("Info: ", filtered_df.info())
    with tab1:
        render_usage_insights_tab(filtered_df)
    
    with tab2:
        render_scheme_demand_tab(filtered_df)
    
    with tab3:
        render_citizen_pain_points_tab(filtered_df)
    
    with tab4:
        render_sentiment_satisfaction_tab(filtered_df)
    
if __name__ == "__main__":
    main()