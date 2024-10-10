import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
import folium
from streamlit_folium import st_folium
# from geopy.geocoders import Nominatim
# import time


# mongo = MongoClient(port=27017)
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

# ######################### Coordinates ####################
# def get_coordinates(country_name):
#     geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)
#     try:
#         location=geolocator.geocode(country_name)
#         time.sleep(1) # delay to avoid hitting API rate limits
#         if location:
#             return location.latitude, location.longitude
#         else:
#             return None, None
#     except Exception as e:
#         st.write(f"Error fetching coordinates for {country_name}: {e}")
#         return None, None
######################### Coordinates ####################

# Convert Mongo data into a pandas DataFrame
def mongo_data_to_dataframe(data):
    df = pd.DataFrame(data)

    # Drop the MongoDB ID field
    if "_id" in df.columns:
        df = df.drop("_id", axis=1)

    # Convert 2,024 to 2024 year format
    df['year'] = df['year'].astype(int)

    return df

# Read country_coordinates CSV
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

######################### Coordinates ####################
        # Fetch latitude and longitude for each country and ass as new columns
        # st.write("Fetching coordinates for countries, please wait...")
        # df['latitude'], df['longitude'] = zip(*df['Country name'].apply(get_coordinates))

        # # Filter out rows if geocodeing fails
        # df = df.dropna(subset=['latitude', 'longitude'])
######################### Coordinates ####################
        # create choropleth map
        fig = px.choropleth(df,
                            locations='Country name',
                            locationmode='country names',
                            color='Life Ladder',
                            title='World Happiness Scores by Country',
                            color_continuous_scale=px.colors.sequential.Plasma)
        
        # Display map in Streamlit
        st.title('World Happiness Map')
        st.plotly_chart(fig)

        # Create Folium map with markers
        m = folium.Map(location=[20,0], zoom_start=2)

        # Add markers for each country
        for i, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['Country name']} - Happiness Score: {row['Life Ladder']}"
            ).add_to(m)
        
        # Display folium map with Streamlit
        st_folium(m, width=1000, height=600)
        

if __name__ == "__main__":
    main()
         