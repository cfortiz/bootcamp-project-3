import streamlit as st
import pandas as pd
from pymongo import MongoClient
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# MongoDB connection setup
def get_mongo_client():
    mongo = MongoClient("mongodb://localhost:27017/")
    return mongo

def get_data_from_mongodb():
    mongo = get_mongo_client()
    db = mongo['worldHappiness']
    collection = db['table']
    
    # Query all documents in the collection
    data = list(collection.find())
    
    # Close client connection
    mongo.close()

    return data

# Convert MongoDB data to a pandas DataFrame

def mongo_data_to_dataframe(data):
    df = pd.DataFrame(data)

    # Drop the MongoDB ID field
    if "_id" in df.columns:
        df = df.drop("_id", axis=1)

    # Convert year format to int
    df['year'] = df['year'].astype(int)

    return df

# Load the country coordinates from CSV

def load_country_coordinates(csv_file):
    file_path = f'back-end/{csv_file}'
    return pd.read_csv(file_path)

# Function to determine the color based on happiness score
def get_color_for_score(score):
    if score >= 7:
        return "green"
    elif score >= 5:
        return "yellow"
    else:
        return "red"

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

        # Load the coordinates from the CSV file
        coordinates_df = load_country_coordinates('country_coordinates.csv')

        # Merge MongoDB data with the coordinates DataFrame
        df = pd.merge(df, coordinates_df, on='Country name', how='left')

        # Filter out rows missing geocoordinates
        df = df.dropna(subset=['latitude', 'longitude'])

        # Create dropdowns for countries and years
        selected_countries = st.multiselect('Select Countries', df['Country name'].unique(), default=df['Country name'].unique())
        selected_years = st.multiselect('Select Years', df['year'].unique(), default=df['year'].max())  # Default to the latest year

        # Filter DataFrame based on the selected countries and years
        df_filtered = df[(df['Country name'].isin(selected_countries)) & (df['year'].isin(selected_years))]

        # Create a Folium map
        m = folium.Map(location=[20, 0], zoom_start=2)

        # Add Choropleth layer for Life Ladder (Happiness Score)
        folium.Choropleth(
            geo_data='back-end/countries.geo.json',  # Path to the GeoJSON file for country borders
            name='choropleth',
            data=df_filtered,
            columns=['Country name', 'Life Ladder'],  # Columns for choropleth
            key_on='feature.properties.name',  # Match country names in GeoJSON and DataFrame
            fill_color='YlGnBu',  # Color scheme
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Life Ladder (Happiness Score)',
        ).add_to(m)

        # Create a marker cluster layer for markers
        marker_cluster = MarkerCluster().add_to(m)

        # Add Circle markers for each filtered country
        for i, row in df_filtered.iterrows():
            happiness_score = row['Life Ladder']
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=7,  # Adjust marker size
                popup=f"{row['Country name']} - Happiness Score: {happiness_score}",
                color=get_color_for_score(happiness_score),
                fill=True,
                fill_color=get_color_for_score(happiness_score),
                fill_opacity=0.7
            ).add_to(marker_cluster)

        # Display Folium map in Streamlit
        st_folium(m, width=1000, height=600)

if __name__ == "__main__":
    main()