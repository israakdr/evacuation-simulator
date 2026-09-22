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
    st.markdown("## 🔍 Wall Extraction (v0.2)")
    
    with st.spinner("Processing floorplan..."):
        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Step 2: Adaptive threshold (better than fixed threshold)
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )
        
        # Step 3: Morphological operations to remove noise
        kernel = np.ones((3, 3), np.uint8)
        # Remove small noise
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        # Connect broken lines
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Step 4: Edge detection
        edges = cv2.Canny(cleaned, 50, 150)
        
        # Step 5: Hough Transform with stricter parameters
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=80,          # Higher threshold = fewer lines
            minLineLength=100,     # Only long lines (walls)
            maxLineGap=20          # Allow gaps in walls
        )
        
        # Step 6: Draw only long lines
        walls_image = image_np.copy()
        wall_count = 0
        
        if lines is not None:
            for line in lines:
                coords = line.flatten()
                if len(coords) == 4:
                    x1, y1, x2, y2 = coords
                    # Calculate line length
                    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    # Only draw lines longer than 100 pixels
                    if length > 100:
                        cv2.line(walls_image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 3)
                        wall_count += 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖼️ Cleaned Binary Image")
        st.image(cleaned, caption="After noise removal", use_container_width=True, clamp=True)
    
    with col2:
        st.markdown("### 📏 Detected Walls (Long Lines Only)")
        st.image(walls_image, caption=f"Detected {wall_count} wall segments", use_container_width=True)
    
    st.markdown("---")
    st.markdown("## 📊 Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Detected Walls", wall_count)
    
    with col2:
        st.metric("Image Width", f"{image_np.shape[1]} px")
    
    with col3:
        st.metric("Image Height", f"{image_np.shape[0]} px")
    
    st.success("✅ v0.2 complete. Walls are now cleaner. Next: 3D model.")

else:
    st.info("👆 Please upload a floorplan image to begin.")
