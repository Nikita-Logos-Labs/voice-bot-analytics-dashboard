import streamlit as st
from charts.chart_functions import (
    create_volume_chart,
    create_duration_histogram,
    create_resolved_rate_chart,
    create_daily_total_minutes_chart,
    create_gujarat_calls_map,
    create_cumulative_minutes_chart,
    fetch_coord_from_latlong_net, 
    city_sources,


)
def render_usage_insights_tab(filtered_df):
    """Render the Usage Insights tab"""
    st.header("📈 Usage Insights")  

    col01,col02 = st.columns(2)
    with col01:
        # Daily total minutes chart
        fig = create_daily_total_minutes_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    with col02:        
        # cumulative - daily minutes chart
        fig = create_cumulative_minutes_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    
    # daily/ hourly filter
    col1,col2=st.columns([4,2])
    with col2:
        view = st.selectbox("View", ["Daily", "Hourly"], index=0) 
    
    col1, col2 = st.columns(2)    
    with col1:
        # Daily call volume chart
        fig = create_volume_chart(filtered_df, view)
        st.plotly_chart(fig, use_container_width=True)
        
        # Call duration distribution
        fig = create_duration_histogram(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # resolved rate
        fig = create_resolved_rate_chart(filtered_df, view=view)
        st.plotly_chart(fig, use_container_width=True)
        # Region-wise count
        fig = create_gujarat_calls_map(filtered_df)
        st.plotly_chart(fig, use_container_width=True)