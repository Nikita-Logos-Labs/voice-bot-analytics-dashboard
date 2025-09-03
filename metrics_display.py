import streamlit as st

def display_key_metrics(filtered_df):
    """Display key metrics in compact stylish cards"""
    col1, col2, col3, col4 = st.columns(4)

    total_calls = len(filtered_df)
    total_duration_min = filtered_df['duration_seconds'].sum() / 60
    avg_duration = filtered_df['duration_seconds'].mean()
    completion_rate = filtered_df['resolved'].mean() * 100

    metrics = [
        ("Total Calls", total_calls),
        ("Total Duration (min)", f"{total_duration_min:.1f}"),
        ("Avg. Duration (sec)", f"{avg_duration:.1f}"),
        ("Resolved Rate", f"{completion_rate:.1f}%")
    ]

    card_style = """
        <div style="
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 4px 3px;
            margin: 5px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            transition: all 0.2s ease-in-out;
            min-height: 50px;
        " onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)'; 
                       this.style.transform='scale(1.02)';"
          onmouseout="this.style.boxShadow='0 2px 6px rgba(0,0,0,0.08)'; 
                       this.style.transform='scale(1)';">
            <h5 style="margin:0; color:#555; font-size:15px;">{label}</h5>
            <p style="margin:0px 0 0 0; font-size:30px; font-weight:500; color:#222; padding:0;">{value}</p>
        </div>
    """

    for col, (label, value) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(card_style.format(label=label, value=value), unsafe_allow_html=True)
