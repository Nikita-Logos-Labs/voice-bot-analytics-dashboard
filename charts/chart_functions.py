import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import timedelta
import requests
from bs4 import BeautifulSoup

# ---------------------TAB 1----------------------#
def create_cumulative_minutes_chart(df):
    """Create cumulative call duration (in minutes) line chart"""    
    # Convert call_date to numeric, handling any string values
    df['call_date'] = pd.to_numeric(df['call_date'], errors='coerce')
    df = df.dropna(subset=['call_date'])
    # Filter out any unreasonably large values
    reasonable_dates = df['call_date'] < 100000  # Adjust this threshold as needed
    df = df[reasonable_dates]    
    if df.empty:
        fig = px.line(title="Cumulative Call Duration (Minutes) - No Valid Data")
        return fig
    try:
        excel_origin = pd.Timestamp("1899-12-30")
        df['call_date'] = excel_origin + pd.to_timedelta(df['call_date'], unit="D")        
    except Exception as e:
        print(f"Error converting dates: {e}")
        daily_minutes = (
            df.groupby('call_date')['duration_seconds']
            .sum()
            .reset_index(name='total_minutes')
        )
        daily_minutes['total_minutes'] = daily_minutes['total_minutes'] / 60
        daily_minutes = daily_minutes.sort_values('call_date')
        daily_minutes['cumulative_minutes'] = daily_minutes['total_minutes'].cumsum()        
        fig = px.line(
            daily_minutes,
            x='call_date',
            y='cumulative_minutes',
            markers=True,
            title="Cumulative Call Duration (Minutes) - Using Serial Dates",
            labels={'call_date': 'Date (Serial)', 'cumulative_minutes': 'Cumulative Duration (Minutes)'}
        )
        return fig
    daily_minutes = (
        df.groupby('call_date')['duration_seconds']
        .sum()
        .reset_index(name='total_minutes')
    )
    daily_minutes['total_minutes'] = daily_minutes['total_minutes'] / 60
    daily_minutes = daily_minutes.sort_values('call_date')    
    # Calculate cumulative sum
    daily_minutes['cumulative_minutes'] = daily_minutes['total_minutes'].cumsum()
    fig = px.line(
        daily_minutes,
        x='call_date',
        y='cumulative_minutes',
        markers=True,
        title="Cumulative Call Duration (Minutes)",
        labels={'call_date': 'Date', 'cumulative_minutes': 'Cumulative Duration (Minutes)'}
    )
    fig.update_layout(
        xaxis_title="📅 Date",
        yaxis_title=None,
        hovermode='x unified'
    )
    fig.update_traces(
        hovertemplate='<b>Cumulative Duration (Minutes):</b> %{y:.1f} <extra></extra>'+
                     '<extra></extra>'
    )
    return fig

def create_daily_total_minutes_chart(df):
    """Create daily total call duration (in minutes) line chart"""
    # Convert call_date to numeric, handling any string values
    df['call_date'] = pd.to_numeric(df['call_date'], errors='coerce')
    df = df.dropna(subset=['call_date'])
    # Filter out serial dates range from 1 (1900-01-01) to around 50000+ for recent dates
    reasonable_dates = df['call_date'] < 100000  # Adjust this threshold as needed
    df = df[reasonable_dates]    
    if df.empty:
        fig = px.line(title="Total Call Duration per Day (Minutes) - No Valid Data")
        return fig
    try:
        excel_origin = pd.Timestamp("1899-12-30")
        df['call_date'] = excel_origin + pd.to_timedelta(df['call_date'], unit="D")        
    except Exception as e:
        print(f"Error converting dates: {e}")
        daily_minutes = (
            df.groupby('call_date')['duration_seconds']
            .sum()
            .reset_index(name='total_minutes')
        )
        daily_minutes['total_minutes'] = daily_minutes['total_minutes'] / 60        
        fig = px.line(
            daily_minutes,
            x='call_date',
            y='total_minutes',
            markers=True,
            title="Total Call Duration per Day (Minutes) - Using Serial Dates",
            labels={'call_date': 'Date (Serial)', 'total_minutes': 'Total Duration (Minutes)'}
        )
        return fig
    daily_minutes = (
        df.groupby('call_date')['duration_seconds']
        .sum()
        .reset_index(name='total_minutes')
    )
    daily_minutes['total_minutes'] = daily_minutes['total_minutes'] / 60
    daily_minutes = daily_minutes.sort_values('call_date')
    fig = px.line(
        daily_minutes,
        x='call_date',
        y='total_minutes',
        markers=True,
        title="Total Call Duration per Day (Minutes)",
        labels={'call_date': 'Date', 'total_minutes': 'Total Duration (Minutes)'}
    )
    fig.update_traces(
        hovertemplate='<b>Total Duration (Minutes):</b> %{y:.1f}<extra></extra>'+
                     '<extra></extra>'
    )
    fig.update_layout(
        xaxis_title="📅 Date",
        yaxis_title=None,
        hovermode='x unified'
    )    
    return fig

