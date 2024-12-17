import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Page Config
st.set_page_config(layout="wide", page_title="Neutral AI Dashboard")

# Title and Description
st.title("Neutral AI Project Dashboard")
st.write("A beginner-friendly dashboard for visualizing and interacting with the Neutral AI project.")

# Sidebar Navigation
st.sidebar.header("Navigation")
options = ["Overview", "Data Visualization", "Metrics and Map"]
choice = st.sidebar.radio("Select a page:", options)

# Example Data
data = {
    "State": ["California", "Texas", "Florida", "New York", "Illinois"],
    "Population": [39538223, 29145505, 21538187, 20201249, 12812508],
    "Gain/Loss": [200000, 150000, -50000, -300000, -100000]
}
df = pd.DataFrame(data)

# Function to create map
def create_map():
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    for _, row in df.iterrows():
        folium.Marker(
            location=[37 + (row['Population'] % 10)/10, -95 + (row['Population'] % 10)/10],
            popup=f"{row['State']}: {row['Population']:,}",
            icon=folium.Icon(color="blue" if row['Gain/Loss'] > 0 else "red")
        ).add_to(m)
    return m

# Logic for Navigation Pages
if choice == "Overview":
    st.subheader("Project Overview")
    st.write("Neutral AI is designed to explore balanced predictions and fairness in data-driven insights.")

elif choice == "Data Visualization":
    st.subheader("Data Visualization")
    st.write("### Population Gain/Loss by State")
    fig = px.bar(df, x="State", y="Gain/Loss", color="Gain/Loss", title="State Gain/Loss Overview")
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Detailed Table")
    st.dataframe(df)

elif choice == "Metrics and Map":
    st.subheader("Key Metrics and Map")

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Population", f"{df['Population'].sum():,}")
    col2.metric("Total Gain", f"{df[df['Gain/Loss'] > 0]['Gain/Loss'].sum():,}")
    col3.metric("Total Loss", f"{df[df['Gain/Loss'] < 0]['Gain/Loss'].sum():,}")

    # Map Visualization
    st.write("### Population Map")
    folium_static(create_map())

# Footer
st.write("---")
st.write("Built with ❤️ using Streamlit and Plotly.")
