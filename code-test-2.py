import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import plotly.graph_objects as go

# Function to create the emoji marker based on score
def get_emoji_for_score(score):
    if score >= 6:
        return "😊"  # Happy face
    elif score >= 4.5:
        return "🙂"  # Neutral face
    else:
        return "😟"  # Sad face

# Function to create color for gauge chart
def get_color_for_gauge(score):
    if score >= 6:
        return "green"
    elif score >= 4.5:
        return "orange"
    else:
        return "red"

# Sample data for demo
df = pd.DataFrame({
    'Country name': ['Brazil', 'Canada', 'USA', 'India', 'China'],
    'year': [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014],
    'Life Ladder': [6.27, 7.32, 6.89, 5.56, 5.20],
    'latitude': [-14.2350, 56.1304, 37.0902, 20.5937, 35.8617],
    'longitude': [-51.9253, -106.3468, -95.7129, 78.9629, 104.1954]
})

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["Map", "Compare Countries", "Credits"])

# Tab 1: Main Map with Smiley Markers
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_country = st.selectbox("Select a country", df['Country name'])
        year = st.selectbox("Select a report year", df['year'].unique())
        
        # Happiness Score and Age chart placeholder
        st.subheader(f"{selected_country} in {year}")
        score = df[df['Country name'] == selected_country]['Life Ladder'].values[0]
        st.metric("Happiness Score", f"{score:.2f}")

        # Placeholder for "Happiness Score by Age"
        st.bar_chart([score-1, score, score+0.5, score-0.5])

        # Gauge Chart for Average Life Evaluation
        gauge_color = get_color_for_gauge(score)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Average Life Evaluation"},
            gauge={'axis': {'range': [0, 10]},
                   'bar': {'color': gauge_color}}))
        st.plotly_chart(fig)
    
    with col2:
        # Folium Map with Smiley Markers
        m = folium.Map(location=[0, 0], zoom_start=2)
        
        marker_cluster = MarkerCluster().add_to(m)
        for i, row in df.iterrows():
            emoji = get_emoji_for_score(row['Life Ladder'])
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['Country name']} - Happiness Score: {row['Life Ladder']}",
                icon=folium.DivIcon(html=f'<div style="font-size:24px;">{emoji}</div>')
            ).add_to(marker_cluster)
        
        st_folium(m, width=700, height=500)

# Tab 2: Compare Countries (Add Comparison Logic)
with tab2:
    st.write("Compare Countries Section")
    country1 = st.selectbox("Select first country", df['Country name'])
    country2 = st.selectbox("Select second country", df['Country name'])
    st.write(f"Comparison between {country1} and {country2}.")

# Tab 3: Credits Section
with tab3:
    st.write("Credits Section")