def create_volume_chart(filtered_df, view="Daily"):
    """Create call volume chart with Hourly / Daily toggle"""

    # ---- Ensure datetime ----
    filtered_df["call_time"] = filtered_df["call_time"].astype(float)
    filtered_df["call_hour"] = (filtered_df["call_time"] * 24).astype(int)

    # ---- Hourly Stats ----
    hourly_calls = (
        filtered_df.groupby("call_hour")
        .size()
        .reset_index(name="count")
    )
    all_hours = pd.DataFrame({"call_hour": range(24)})
    hourly_calls = all_hours.merge(hourly_calls, on="call_hour", how="left").fillna(0)
    hourly_calls["label"] = hourly_calls["call_hour"].apply(lambda x: f"{x:02d}:00")

    # ---- Daily Stats ----
    filtered_df["call_date"] = pd.to_numeric(filtered_df["call_date"], errors="coerce")
    filtered_df["call_date"] = pd.to_datetime(
        filtered_df["call_date"], origin="1899-12-30", unit="D"
    )
    daily_calls = (
        filtered_df.groupby("call_date")
        .size()
        .reset_index(name="count")
    )
    daily_calls["label"] = daily_calls["call_date"].dt.strftime("%Y-%m-%d")

    # ---- Pick Data ----
    if view == "Hourly":
        data = hourly_calls
        x_title = "🕒 Hour of Day"
        hovertemplate = '<b>Time: </b>%{x}<br><b>Calls: </b>%{y}<br><extra></extra>'+'<extra></extra>'
    else:
        data = daily_calls
        x_title = "📅 Date"
        hovertemplate = "<b>Date: </b>%{x}<br><b>Calls: </b> %{y}<br><extra></extra>" + '<extra></extra>'

    # ---- Chart ----
    fig = px.line(
        data,
        x="label",
        y="count",
        title=f"Call Volume - {view}",
        markers=True
    )
    fig.update_xaxes(title=x_title, tickangle=45) 
    fig.update_yaxes(title=None) 
    fig.update_traces(hovertemplate=hovertemplate)
    return fig


def create_resolved_rate_chart(filtered_df, view="Daily"):
    """Create line chart showing resolved rate (%) with Hourly / Daily toggle"""
    # Preprocess time
    filtered_df["call_time"] = filtered_df["call_time"].astype(float)
    filtered_df["call_hour"] = (filtered_df["call_time"] * 24).astype(int)

    # ---- Hourly Stats ----
    hourly_stats = (
        filtered_df.groupby("call_hour")
        .agg(
            total_calls=("call_hour", "size"),
            resolved_calls=("resolved", lambda x: (x == True).sum())
        )
        .reset_index()
    )
    all_hours = pd.DataFrame({"call_hour": range(24)})
    hourly_stats = all_hours.merge(hourly_stats, on="call_hour", how="left").fillna(0)
    hourly_stats["resolved_rate"] = (
        (hourly_stats["resolved_calls"] / hourly_stats["total_calls"]) * 100
    ).fillna(0)
    hourly_stats["label"] = hourly_stats["call_hour"].apply(lambda x: f"{x:02d}:00")

    # ---- Daily Stats ----
    filtered_df["call_date"] = pd.to_datetime(filtered_df["call_date"])
    daily_stats = (
        filtered_df.groupby("call_date")
        .agg(
            total_calls=("call_date", "size"),
            resolved_calls=("resolved", lambda x: (x == True).sum())
        )
        .reset_index()
    )
    daily_stats["resolved_rate"] = (
        (daily_stats["resolved_calls"] / daily_stats["total_calls"]) * 100
    ).fillna(0)
    daily_stats["label"] = daily_stats["call_date"].dt.strftime("%Y-%m-%d")

    # ---- Pick Data Based on View ----
    if view == "Hourly":
        data = hourly_stats
        x_title = "🕒 Hour of Day"        
        hovertemplate = '<b>Time: </b>%{x}<br><b>Resolved Calls (%): </b>%{y:.2f}<br><extra></extra>'+'<extra></extra>'
    else:
        data = daily_stats
        x_title = "📅 Date"
        hovertemplate = "<b>Date: </b>%{x}<br><b>Resolved Calls (%): </b> %{y:.2f}<br><extra></extra>" + '<extra></extra>'


    # ---- Create Figure ----
    fig = px.line(
        data,
        x="label",
        y="resolved_rate",
        title=f"Call Resolved Rate (%) - {view}",
        markers=True
    )
    fig.update_xaxes(title=x_title, tickangle=45)  
    fig.update_yaxes(title=None)    
    fig.update_traces(hovertemplate=hovertemplate)
    return fig


