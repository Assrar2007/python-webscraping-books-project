import io

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Import the scraper function from your existing file
from flipkart_scraper import scrape_books

# ---------------------------
# STREAMLIT PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Books Web Scraping & Analysis",
    layout="wide",
)

st.title("📚 Books Web Scraping & Data Analysis App")
st.write(
    "This app scrapes book data from **BooksToScrape** and shows "
    "summary statistics, interactive filters, charts, and download options."
)

# ---------------------------
# SIDEBAR SETTINGS
# ---------------------------
st.sidebar.header("Scraping Settings")

num_pages = st.sidebar.slider(
    "Number of pages to scrape",
    min_value=1,
    max_value=10,
    value=5,
    step=1,
    help="Each page has ~20 books.",
)

st.sidebar.markdown("---")
st.sidebar.info("Click **Run Scraper** to start scraping.")

# ---------------------------
# MAIN ACTION BUTTON
# ---------------------------
if st.button("🚀 Run Scraper"):
    with st.spinner("Scraping books... please wait..."):
        df = scrape_books(num_pages=num_pages)

    st.success(
        f"Scraping completed! Collected **{len(df)} books** "
        f"from **{num_pages} pages**."
    )

    # -----------------------
    # KEY METRICS (KPIs)
    # -----------------------
    st.subheader("📊 Key Metrics")

    colA, colB, colC, colD = st.columns(4)

    colA.metric("Total Books", len(df))
    colB.metric("Min Price (£)", f"{df['price_clean'].min():.2f}")
    colC.metric("Max Price (£)", f"{df['price_clean'].max():.2f}")
    colD.metric("Avg Price (£)", f"{df['price_clean'].mean():.2f}")

    # -----------------------
    # TABS
    # -----------------------
    tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "📘 Data Table", "ℹ About"])

    # =======================
    # TAB 1: DASHBOARD
    # =======================
    with tab1:
        st.subheader("💡 Price Summary")
        st.write(df["price_clean"].describe())

        # Charts
        col1, col2 = st.columns(2)

        # Price distribution
        with col1:
            st.markdown("**Price Distribution**")
            fig1, ax1 = plt.subplots()
            ax1.hist(df["price_clean"], bins=10)
            ax1.set_xlabel("Price (£)")
            ax1.set_ylabel("Number of Books")
            ax1.set_title("Distribution of Book Prices")
            st.pyplot(fig1)

        # Rating counts
        with col2:
            st.markdown("**Books by Rating**")
            rating_counts = df["rating"].value_counts()
            st.bar_chart(rating_counts)

        # Availability chart
        st.markdown("**Availability of Books**")
        avail_counts = df["availability"].value_counts()
        st.bar_chart(avail_counts)

        # -------------------
        # DOWNLOAD FULL DATA
        # -------------------
        st.subheader("⬇️ Download Full Dataset")

        # CSV download
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Full Data (CSV)",
            data=csv_bytes,
            file_name="books_data.csv",
            mime="text/csv",
        )

        # Excel download
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="data")
        excel_bytes = output.getvalue()

        st.download_button(
            label="Download Full Data (Excel)",
            data=excel_bytes,
            file_name="books_data.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
        )

    # =======================
    # TAB 2: DATA TABLE + FILTERS
    # =======================
    with tab2:
        st.subheader("📘 Full Dataset")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.subheader("🔍 Filter Books")

        # -------- Filters --------
        # Title search
        search_keyword = st.text_input(
            "Search by title keyword:", key="search_keyword"
        )

        # Rating filter
        rating_filter = st.multiselect(
            "Filter by Rating:",
            options=sorted(df["rating"].dropna().unique()),
            key="rating_filter",
        )

        # Price range filter
        min_price = float(df["price_clean"].min())
        max_price = float(df["price_clean"].max())
        price_range = st.slider(
            "Select Price Range (£):",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            key="price_range",
        )

        # Apply filters
        filtered_df = df.copy()

        if search_keyword:
            filtered_df = filtered_df[
                filtered_df["title"].str.contains(search_keyword, case=False)
            ]

        if rating_filter:
            filtered_df = filtered_df[filtered_df["rating"].isin(rating_filter)]

        filtered_df = filtered_df[
            (filtered_df["price_clean"] >= price_range[0])
            & (filtered_df["price_clean"] <= price_range[1])
        ]

        # -------- Sorting --------
        st.subheader("⬇️ Sort Books")

        sort_option = st.selectbox(
            "Sort by:",
            [
                "None",
                "Price: Low to High",
                "Price: High to Low",
                "Title (A–Z)",
                "Title (Z–A)",
            ],
            key="sort_option",
        )

        if sort_option == "Price: Low to High":
            filtered_df = filtered_df.sort_values(
                "price_clean", ascending=True
            )
        elif sort_option == "Price: High to Low":
            filtered_df = filtered_df.sort_values(
                "price_clean", ascending=False
            )
        elif sort_option == "Title (A–Z)":
            filtered_df = filtered_df.sort_values("title", ascending=True)
        elif sort_option == "Title (Z–A)":
            filtered_df = filtered_df.sort_values("title", ascending=False)

        st.write(f"Showing {len(filtered_df)} filtered books:")
        st.dataframe(filtered_df, use_container_width=True)

        # -------- Download filtered --------
        st.subheader("⬇️ Download Filtered Results")

        csv_bytes_filt = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Filtered Data (CSV)",
            data=csv_bytes_filt,
            file_name="filtered_books.csv",
            mime="text/csv",
        )

    # =======================
    # TAB 3: ABOUT
    # =======================
    with tab3:
        st.subheader("ℹ About This App")
        st.write(
            """
This web application demonstrates an end-to-end **Web Scraping & Data Analysis**
project using Python.

**Features:**
- Scrapes book data (title, price, availability, rating) from BooksToScrape.
- Cleans and stores data using **pandas**.
- Generates descriptive statistics and visualisations with **matplotlib**.
- Provides interactive **filters**, **sorting**, and **downloads** (CSV & Excel).
- Built with **Streamlit** for a simple, modern web UI.

**Tech Stack:**
- Python
- Requests, BeautifulSoup
- Pandas, Matplotlib
- Streamlit
"""
        )

else:
    st.info("Click **Run Scraper** above to start the process.")
