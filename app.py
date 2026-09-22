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
    st.markdown("## 🔍 Wall Extraction (v0.4 - Cleaned)")
    
    with st.spinner("Processing floorplan..."):
        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Step 2: Adaptive threshold
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )
        
        # Step 3: Remove small dots (noise)
        kernel_small = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_small, iterations=1)
        
        # Step 4: Remove text and small objects (keep only thick lines)
        # Erosion removes thin lines (text, furniture)
        kernel_erode = np.ones((2, 2), np.uint8)
        eroded = cv2.erode(cleaned, kernel_erode, iterations=1)
        
        # Dilation restores the thick lines
        kernel_dilate = np.ones((3, 3), np.uint8)
        walls_clean = cv2.dilate(eroded, kernel_dilate, iterations=2)
        
        # Step 5: Connect broken lines
        kernel_close = np.ones((5, 5), np.uint8)
        walls_clean = cv2.morphologyEx(walls_clean, cv2.MORPH_CLOSE, kernel_close, iterations=1)
        
        # Step 6: Edge detection
        edges = cv2.Canny(walls_clean, 50, 150)
        
        # Step 7: Detect lines (Hough Transform)
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=30,
            maxLineGap=15
        )
        
        # Step 8: Draw lines
        walls_image = image_np.copy()
        wall_count = 0
        
        if lines is not None:
            for line in lines:
                coords = line.flatten()
                if len(coords) == 4:
                    x1, y1, x2, y2 = coords
                    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    # Color based on length
                    if length > 100:
                        color = (255, 0, 0)  # Blue = external
                        thickness = 3
                    else:
                        color = (0, 255, 0)  # Green = internal
                        thickness = 2
                    cv2.line(walls_image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
                    wall_count += 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖼️ Cleaned Walls (Binary)")
        st.image(walls_clean, caption="After noise removal", use_container_width=True, clamp=True)
    
    with col2:
        st.markdown("### 📏 Detected Walls")
        st.image(walls_image, caption=f"Detected {wall_count} wall segments", use_container_width=True)
    
    st.markdown("---")
    st.markdown("## 📊 Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Walls", wall_count)
    
    with col2:
        st.metric("Image Width", f"{image_np.shape[1]} px")
    
    with col3:
        st.metric("Image Height", f"{image_np.shape[0]} px")
    
    st.success("✅ v0.4 complete. Walls are cleaner. Next: 3D model.")

else:
    st.info("👆 Please upload a floorplan image to begin.")