def create_duration_histogram(filtered_df):
    """Create call duration distribution with fixed buckets"""
    bins = [0, 60, 180, 300, 600, float("inf")]
    labels = ["<1 min", "1–3 mins", "3–5 mins", "5–10 mins", ">10 mins"]
    filtered_df['duration_bucket'] = pd.cut(
        filtered_df['duration_seconds'],
        bins=bins,
        labels=labels,
        right=False 
    )
    bucket_counts = filtered_df['duration_bucket'].value_counts().reindex(labels).reset_index()
    bucket_counts.columns = ['duration_bucket', 'count']
    fig = px.bar(
        bucket_counts,
        x="duration_bucket",
        y="count",
        title="Call Duration Distribution",
        labels={"duration_bucket": "🕒 Call Duration", "count": ""},
        text="count"
    )
    fig.update_traces(textposition="outside")
    fig.update_traces(
        hovertemplate='<b>Duration: </b>%{x}<br><b>Count: </b>%{y}<extra></extra>'
    )
    return fig

city_sources = {
    "Ahmedabad": "https://www.latlong.net/place/ahmedabad-gujarat-india-1187.html",
    "Surat": "https://latitude.to/map/in/india/cities/surat",         # Example, update similarly
    "Vadodara": "https://latitude.to/map/in/india/cities/vadodara",
    "Rajkot": "https://latitude.to/map/in/india/cities/rajkot",
    "Gandhinagar": "https://latitude.to/map/in/india/cities/gandhinagar",
    "Bharuch": "https://latitude.to/map/in/india/cities/bharuch",     # And others...
    "Bhavnagar": "https://latitude.to/map/in/india/cities/bhavnagar",
    "Junagadh": "https://latitude.to/map/in/india/cities/junagarh",
    "Anand": "https://latitude.to/map/in/india/cities/anand",
    "Valsad": "https://latitude.to/map/in/india/cities/valsad"
}

