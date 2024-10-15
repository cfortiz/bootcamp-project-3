# IMPORTS + DEPENDENCIES
import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# SET VARIABLES
Happiness_Score = df['Life Ladder']



# MONGO CLIENT
def get_mongo_client():
    mongo = MongoClient("mongodb://localhost:27017/")
    return mongo

# MONGO DB + COLLECTION
def get_data_from_mongodb():
    mongo = get_mongo_client()
    db = mongo['worldHappiness'] # SET DB NAME FROM MONGODB
    collection = db['table'] # SET COLLECTION NAME FROM MONGODB
    
    data = list(collection.find()) # QUERY ALL DOCUMENTS 
    
    mongo.close() # CLOSE CLIENT CONNECTION

    return data

# CONVERT MONGO TO PANDAS DF
def mongo_data_to_dataframe(data):
    df = pd.DataFrame(data)

# Drop the MongoDB ID field

    if "_id" in df.columns:
        df = df.drop("_id", axis=1)

# Convert 2,024 to 2024 year format

    df['year'] = df['year'].astype(int)

    return df

# Read country_coordinates CSV
@st.cache_data
def load_country_coordinates(csv_file):
    file_path = f'back-end/{csv_file}'
    return pd.read_csv(file_path)

# Streamlit app

def main():
    st.title("World Happiness Dashboard")
    st.write("Interactive Map")

    # Fetch data from MongoDB
    data = get_data_from_mongodb()

    if data:
        # Convert to DataFrame
        df = mongo_data_to_dataframe(data)

        # Filter out rows with no data
        df = df.dropna(subset=['Life Ladder', 'Country name'])

        # Load coordinates from CSV file
        coordinates_df = load_country_coordinates('country_coordinates.csv')

        # Merge mongo db with the coordinates_df
        df = pd.merge(df, coordinates_df, on='Country name', how='left')

        # Filter out if missing geocoordinates
        df = df.dropna(subset=['latitude', 'longitude'])

# Create Dropdowns

        # Create dropdowns for countries and years
        selected_countries = st.multiselect('Select Countries', df['Country name'].unique(), default=df['Country name'].unique())
        selected_years = st.multiselect('Select Years', df['year'].unique(), default=df['year'].max())  # Default to the latest year
        selected_metric = st.selectbox(
            "Select metric:",
            df[''].unique(),

            index=None,

        )

        # Filter DataFrame based on the selected countries and years
        filtered_df = df[(df['Country name'].isin(selected_countries)) & (df['year'].isin(selected_years))]

        
        # Create Folium map
        m = folium.Map(location=[20,0], zoom_start=2)

        # Add geojson path
        geojson_path = 'back-end/countries.geo.json'

        # Add Choropleth layer for Life Ladder (Happiness Score)
        folium.Choropleth(
            geo_data = geojson_path,
            name = 'Choropleth',
            data = filtered_df,
            columns = ['Country name', 'Life Ladder'],
            key_on = 'feature.properties.name',
            fill_color = 'Blues',
            fill_opacity = 0.7,
            line_opacity = 0.2,
            legend_name = 'Life Ladder (Happiness Score)',
        ).add_to(m)

        # Create a marker cluster layer
        marker_cluster = MarkerCluster().add_to(m)

        # Add markers for each country
        for i, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['Country name']} - Happiness Score: {row['Life Ladder']}"
            ).add_to(m)
        
        # Display folium map with Streamlit
        st_folium(m, width=1000, height=600)

        # create choropleth map
        fig = px.choropleth(df,
                            locations='Country name',
                            locationmode='country names',
                            color='Life Ladder',
                            title='World Happiness Scores by Country',
                            color_continuous_scale=px.colors.sequential.Plasma)
        
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
         