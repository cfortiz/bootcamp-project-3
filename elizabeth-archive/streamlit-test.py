# import libraries and dependencies
import streamlit_app as st # requirement 3: your project must include at least one JavaScript or Python library that we did not cover.
from pymongo import MongoClient # requirement 2: data must be stored in and extracted from at least one database (PostgreSQL, MongoDB, SQLite, etc).
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import plotly.express as px

# Initialize Nominatim API for geocoding
geolocator = Nominatim(user_agent="geoapiExercises")

# Create a function to get the coordinates of a country
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

    # Make Adjustments to dataframe: Drop the MongoDB ID field and convert 'year' from mongodb string to pd int so that it doesn't have the comma in the year
    if "_id" in df.columns:
        df = df.drop("_id", axis=1)

    df['year'] = df['year'].astype(int)
    df['latitude'],df['longitude']= df['Country name'].apply(get_coordinates) 


    return df

# Streamlit app
def main():
    st.title("World Happiness Report")
    st.write("This is a Python-based frontend application.")

# Add a button and a slider
    # if st.button("Say Hello"):
    #     st.write("Hello!")

    # slider_value = st.slider("Choose a number", 0, 100)
    # st.write(f"You selected {slider_value}")



    # Fetch data from MongoDB
    data = get_data_from_mongodb()

    if data:
        # Convert to DataFrame
        df = mongo_data_to_dataframe(data)

        # Display the data as a table in Streamlit
        # st.dataframe(df)
        
        # Optionally display some statistics or summary
    #     st.write("Data Summary:")
    #     st.write(df.describe())
    # else:
    #     st.write("No data found in the MongoDB collection.")


# add a map with the smiley face markers that buckets red, yellow, green
# life ladder is the metric i'm going to use
# red is >= 0 and < 4
# yellow is >= 4 and < 8
# green is >= 8

# i need coordinates of each country in order to make a map

    import plotly.express as px

    # # Sample data with country names and values (replace with your own data)
    # # add a filter dropdown for a year in the data and get one row per country to plot 
    # data = {
    #     'Country name': ['United States', 'Canada', 'Germany', 'France', 'Brazil', 'Australia', 'China', 'India'],
    #     'Happiness Score': [7.1, 7.2, 6.9, 6.7, 6.3, 7.5, 5.8, 6.1]
    # }

    # # Convert to DataFrame
    # df = pd.DataFrame(data)

    # # Create a choropleth map using Plotly Express
    # fig = px.choropleth(df, 
    #                     locations='Country name', 
    #                     locationmode='country names', 
    #                     color='Happiness Score', 
    #                     title='World Happiness Scores by Country',
    #                     color_continuous_scale=px.colors.sequential.Plasma)

    # # Display the map in Streamlit
    # st.title('World Happiness Map')
    # # st.plotly_chart(fig)
    # # Set the figure size by specifying width and height
    # # Set OpenStreetMap as the tileset for the map
    # fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=2, mapbox_center={"lat": 20, "lon": 0})
    # st.plotly_chart(fig, use_container_width=False, width=900, height=600)

    

    # Dropdown for selecting the year
    selected_year = st.selectbox('Select Year', df['year'].unique())

    # Filter data based on the selected year
    filtered_data = df[df['year'] == selected_year]

    # Create Folium map
    m = folium.Map(location=[20, 0], zoom_start=4, tiles='OpenStreetMap')

    # Add markers for the filtered data
    for i, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Country name']} - Happiness Score: {row['Happiness Score']}"
        ).add_to(m)

    # Display the map
    st_folium(m, width=1000, height=600)

if __name__ == "__main__":
    main()

