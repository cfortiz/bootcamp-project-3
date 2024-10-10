# import libraries and dependencies
import streamlit as st # requirement 3: your project must include at least one JavaScript or Python library that we did not cover.
from pymongo import MongoClient # requirement 2: data must be stored in and extracted from at least one database (PostgreSQL, MongoDB, SQLite, etc).
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import plotly.express as px

# initialize geolocator
geolocator = Nominatim(user_agent='geoapiExercises')

# function to get coordinates (latitude, longitude) based on country name
def get_coordinates(country_name):
    try:
        location = geolocator.geocode(country_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except:
        return None

# MongoDB connection setup
def get_mongo_client():
    # Replace with your MongoDB connection string
    mongo = MongoClient("mongodb://localhost:27017/")
    return mongo

# Fetch data from MongoDB
def get_data_from_mongodb():
    mongo = get_mongo_client()
    db = mongo['worldHappiness']  # Database name
    collection = db['table']  # Collection name
    
    # Query all documents in the collection
    data = list(collection.find())

    # Close the client connection
    mongo.close()
    
    return data

# Convert MongoDB data to a pandas DataFrame
def mongo_data_to_dataframe(data):
    # Convert MongoDB list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    
    # Make adjustments to dataframe
    # Drop the MongoDB ID field
    if "_id" in df.columns:
        df = df.drop("_id", axis=1)
    
    # convert year from str to int so that the year no longer has a comma
    df['year'] = df['year'].astype(int)

    # add latitude and longitude columns by applying the geocoding function
    df['latitude'],df['longitude'] = zip(*df['Country name'].apply(get_coordinates))

    return df

# Streamlit app
def main():
    st.title("World Happiness Dashboard")
    st.write("This is a Python-based frontend application.")

    # Fetch data from MongoDB
    data = get_data_from_mongodb()

    if data:
        df = mongo_data_to_dataframe(data)
    else:
        st.write("No data found in MongoDB.")
        return

    # Dropdown for selecting the year
    selected_year = st.selectbox('Select Year', df['year'].unique())

    # Filter data based on the selected year
    filtered_data = df[df['year'] == selected_year]

    # Create a choropleth map using Plotly Express
    fig = px.choropleth(filtered_data, 
                        locations='Country name', 
                        locationmode='country names', 
                        color='Happiness Score', 
                        title=f'World Happiness Scores by Country in {selected_year}',
                        color_continuous_scale=px.colors.sequential.Plasma)

    # Display the map in Streamlit
    st.plotly_chart(fig, use_container_width=False, width=900, height=600)

    # Create Folium map
    m = folium.Map(location=[20, 0], zoom_start=4, tiles='OpenStreetMap')

    # Add markers for the filtered data
    for i, row in filtered_data.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['Country name']} - Happiness Score: {row['Happiness Score']}"            
            ).add_to(m)

    # Display the map
    st_folium(m, width=1000, height=600)

if __name__ == "__main__":
    main()






