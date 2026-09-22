import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
from PIL import Image
import json
import os

st.set_page_config(
    page_title="Evacuation Simulator",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Evacuation Simulator")
st.markdown("### Upload a floorplan to start")

uploaded_file = st.file_uploader(
    "Choose a floorplan image (PNG, JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    
    st.markdown("---")
    st.markdown("## 📐 Original Floorplan")
    st.image(image, caption="Uploaded Floorplan", use_container_width=True)
    
    # ============================================
    # Three.js 3D Viewer
    # ============================================
    st.markdown("---")
    st.markdown("## 🌐 3D View (Three.js)")
    
    # Read the HTML file
    html_file = "assets/floorplan_viewer.html"
    
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Display in Streamlit
        components.html(html_content, height=700, scrolling=False)
    else:
        st.error(f"File not found: {html_file}")
    
    st.success("✅ v0.9 complete. Three.js viewer is ready.")

else:
    st.info("👆 Please upload a floorplan image to begin.")
