import streamlit as st
from charts.chart_functions import (
    create_common_actions_chart,
    create_wordcloud,
    create_pain_point_chart
)

def render_citizen_pain_points_tab(filtered_df):
    """Render the Citizen Pain Points tab"""
    st.header("Citizen Pain Points")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Most common requested actions
        fig = create_common_actions_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)     
    with col2:        
        st.write(" ")
        st.write(" ")
        fig = create_wordcloud(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    fig = create_pain_point_chart(filtered_df)
    st.plotly_chart(fig, use_container_width=True)