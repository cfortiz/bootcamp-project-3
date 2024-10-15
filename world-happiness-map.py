# -------------------------------------------------- libraries and dependencies -------------------------------------------------- #
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
import plotly.graph_objects as go
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from pymongo import MongoClient

# -------------------------------------------------- DEFINE: convert mongodb fig 2024 to pandas df and add country coordinates -------------------------------------------------- #
def get_mongo_client():
    mongo = MongoClient('mongodb://localhost:27017/')
    return mongo

# Fetch data from 'fig' collection
def get_fig_data_from_mongodb():
    mongo = get_mongo_client()
    db = mongo['worldHappiness']
    fig_collection = db['fig']
    fig_data = list(fig_collection.find())
    mongo.close()
    return fig_data

# Fetch data from 'table' collection
def get_table_data_from_mongodb():
    mongo = get_mongo_client()
    db = mongo['worldHappiness']
    table_collection = db['table']
    table_data = list(table_collection.find())
    mongo.close()
    return table_data

# Convert MongoDB fig data to pandas DataFrame
def mongo_data_to_fig_df(fig_data):
    fig_df = pd.DataFrame(fig_data)
    if '_id' in fig_df.columns:
        fig_df = fig_df.drop('_id', axis=1)
    return fig_df

# Convert MongoDB table data to pandas DataFrame
def mongo_data_to_table_df(table_data):
    table_df = pd.DataFrame(table_data)
    if '_id' in table_df.columns:
        table_df = table_df.drop('_id', axis=1)
    return table_df

def load_country_coordinates(csv_file):
    return pd.read_csv('back-end/country_coordinates.csv')

# -------------------------------------------------- FETCH: STREAMLIT MAP -------------------------------------------------- #
def main():
    # Title of Page
    st.title("World Happiness Dashboard")
    # Tabs listed under the dashboard
    tab1, tab2, tab3 = st.tabs(["2024 World Map", "Compare Countries by Year", "Data Tables"])

    # Filter options for year and country
    year_options = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014']
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


    # Fetch data from both collections
    fig_data = get_fig_data_from_mongodb()
    table_data = get_table_data_from_mongodb()

    # Convert both collections data to DataFrames to use in Streamlit
    if fig_data and table_data:
        fig_df = mongo_data_to_fig_df(fig_data)
        table_df = mongo_data_to_table_df(table_data)
        # Load coordinates csv into a DataFrame and merge with the fig_df to create the 2024 Map
        coordinates_df = load_country_coordinates('back-end/country_coordinates.csv')
        merged_fig_df = pd.merge(fig_df, coordinates_df, on='Country name', how='left')

# -------------------------------------------------- TAB 1: WORLD MAP (map does not use filtered data)  -------------------------------------------------- #
        with tab1:
            col1, col2 = st.columns([1,3])
            # Dropdown to select country
            country_selection = st.selectbox("Select a country to see 2024 metrics:", country_options)
            # Filter data for the selected country
            country_fig_data = merged_fig_df[merged_fig_df['Country name'] == country_selection]

            if not country_fig_data.empty:
                # Display country-specific data
                with col1:
                    st.subheader(f'2024 {country_selection} Metrics')
                    st.metric("Happiness Score", round(country_fig_data['Ladder score'].values[0], 2))
                    st.metric('Log GDP per Capita', round(country_fig_data['Explained by: Log GDP per capita'].values[0], 2))
                    st.metric('Healthy life expectancy', round(country_fig_data['Explained by: Healthy life expectancy'].values[0], 2))
                    st.metric('Freedom to make life choices', round(country_fig_data['Explained by: Freedom to make life choices'].values[0], 2))
                    st.metric('Generosity', round(country_fig_data['Explained by: Generosity'].values[0], 2))
                    st.metric('Perceptions of corruption', round(country_fig_data['Explained by: Perceptions of corruption'].values[0], 2))
                    st.metric('Dystopia + residual', round(country_fig_data['Dystopia + residual'].values[0], 2))
                    # add more metrics
                
                # Display Folium map with zoom
                fig_map = folium.Map(location=[20,0], zoom_start=4)

                # Choropleth Layer
                folium.Choropleth(
                    geo_data='back-end/countries.geo.json',
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
                            # popup=
                            icon=folium.Icon(color='blue', icon='info-sign'),
                        ).add_to(marker_cluster)

                # Display Folium map in Streamlit
                st_folium(fig_map, width=700, height=500)




if __name__ == "__main__":
        main()


