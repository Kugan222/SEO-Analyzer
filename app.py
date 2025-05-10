import streamlit as st
import sys
import os

# Allow import from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import SEO logic
from core_scraper import seo_analysis, output_data_path

# Page config
st.set_page_config(page_title="SEO Brand Analyzer", layout="centered")
st.title("🔍 Amazon SEO & Brand Analyzer")

# Custom dark-mode-friendly CSS
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 2rem;
    }

    input, textarea {
        background-color: #1e1e1e;
        color: white;
        border-radius: 0.4rem;
        padding: 0.5rem;
    }

    button, .stButton button {
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        border-radius: 0.5rem;
        background-color: #0e1117;
        color: white;
        border: 1px solid #444;
    }

    img {
        max-width: 100%;
        height: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Input field
url = st.text_input("Enter Amazon Search URL:", "https://www.amazon.in/s?k=smartphones")

# On click
if st.button("Run SEO Analysis"):
    with st.spinner("Analyzing website..."):
        try:
            seo_analysis(url, st=st)  # Pass Streamlit for UI messages

            st.success("Analysis complete!")

            # Display result charts
            st.subheader("Analysis Charts")
            for title, path in {
                "Brand Distribution": output_data_path["brand_chart"],
                "Keyword Frequency": output_data_path["keyword_chart"],
                "Top Product Prices": output_data_path["price_chart"]
            }.items():
                if os.path.exists(path):
                    st.markdown(f"**{title}**")
                    st.image(path, use_column_width=True)
                else:
                    st.warning(f"⚠️ {title} not available.")

            # Download buttons
            st.subheader("📥 Download Reports")
            for label, path in {
                "Excel Report": output_data_path["excel"],
                "JSON Report": output_data_path["json"]
            }.items():
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        st.download_button(label=f"Download {label}", data=f, file_name=os.path.basename(path))
                else:
                    st.warning(f"{label} not available.")

        except Exception as e:
            st.error(f"Error: {e}")
