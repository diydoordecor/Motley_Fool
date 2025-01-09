import streamlit as st
import pandas as pd

# Load the data
uploaded_file = 'StockAdvisor-scorecard-2025-01-07.csv'
try:
    data = pd.read_csv(uploaded_file)
except FileNotFoundError:
    st.error("The file 'StockAdvisor-scorecard-2025-01-07.csv' was not found. Please ensure the file is in the correct directory.")
    st.stop()

# Remove the "Follow" column
if "Follow" in data.columns:
    data = data.drop(columns=["Follow"])

# Clean and convert numeric columns
def clean_numeric_column(column):
    return pd.to_numeric(column.replace('[\$,B]', '', regex=True), errors='coerce')

numeric_columns = ["Price", "Quant: 5Y", "Market Cap", "Adj. Rec. Price", "Return Since Rec"]
for col in numeric_columns:
    if col in data.columns:
        data[col] = clean_numeric_column(data[col])

# Multiply "Return Since Rec" by 100 for percentage formatting
if "Return Since Rec" in data.columns:
    data["Return Since Rec"] = data["Return Since Rec"] * 100

# Define pages
def main_dashboard():
    st.title("Stock Advisor Dashboard")
    st.markdown("### Stock Performance")

    # Add column headers
    header_cols = st.columns([1.2, 1, 1, 1, 1, 1.5, 1.2, 1.2])
    headers = ["Symbol", "Price", "Rec Date", "Team", "Quant: 5Y", "Market Cap", "Adj. Rec. Price", "Return Since Rec"]
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")

    # Display data in a grid-like structure
    for index, row in data.iterrows():
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.2, 1, 1, 1, 1, 1.5, 1.2, 1.2])

        with col1:
            st.markdown(f"**{row['Symbol']}**")
        with col2:
            st.markdown(f"${row['Price']:.2f}")
        with col3:
            st.markdown(f"{row['Rec Date']}")
        with col4:
            st.markdown(f"{row['Team']}")
        with col5:
            st.markdown(f"{row['Quant: 5Y']:.2f}")
        with col6:
            st.markdown(f"${row['Market Cap']:.2f}B")
        with col7:
            st.markdown(f"${row['Adj. Rec. Price']:.2f}")
        with col8:
            st.markdown(f"{row['Return Since Rec']:.0f}%")

        # Smaller separator
        st.markdown("<hr style='margin:5px 0'>", unsafe_allow_html=True)

    # Sidebar Filters
    st.sidebar.header("Filters")
    price_filter = st.sidebar.slider("Price Range", float(data["Price"].min()), float(data["Price"].max()), (float(data["Price"].min()), float(data["Price"].max())))
    team_filter = st.sidebar.multiselect("Select Team", options=data["Team"].unique(), default=data["Team"].unique())
    type_filter = st.sidebar.multiselect("Select Type", options=data["Type"].unique(), default=data["Type"].unique())

    # Apply filters
    filtered_data = data[(data["Price"] >= price_filter[0]) & (data["Price"] <= price_filter[1])]
    filtered_data = filtered_data[filtered_data["Team"].isin(team_filter)]
    filtered_data = filtered_data[filtered_data["Type"].isin(type_filter)]

    # Display filtered data in a grid-like structure
    st.markdown("### Filtered Results")
    header_cols = st.columns([1.2, 1, 1, 1, 1, 1.5, 1.2, 1.2])
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")

    for index, row in filtered_data.iterrows():
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.2, 1, 1, 1, 1, 1.5, 1.2, 1.2])

        with col1:
            st.markdown(f"**{row['Symbol']}**")
        with col2:
            st.markdown(f"${row['Price']:.2f}")
        with col3:
            st.markdown(f"{row['Rec Date']}")
        with col4:
            st.markdown(f"{row['Team']}")
        with col5:
            st.markdown(f"{row['Quant: 5Y']:.2f}")
        with col6:
            st.markdown(f"${row['Market Cap']:.2f}B")
        with col7:
            st.markdown(f"${row['Adj. Rec. Price']:.2f}")
        with col8:
            st.markdown(f"{row['Return Since Rec']:.0f}%")

        st.markdown("<hr style='margin:5px 0'>", unsafe_allow_html=True)

def about_page():
    st.title("About This App")
    st.markdown("""
    This app provides stock recommendations and insights.
    - View stock performance
    - Filter based on your criteria
    """)

# Sidebar Navigation
page = st.sidebar.selectbox("Navigate", ["Dashboard", "About"])

# Render the selected page
if page == "Dashboard":
    main_dashboard()
elif page == "About":
    about_page()
