import streamlit as st
import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Fashion Recommendation System",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("👗 Fashion Recommendation System")
st.caption("AI-powered stylist assistant")

# ---------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------

csv_path = Path("data/products.csv")

if csv_path.exists():

    try:
        df = pd.read_csv(csv_path)

        st.success("Dataset loaded successfully ✅")

        # ---------------------------------------------------
        # SHOW DATASET
        # ---------------------------------------------------

        st.subheader("📂 Product Dataset")
        st.dataframe(df)

        # ---------------------------------------------------
        # SIDEBAR FILTERS
        # ---------------------------------------------------

        st.sidebar.header("🎀 Filters")

        aesthetic_options = df["aesthetic"].unique()

        selected_aesthetic = st.sidebar.selectbox(
            "Choose Aesthetic",
            aesthetic_options
        )

        price_options = df["price_tier"].unique()

        selected_price = st.sidebar.selectbox(
            "Choose Price Tier",
            price_options
        )

        # ---------------------------------------------------
        # FILTER PRODUCTS
        # ---------------------------------------------------

        filtered_df = df[
            (df["aesthetic"] == selected_aesthetic) &
            (df["price_tier"] == selected_price)
        ]

        # ---------------------------------------------------
        # SHOW RECOMMENDATIONS
        # ---------------------------------------------------

        st.subheader("✨ Recommended Products")

        if len(filtered_df) > 0:

            for _, row in filtered_df.iterrows():

                col1, col2 = st.columns([1, 2])

                # ---------------------------------------------------
                # IMAGE COLUMN
                # ---------------------------------------------------

                with col1:

                    image_path = Path(row["image_path"])

                    st.write("Path:", image_path)
                    st.write("Exists:", image_path.exists())

                    if image_path.exists():
                        st.image(str(image_path), width=250)
                    else:
                        st.error(f"Image not found: {image_path}")

                # ---------------------------------------------------
                # PRODUCT DETAILS
                # ---------------------------------------------------

                with col2:

                    st.markdown(f"### {row['title']}")

                    st.write(f"📌 Category: {row['category']}")
                    st.write(f"🎨 Aesthetic: {row['aesthetic']}")
                    st.write(f"💸 Price: ₹{row['price']}")
                    st.write(f"🏷️ Price Tier: {row['price_tier']}")
                    st.write(f"✨ Tags: {row['tags']}")

                    st.markdown(
                        f"[🛍 Shop Here]({row['link']})"
                    )

                st.divider()

        else:
            st.warning("No matching products found.")

    except Exception as e:
        st.error(f"Error reading CSV: {e}")

else:
    st.error("products.csv not found inside data folder.")