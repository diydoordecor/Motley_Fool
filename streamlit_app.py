import streamlit as st
import pandas as pd

# Load the data
uploaded_file = '/mnt/data/StockAdvisor-scorecard-2025-01-07.csv'
data = pd.read_csv(uploaded_file)

# Format Streamlit App
st.title("Stock Advisor Dashboard")

# Displaying the table with a similar format as the screenshot
st.markdown("### Stock Performance")

# Style and display the dataframe
def style_dataframe(df):
    df = df.style.format({
        "Price": "$ {:.2f}",
        "Market Cap": "${:.2fB}",
        "Adj. Rec. Price": "$ {:.2f}",
        "Return Since Rec": "{:.0%}",
        "Return vs. S&P 500": "{:.0%}"
    })
    return df

styled_data = style_dataframe(data)
st.dataframe(data, use_container_width=True)

# Adding filter options
st.sidebar.header("Filters")
price_filter = st.sidebar.slider("Price Range", float(data["Price"].min()), float(data["Price"].max()), (float(data["Price"].min()), float(data["Price"].max())))
team_filter = st.sidebar.multiselect("Select Team", options=data["Team"].unique(), default=data["Team"].unique())
type_filter = st.sidebar.multiselect("Select Type", options=data["Type"].unique(), default=data["Type"].unique())

# Apply filters
filtered_data = data[(data["Price"] >= price_filter[0]) & (data["Price"] <= price_filter[1])]
filtered_data = filtered_data[filtered_data["Team"].isin(team_filter)]
filtered_data = filtered_data[filtered_data["Type"].isin(type_filter)]

# Display filtered data
st.markdown("### Filtered Results")
st.dataframe(filtered_data, use_container_width=True)
