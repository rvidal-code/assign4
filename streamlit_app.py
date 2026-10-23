# Import necessary packages (Make sure to also include in "requirements.txt" in this repository.)
import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Print Title for the App
st.title("Microsoft Stock Data Dashboard by Raimundo Vidal")

# Read CSV file with stock data (CSV file must be in 'main' folder for your assignment 4 repository) 
df = pd.read_csv("msft.csv")

# Set up the 4 tabs on the Dashboard
tabs = st.tabs(["📋 Raw Data", "📈 Price Chart", "📊 Volume Chart", "🥤 Top US Beverages"])

# Tab 1: Raw Data
with tabs[0]:
    st.subheader(f"Raw Data for MSFT")
    st.dataframe(df, use_container_width=True)

# Tab 2: Closing Price Chart
with tabs[1]:
    st.subheader(f"Closing Price for MSFT")
    st.line_chart(df['Close'])

# Tab 3: Volume Chart
with tabs[2]:
    st.subheader(f"Volume for MSFT")
    st.bar_chart(df['Volume'])

# Tab 4: Most Consumed Beverages in the US (fetched online)
with tabs[3]:
    st.subheader("Most Consumed Beverages in the US")

    # Put the link to a public CSV here. It needs two columns:
    # "Beverage" and "Gallons per capita"
    BEVERAGE_URL = "PASTE_YOUR_CSV_URL_HERE"

    @st.cache_data(ttl=3600)
    def load_beverage_data(url):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text))

    try:
        bev_df = load_beverage_data(BEVERAGE_URL)
        bev_df = bev_df.sort_values("Gallons per capita", ascending=False)
        st.dataframe(bev_df, use_container_width=True)
        st.bar_chart(bev_df.set_index("Beverage")["Gallons per capita"])
        st.write(f"Most consumed beverage: **{bev_df.iloc[0]['Beverage']}**")
    except Exception as e:
        st.error(f"Could not load beverage data: {e}")
