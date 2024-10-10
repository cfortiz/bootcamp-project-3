import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px

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

# Convert Mongo data into a pandas DataFrame
def mongo_data_to_dataframe(data):
    df = pd.DataFrame(data)

    # Drop the MongoDB ID field
    if "_id" in df.columns:
        df = df.drop("_id", axis=1)

    # Convert 2,024 to 2024 year format
    df['year'] = df['year'].astype(int)

    return df

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

        # Display the data as a table in Streamlit
        st.dataframe(df)

if __name__ == "__main__":
    main()
         