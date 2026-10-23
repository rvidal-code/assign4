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

    # Replace with your GitHub raw URL, for example:
    # https://raw.githubusercontent.com/<your-username>/<your-repo>/main/beverages.csv
    BEVERAGE_URL = "PASTE_YOUR_RAW_GITHUB_URL_HERE"

    @st.cache_data(ttl=3600)
    def load_beverage_data(url):
        try:
            # First choice: fetch the data online
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return pd.read_csv(StringIO(response.text)), "online"
        except Exception:
            # Fallback: read the CSV stored in the repository
            return pd.read_csv("beverages.csv"), "local file"

    try:
        bev_df, source = load_beverage_data(BEVERAGE_URL)
        bev_df = bev_df.sort_values("Gallons per capita", ascending=False)

        st.write(f"Most consumed beverage: **{bev_df.iloc[0]['Beverage']}**")
        st.bar_chart(bev_df.set_index("Beverage")["Gallons per capita"])
        st.dataframe(bev_df, use_container_width=True)
        st.caption(f"Data loaded from: {source}. Source: Beverage Marketing Corporation (2010 per capita figures).")
    except Exception as e:
        st.error(f"Could not load beverage data: {e}")