def fetch_coord_from_latlong_net(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    # Finds the line with "Latitude" and "Longitude"
    lat = lon = None
    text = soup.get_text()
    for line in text.splitlines():
        if "Latitude" in line and "Longitude" in line:
            parts = line.split()
            try:
                lat = float(parts[1].strip(','))
                lon = float(parts[3])
                break
            except:
                continue
    return lat, lon

def create_gujarat_calls_map(df):
    city_coords = {
        "Ahmedabad": [23.0258, 72.5873],
        "Surat": [21.1702, 72.8311],
        "Vadodara": [22.2994, 73.2081],
        "Rajkot": [22.2916, 70.7932],
        "Gandhinagar": [23.2156, 72.6369],
        "Bharuch": [21.7051, 72.9959],
        "Bhavnagar": [21.7645, 72.1519],
        "Junagadh": [21.5222, 70.4579],
        "Anand": [22.5645, 72.9289],
        "Valsad": [20.5992, 72.9342]
    }
    df["lat"] = df["location"].map(lambda x: city_coords.get(x, [None, None])[0])
    df["lon"] = df["location"].map(lambda x: city_coords.get(x, [None, None])[1])
    df = df.dropna(subset=["lat", "lon"])
    # Aggregate counts
    call_counts = df.groupby(["location", "lat", "lon"]).size().reset_index(name="call_count")
    # Map
    fig = px.scatter_mapbox(
        call_counts,
        lat="lat",
        lon="lon",
        size="call_count",
        color="call_count",
        hover_name="location",
        hover_data={
            "call_count": True, 
            "lat": False, 
            "lon": False
        },
        zoom=6,
        mapbox_style="carto-positron",
        title="Calls Distribution Across Gujarat"
    )
    fig.update_traces(
        hovertemplate=" <b>%{hovertext}</b> <br> Calls: %{customdata[0]} "
    )
    fig.update_layout(
        mapbox_center={"lat": 22.3, "lon": 71.2}
    )
    return fig


# ------------------- TAB 2----------------------------#
def create_top_schemes_chart(filtered_df):
    """Create top requested schemes bar chart in pyramid style with custom hover"""
    top_schemes = filtered_df['scheme_requested'].value_counts().nlargest(10).reset_index()
    top_schemes.columns = ['scheme', 'count']
    top_schemes = top_schemes[::-1]
    fig = px.bar(
        top_schemes,
        x='count',
        y='scheme',
        orientation='h',
        title='Top 10 Requested Schemes',
        text='count', 
        hover_data={'scheme': False, 'count': True}, 
    )
    fig.update_traces(
        hovertemplate=' <b> %{y} </b><br> <b>Count: </b>%{x} <extra></extra>'
    )
    fig.update_layout(
        yaxis=dict(title='', autorange='reversed'),  # largest on top
        xaxis_title='Count',
    )
    return fig

def create_scheme_business_heatmap(filtered_df):
    """Create scheme demand by business type heatmap with proper width and count hover"""
    scheme_business = pd.crosstab(filtered_df['scheme_requested'], filtered_df['business_type'])
    fig = px.imshow(
        scheme_business,
        text_auto=True,        
        aspect="auto",           
        labels=dict(x="Profession", y="", color="Count"),
        title="Caller Profession-wise Scheme Demand"
    )
    fig.update_traces(
        hovertemplate=' <b>%{y} </b><br> <b>Profession: </b>%{x} <br> <b>Count: </b>%{z} <extra></extra>'
    )
    fig.update_layout(
        autosize=True,
        margin=dict(l=150, r=50, t=50, b=150),
        xaxis_tickangle=-45,
        yaxis=dict(tickmode='linear')
    )
    return fig

def create_scheme_region_sunburst(filtered_df):
    """Create scheme requests by region sunburst chart with custom hover"""
    region_scheme = (
        filtered_df.groupby(['location', 'scheme_requested'])
        .size()
        .reset_index(name='count')
    )
    fig = px.sunburst(
        region_scheme,
        path=['location', 'scheme_requested'],
        values='count',
        title='Scheme Requests by Region'
    )
    fig.update_traces(
        hovertemplate=' <b>%{label} </b><br> <b>Region: </b>%{parent} <br> <b>Count: </b>%{value} <extra></extra>'
    )
    return fig


# -------------------------TAB 3----------------------#

def create_common_actions_chart(filtered_df):
    """Create most common requested actions chart"""
    common_actions = filtered_df['requested_action'].value_counts().reset_index()
    common_actions.columns = ['action', 'count']
    fig = px.bar(common_actions, x='count', y='action', orientation='h', 
                title='Most Common Requested Actions')
    fig.update_traces(
        hovertemplate=' <b>%{y} </b><br><b>Count: </b>%{x} <extra></extra>'
    )
    fig.update_layout(
        yaxis_title=None,
        xaxis_title='Count',
    )
    return fig

def create_wordcloud(filtered_df):
    """Create responsive word cloud from queries (Plotly version)"""
    text = " ".join(
        filtered_df['requested_action'].astype(str) + " " +
        filtered_df['scheme_requested'].astype(str)
    )
    wordcloud = WordCloud(width=1200, height=800, background_color='white').generate(text)
    wc_img = wordcloud.to_array()
    fig = px.imshow(wc_img)
    fig.update_layout(
        title="Word Cloud of Requested Actions & Schemes",
        title_x=0,  # left align
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    fig.update_layout(height=400)  # set to whatever looks good
    fig.update_traces(hovertemplate=None, hoverinfo='skip')  # no hover tooltips
    return fig

def create_pain_point_chart(df, top_n=10):
    """Create bar chart of most common citizen pain points"""
    # Count frequency of pain points
    pain_points = df['citizen_pain_point'].value_counts().reset_index()
    pain_points.columns = ['pain_point', 'count']
    
    # Keep top N
    pain_points = pain_points.head(top_n)

    # Create bar chart
    fig = px.bar(
        pain_points,
        x='count',
        y='pain_point',
        orientation='h',
        title=f'Top {top_n} Citizen Pain Points',
        text='count'
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),  # Highest on top
        xaxis_title="Count",
        yaxis_title=None
    )
    fig.update_traces(
        hovertemplate=' <b>%{y} </b><br><b>Count: </b>%{x} <extra></extra>'
    )
    return fig
# -------------------------TAB 4----------------------------------#
def create_drop_off_pie_chart(filtered_df):
    """Create drop-off points pie chart"""
    drop_off_df = filtered_df[~filtered_df['resolved']]
    drop_off_reasons = drop_off_df['requested_action'].value_counts().reset_index()
    drop_off_reasons.columns = ['action', 'count']
    fig = px.pie(drop_off_reasons, values='count', names='action', 
                title='Drop-off Points by Action Type')
    fig.update_traces(
        hovertemplate=' <b>%{label}</b> <br> <b>Count: </b>%{value} <extra></extra>'
    )
    return fig


def create_agent_sentiment_pie(filtered_df):
    """Create agent sentiment distribution pie chart with custom hover"""
    agent_sentiment = filtered_df['sentiment_agent'].value_counts().reset_index()
    agent_sentiment.columns = ['sentiment', 'count']
    color_map = {
        'Positive': '#6abf69',  
        'Neutral': "#ffe681",   
        'Negative': "#f36060"  
    }
    fig = px.pie(
        agent_sentiment,
        values='count',
        names='sentiment',
        title='Agent Sentiment Distribution',
        color='sentiment',
        color_discrete_map=color_map
    )
    fig.update_traces(
        hovertemplate=' <b>%{label}</b> <br> <b>Count: </b>%{value} <extra></extra>'
    )
    return fig

def create_scheme_sentiment_pie(filtered_df):
    """Create scheme sentiment distribution pie chart"""
    scheme_sentiment = filtered_df['sentiment_scheme'].value_counts().reset_index()
    scheme_sentiment.columns = ['sentiment', 'count']
    color_map = {
        'Positive': '#6abf69',  
        'Neutral': "#ffe681",   
        'Negative': "#f36060"  
    }
    fig = px.pie(scheme_sentiment, values='count', names='sentiment', 
                title='Scheme Sentiment Distribution', color='sentiment',color_discrete_map=color_map)
    fig.update_traces(
        hovertemplate=' <b>%{label}</b> <br> <b>Count: </b>%{value} <extra></extra>'
    )
    return fig

color_map = {
    'Positive': '#6abf69',  # Green
    'Neutral': '#ffe681',   # Yellow
    'Negative': '#f36060'   # Red
}

def create_sentiment_trend_chart(filtered_df):
    """Create agent sentiment trend over time chart with custom hover and labels"""
    sentiment_trend = (
        filtered_df.groupby(['call_date', 'sentiment_agent'])
        .size()
        .reset_index(name='count')
    )
    fig = px.line(
        sentiment_trend,
        x='call_date',
        y='count',
        color='sentiment_agent',
        color_discrete_map=color_map,  # Apply custom colors
        title='Sentiment Trend Over Time',
        labels={'call_date': 'Date', 'sentiment_agent': 'Agent Sentiment', 'count': ''} 
    )
    fig.update_traces(
        customdata=sentiment_trend[['sentiment_agent']],
        hovertemplate=' <b>%{customdata[0]}</b> <br> <b>Date: </b>%{x|%d-%m-%y} <br> <b>Count: </b>%{y} <extra></extra>'
    )
    fig.update_layout(
        legend_title_text='Sentiment',
        yaxis_title=None,
        xaxis_title="📅 Date"

    )
    return fig

def create_scheme_sentiment_trend_chart(filtered_df):
    """Create scheme sentiment trend over time chart (like agent sentiment trend)"""
    scheme_trend = (
        filtered_df.groupby(['call_date', 'sentiment_scheme'])
        .size()
        .reset_index(name='count')
    )
    fig = px.line(
        scheme_trend,
        x='call_date',
        y='count',
        color='sentiment_scheme',
        color_discrete_map=color_map,  # Apply custom colors
        title='Scheme Sentiment Trend Over Time',
        labels={'call_date': 'Date', 'sentiment_scheme': 'Scheme Sentiment', 'count': 'Count'}
    )
    fig.update_traces(
        customdata=scheme_trend[['sentiment_scheme']],
        hovertemplate=' <b>%{customdata[0]}</b> <br> <b>Date: </b>%{x|%d-%m-%y} <br> <b>Count: </b>%{y} <extra></extra>'
    )
    fig.update_layout(
        legend_title_text='Sentiment',
        yaxis_title=None,
        xaxis_title="📅 Date"
    )
    return fig
