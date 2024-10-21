from functools import lru_cache as memoized

import folium
from folium.plugins import MarkerCluster
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pymongo import MongoClient
import streamlit as st
from streamlit_folium import st_folium


MIN_YEAR_OPTION = 2014
MAX_YEAR_OPTION = 2023
DEFAULT_YEAR_RANGE = (2018, 2022)

# Configure the streamlit page to use a wide layout
st.set_page_config(layout='wide')


def get_mongo_client():
    """Connect to MongoDB using a pymongoMongoClient"""
    mongo = MongoClient('mongodb://localhost:27017/')
    return mongo


def get_data_from_mongo(collection_name):
    """Fetch all data from a collection in worldHappiness mongo db
    
    Args:
        collection: String name of the collection
    
    Returns:
        A list of all documents in the mongo worldHappiness db collection passed
        as an argument.
    
    """
    with get_mongo_client() as mongo:
        mongo = get_mongo_client()
        db = mongo.worldHappiness
        collection = db[collection_name]
        return list(collection.find({}, {'_id': 0}))


def get_fig_data_from_mongodb():
    """Fetch data from the mongo 'fig' collection"""
    return get_data_from_mongo(collection_name='fig')


def get_table_data_from_mongodb():
    """Fetch data from the mongo 'table' collection"""
    return get_data_from_mongo(collection_name='table')


def mongo_data_to_fig_df(fig_data):
    """Convert MongoDB fig data to pandas DataFrame"""
    fig_df = pd.DataFrame(fig_data)
    return fig_df


def mongo_data_to_table_df(table_data):
    """Convert MongoDB table data to pandas DataFrame"""
    table_df = pd.DataFrame(table_data)
    return table_df


def load_country_coordinates(csv_file):
    """Load country coordinates from CSV file"""
    return pd.read_csv('back_end/resources/country_coordinates.csv')


# Memoized for performance, since we only need to get year options once
@memoized
def get_year_options():
    """Get the list of all year option values for streamlit controls

    Returns:
        A list with all year option values as strings in reverse chronological
        order.

    """
    return list(map(str, reversed(range(MIN_YEAR_OPTION, MAX_YEAR_OPTION+1))))


# Memoized for performance, since we only need to get country options once
@memoized
def get_country_options():
    """Get the list of all country option values for streamlit controls

    Returns:
        A list of all country names as strings to be used as country option
        values.

    """
    mongo = get_mongo_client()
    db = mongo.worldHappiness
    countries = set()
    for collection_name in ('fig', 'table'):
        collection = db[collection_name]
        for result in collection.find({}, {'Country name': 1, '_id': 0}):
            country = result['Country name']
            countries.add(country)
    return sorted(countries)


def main():
    # Set page title, and add dashboard tabs
    st.title("World Happiness Dashboard")
    tab1, tab2 = st.tabs(["2024 World Map", "Compare Countries by Year"])

    # Filter options for year and country
    year_options = get_year_options()
    country_options = get_country_options()
    metric_options = [  # Hard-coded variable options
        'Life Ladder',
        'Log GDP per capita',
        'Social support',
        'Healthy life expectancy at birth',
        'Freedom to make life choices',
        'Generosity',
        'Perceptions of corruption',
        'Positive affect',
        'Negative affect',
    ]

    # Fetch data from both collections
    fig_data = get_fig_data_from_mongodb()
    table_data = get_table_data_from_mongodb()

    # Convert both collections data to DataFrames to use in Streamlit
    if fig_data and table_data:
        fig_df = mongo_data_to_fig_df(fig_data)
        table_df = mongo_data_to_table_df(table_data)

        # Load coordinates csv into a DataFrame and merge with the fig_df to create the 2024 Map
        coordinates_df = load_country_coordinates('back_end/resources/country_coordinates.csv')
        merged_fig_df = pd.merge(fig_df, coordinates_df, on='Country name', how='left')

    # Streamlit tab 1: World Happiness Map for year 2024
    # Note: map does not update in realtime based on filtered data
    with tab1:
        # Dropdown to select country
        country_selection = st.selectbox("Select a country to see 2024 metrics:", country_options)

        # Filter data for the selected country
        country_fig_data = merged_fig_df[merged_fig_df['Country name'] == country_selection]
        st.header(f'2024 {country_selection} Metrics')

        col1, col2, col3 = st.columns(3)

        if not country_fig_data.empty:
            # Display country-specific data
            col1.metric("Happiness Score", round(country_fig_data['Ladder score'].values[0], 2))
            col1.metric('Log GDP per Capita', round(country_fig_data['Explained by: Log GDP per capita'].values[0], 2))
            col2.metric('Healthy Life Expectancy', round(country_fig_data['Explained by: Healthy life expectancy'].values[0], 2))
            col2.metric('Freedom to make Life Choices', round(country_fig_data['Explained by: Freedom to make life choices'].values[0], 2))
            col3.metric('Generosity', round(country_fig_data['Explained by: Generosity'].values[0], 2))
            col3.metric('Perceptions of Corruption', round(country_fig_data['Explained by: Perceptions of corruption'].values[0], 2))
        fig_map = folium.Map(location=[20,0], zoom_start=2)

        # Choropleth Layer
        folium.Choropleth(
            geo_data='back_end/resources/countries.geo.json',
            name='choropleth',
            data=merged_fig_df,
            columns=['Country name', 'Ladder score'],
            key_on='feature.properties.name',
            fill_color='YlGnBu',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='World Happiness Score',
        ).add_to(fig_map)

        # Marker Cluster Layer
        marker_cluster = MarkerCluster().add_to(fig_map)
        for _, row in merged_fig_df.iterrows():
            if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    tooltip=f"{row['Country name']}: {row['Ladder score']}" ,
                    icon=folium.Icon(color='blue', icon='info-sign'),
                ).add_to(marker_cluster)

        # Display Folium map in Streamlit
        st_folium(fig_map, width=1000, height=500)

    # Streamlit tab 2: Comparing Countries
    with tab2:
        # Dropdown to select year
        # country_selection
        metric_selection = st.selectbox(
            "Select a metric to see year to year:",
            metric_options
        )
        year_selection = st.slider(
            "Select a range of years:",
            MIN_YEAR_OPTION, MAX_YEAR_OPTION,
            DEFAULT_YEAR_RANGE
        )
        st.write("Year Range:", year_selection)

        # Filter data based on Country, Metric, Year Range selection
        filtered_table_df = table_df[
            (table_df['Country name'] == country_selection) &
            (table_df['year'] >= year_selection[0]) &
            (table_df['year'] <= year_selection[1])
        ]

        # Create Line Chart
        if not filtered_table_df.empty:
            fig = px.line(
                filtered_table_df,
                x='year',
                y=metric_selection,
                title=f'{metric_selection} over time for {country_selection}'
            )

            # Update layout
            fig.update_layout(
                xaxis=dict(
                    tickmode='linear',
                    tick0=filtered_table_df['year'].min(),
                    dtick=1,
                )
            )

            # Display the line chart in Streamlit
            st.plotly_chart(fig)


if __name__ == "__main__":
        main()
