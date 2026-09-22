import streamlit as st
import cv2
import numpy as np
from PIL import Image

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
    
    st.markdown("---")
    st.markdown("## 🔍 Wall Extraction")
    
    with st.spinner("Processing floorplan..."):
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        edges = cv2.Canny(gray, 50, 150)
        
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=30,
            maxLineGap=10
        )
        
        walls_image = image_np.copy()
        wall_count = 0
        
        if lines is not None:
            for line in lines:
                if line is not None and len(line) > 0:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(walls_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    wall_count += 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖼️ Thresholded Image")
        st.image(thresh, caption="Black lines = potential walls", use_container_width=True, clamp=True)
    
    with col2:
        st.markdown("### 📏 Detected Walls")
        st.image(walls_image, caption=f"Detected {wall_count} wall segments", use_container_width=True)
    
    st.markdown("---")
    st.markdown("## 📊 Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Detected Lines", wall_count)
    
    with col2:
        st.metric("Image Width", f"{image_np.shape[1]} px")
    
    with col3:
        st.metric("Image Height", f"{image_np.shape[0]} px")
    
    st.success("✅ Wall extraction complete. Next step: convert to 3D model.")

else:
    st.info("👆 Please upload a floorplan image to begin.")
