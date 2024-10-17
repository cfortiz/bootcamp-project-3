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

# Configure the streamlit page layout
st.set_page_config(layout='wide')


def get_mongo_client():
    """Connect to MongoDB using a pymongoMongoClient"""
    mongo = MongoClient('mongodb://localhost:27017/')
    return mongo


def get_fig_data_from_mongodb():
    """Fetch data from the mongo 'fig' collection"""
    mongo = get_mongo_client()
    db = mongo['worldHappiness']
    fig_collection = db['fig']
    fig_data = list(fig_collection.find())
    mongo.close()
    return fig_data


def get_table_data_from_mongodb():
    """Fetch data from the mongo 'table' collection"""
    mongo = get_mongo_client()
    db = mongo['worldHappiness']
    table_collection = db['table']
    table_data = list(table_collection.find())
    mongo.close()
    return table_data


def mongo_data_to_fig_df(fig_data):
    """Convert MongoDB fig data to pandas DataFrame"""
    fig_df = pd.DataFrame(fig_data)
    if '_id' in fig_df.columns:
        fig_df = fig_df.drop('_id', axis=1)
    return fig_df


def mongo_data_to_table_df(table_data):
    """Convert MongoDB table data to pandas DataFrame"""
    table_df = pd.DataFrame(table_data)
    if '_id' in table_df.columns:
        table_df = table_df.drop('_id', axis=1)
    return table_df


def load_country_coordinates(csv_file):
    """Load country coordinates from CSV file"""
    return pd.read_csv('back-end/resources/country_coordinates.csv')


def get_year_options():
    """Get the list of all year option values
    
    Returns:
        A list with all year option values as strings in reverse chronological
        order.
    
    """
    return list(map(str, reversed(range(MIN_YEAR_OPTION, MAX_YEAR_OPTION+1))))


def main():
    # Set page title, and add dashboard tabs
    st.title("World Happiness Dashboard")
    tab1, tab2 = st.tabs(["2024 World Map", "Compare Countries by Year"])

    # Filter options for year and country
    year_options = get_year_options()
    country_options = ['Afghanistan','Albania','Algeria','Angola','Argentina','Armenia','Australia','Austria','Azerbaijan',
                       'Bahrain','Bangladesh','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia','Bosnia and Herzegovina','Botswana','Brazil','Bulgaria','Burkina Faso','Burundi',
                       'Cambodia','Cameroon','Canada','Central African Republic','Chad','Chile','China','Colombia','Comoros','Congo (Brazzaville)','Congo (Kinshasa)','Costa Rica','Croatia','Cuba','Cyprus','Czechia',
                       'Denmark','Djibouti','Dominican Republic','Ecuador','Egypt','El Salvador','Estonia','Eswatini','Ethiopia',
                       'Finland','France','Gabon','Gambia',	'Georgia','Germany','Ghana','Greece','Guatemala','Guinea','Guyana',
                       'Haiti','Honduras','Hong Kong S.A.R. of China','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','Israel','Italy','Ivory Coast',
                       'Jamaica','Japan','Jordan','Kazakhstan','Kenya','Kosovo','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho','Liberia','Libya','Lithuania','Luxembourg',
                       'Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','Mauritania','Mauritius','Mexico','Moldova','Mongolia','Montenegro','Morocco','Mozambique','Myanmar',
                       'Namibia','Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria','North Macedonia','Norway','Oman',
                       'Pakistan','Panama','Paraguay','Peru','Philippines','Poland','Portugal','Qatar','Romania','Russia','Rwanda',
                       'Saudi Arabia','Senegal','Serbia','Sierra Leone','Singapore','Slovakia','Slovenia','Somalia','Somaliland region','South Africa','South Korea','South Sudan','Spain','Sri Lanka','State of Palestine','Sudan','Suriname','Sweden','Switzerland','Syria',
                       'Taiwan Province of China','Tajikistan','Tanzania','Thailand','Togo','Trinidad and Tobago','Tunisia','Turkmenistan','Türkiye',
                       'Uganda','Ukraine','United Arab Emirates','United Kingdom','United States','Uruguay','Uzbekistan','Venezuela','Vietnam','Yemen','Zambia','Zimbabwe']
    metric_options = ['Life Ladder','Log GDP per capita',
                      'Social support','Healthy life expectancy at birth',
                      'Freedom to make life choices','Generosity',
                      'Perceptions of corruption','Positive affect','Negative affect']


    # Fetch data from both collections
    fig_data = get_fig_data_from_mongodb()
    table_data = get_table_data_from_mongodb()

    # Convert both collections data to DataFrames to use in Streamlit
    if fig_data and table_data:
        fig_df = mongo_data_to_fig_df(fig_data)
        table_df = mongo_data_to_table_df(table_data)
        # Load coordinates csv into a DataFrame and merge with the fig_df to create the 2024 Map
        coordinates_df = load_country_coordinates('back-end/resources/country_coordinates.csv')
        merged_fig_df = pd.merge(fig_df, coordinates_df, on='Country name', how='left')

# -------------------------------------------------- TAB 1: WORLD MAP (map does not change based on filtered data)  -------------------------------------------------- #
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
            geo_data='back-end/resources/countries.geo.json',
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

# -------------------------------------------------- TAB 2: COMPARING COUNTRIES  -------------------------------------------------- #

    with tab2:
        
        # Dropdown to select year
        country_selection
        metric_selection = st.selectbox("Select a metric to see year to year:", metric_options)
        year_selection = st.slider("Select a range of years:", 2014, 2023, (2018,2022))
        st.write("Year Range:", year_selection)

        # Filtered data based on Country, Metric, Year Range selection
        filtered_table_df = table_df[
            (table_df['Country name'] == country_selection) &
            (table_df['year'] >= year_selection[0]) &
            (table_df['year'] <= year_selection[1])
        ]

        # Create Line Chart
        if not filtered_table_df.empty:
            fig = px.line(filtered_table_df,
                          x='year',
                          y=metric_selection,
                          title=f'{metric_selection} over time for {country_selection}')
            
            # Update layout
            fig.update_layout(
                xaxis = dict(
                    tickmode = 'linear',
                    tick0 = filtered_table_df['year'].min(),
                    dtick = 1
                )
            )
            
            # Display the line chart in Streamlit
            st.plotly_chart(fig)



if __name__ == "__main__":
        main()


