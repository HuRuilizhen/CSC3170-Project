import streamlit as st
import base64

def set_bg(bg_image):
    """
    This function sets a background image for a Streamlit app.

    Args:
    bg_image (str): The path or URL to the image file to use as the background.
    """
    # Check if the image file is a local file and not a URL
    if not bg_image.startswith("http://") and not bg_image.startswith("https://"):
        # Encode the local file to be suitable for URL embedding
        with open(bg_image, "rb") as file:
            bg_image = base64.b64encode(file.read()).decode("utf-8")
            bg_image = f"data:image/jpeg;base64,{bg_image}"

    # Inject CSS to use the background image
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({bg_image});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
def set_page_config(layout="wide"):
    st.set_page_config(layout=layout)
