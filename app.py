import streamlit as st # frontend framework for creating titles, buttons, dropdowns, images and ui
import pandas as pd # reading csv and so that it becomes a dataframe or a table, i.e excel inside python
from pathlib import Path # working with file paths in a platform-independent way (Windows, macOS, Linux)

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
aesthetic_descriptions = {
    "y2k": "Bold, playful and nostalgic fashion inspired by the early 2000s, featuring bright colors, statement pieces and fun patterns.",

    "old_money": "Classic, elegant and timeless fashion with tailored silhouettes, neutral colors and a sophisticated appearance.",

    "streetwear": "Urban and edgy fashion focused on comfort, oversized fits, graphic pieces and modern youth culture.",

    "soft_girl": "Feminine and delicate fashion featuring pastel colors, cute details, soft fabrics and a gentle aesthetic.",

    "minimalist": "Clean and refined fashion built around simple silhouettes, neutral colors and timeless wardrobe essentials.",

    "zara_larrson": "Confident, trendy and performance-inspired fashion featuring bold colors, statement pieces and pop-star energy.",

    "indian_traditional": "Rich cultural fashion featuring traditional silhouettes, intricate embroidery, vibrant colors and heritage-inspired designs.",

    "indowestern": "A fusion of Indian and Western fashion that combines traditional elements with contemporary styling.",

    "whimsical": "Creative, expressive and playful fashion featuring unique details, vibrant colors and imaginative styling."
}

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
        st.subheader("👤 Your Style Profile")
        st.markdown(f"🎨 **Preferred Aesthetic:** {selected_aesthetic}")
        st.markdown(f"💰 **Budget Tier:** {selected_price}")

        st.subheader(f'About {selected_aesthetic} Aesthetic:')
        st.write(aesthetic_descriptions[selected_aesthetic])

        # ---------------------------------------------------
        # SHOW RECOMMENDATIONS
        # ---------------------------------------------------
        if len(filtered_df) > 1:
            st.subheader(f'Found {len(filtered_df)} Recommended Products')
        else:
            st.subheader(f'Found {len(filtered_df)} Recommended Product')
        if len(filtered_df) > 0:

            for _, row in filtered_df.iterrows():

                col1, col2 = st.columns([1, 2])

                # ---------------------------------------------------
                # IMAGE COLUMN
                # ---------------------------------------------------

                with col1:

                    image_path = Path(row["image_path"])
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


