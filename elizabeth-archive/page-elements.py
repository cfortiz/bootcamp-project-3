import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import plotly.graph_objects as go

def main():

    st.title("Insert Title Here")
    st.header("Insert Header Here")
    st.subheader("Insert Subheader Here")
    st.markdown("Insert Markdown Here")

    tab1, tab2 = st.tabs(["World Map", "Compare Countries"])


if __name__ == "__main__":
    main()