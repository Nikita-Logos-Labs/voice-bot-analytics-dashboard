import streamlit as st
from charts.chart_functions import (
    create_top_schemes_chart,
    create_scheme_business_heatmap,
    create_scheme_region_sunburst
)

def render_scheme_demand_tab(filtered_df):
    """Render the Scheme Demand & Awareness tab"""
    st.header("Scheme Demand & Awareness")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top requested schemes
        fig = create_top_schemes_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Scheme requests by region sunburst
        fig = create_scheme_region_sunburst(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    
    # Scheme demand by business type heatmap
    fig = create_scheme_business_heatmap(filtered_df)
    st.plotly_chart(fig, use_container_width=True)