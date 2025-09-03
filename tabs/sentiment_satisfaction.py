import streamlit as st
from charts.chart_functions import (
    create_agent_sentiment_pie,
    create_scheme_sentiment_pie,
    create_sentiment_trend_chart,
    create_scheme_sentiment_trend_chart,
    create_drop_off_pie_chart
)

def render_sentiment_satisfaction_tab(filtered_df):
    """Render the Sentiment & Satisfaction tab"""
    st.header("Sentiment & Satisfaction")
     # Drop-off points pie chart
    fig = create_drop_off_pie_chart(filtered_df)
    st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Agent sentiment distribution
        fig = create_agent_sentiment_pie(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Scheme sentiment distribution
        fig = create_scheme_sentiment_pie(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sentiment trend over time
        fig = create_sentiment_trend_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Scheme sentiment heatmap
        fig = create_scheme_sentiment_trend_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)