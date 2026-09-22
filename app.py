import streamlit as st
import cv2
import numpy as np
from PIL import Image
import json

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
    st.markdown("## 🔍 Wall Extraction (v0.6 - Merged)")
    
    with st.spinner("Processing floorplan..."):
        # ============================================
        # 1. Preprocessing
        # ============================================
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )
        
        kernel_small = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_small, iterations=1)
        
        kernel_erode = np.ones((2, 2), np.uint8)
        eroded = cv2.erode(cleaned, kernel_erode, iterations=1)
        
        kernel_dilate = np.ones((3, 3), np.uint8)
        walls_clean = cv2.dilate(eroded, kernel_dilate, iterations=2)
        
        kernel_close = np.ones((5, 5), np.uint8)
        walls_clean = cv2.morphologyEx(walls_clean, cv2.MORPH_CLOSE, kernel_close, iterations=1)
        
        # ============================================
        # 2. Edge Detection
        # ============================================
        edges = cv2.Canny(walls_clean, 50, 150)
        
        # ============================================
        # 3. Hough Transform
        # ============================================
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=30,
            maxLineGap=15
        )
        
        # ============================================
        # 4. Merge Similar Lines (v0.6)
        # ============================================
        def are_similar(line1, line2, angle_tol=10, dist_tol=20):
            """Check if two lines are similar (same direction and close)."""
            x1, y1, x2, y2 = line1
            x3, y3, x4, y4 = line2
            
            # Calculate angles
            angle1 = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            angle2 = np.degrees(np.arctan2(y4 - y3, x4 - x3))
            
            # Angle difference
            angle_diff = abs(angle1 - angle2)
            if angle_diff > 90:
                angle_diff = 180 - angle_diff
            
            # Distance between midpoints
            mid1 = ((x1 + x2) / 2, (y1 + y2) / 2)
            mid2 = ((x3 + x4) / 2, (y3 + y4) / 2)
            dist = np.sqrt((mid1[0] - mid2[0])**2 + (mid1[1] - mid2[1])**2)
            
            return angle_diff < angle_tol and dist < dist_tol
        
        # Merge lines
        merged_lines = []
        used = set()
        
        if lines is not None:
            for i, line1 in enumerate(lines):
                if i in used:
                    continue
                coords1 = line1.flatten()
                if len(coords1) != 4:
                    continue
                
                # Find similar lines
                group = [coords1]
                for j, line2 in enumerate(lines):
                    if j <= i or j in used:
                        continue
                    coords2 = line2.flatten()
                    if len(coords2) != 4:
                        continue
                    if are_similar(coords1, coords2):
                        group.append(coords2)
                        used.add(j)
                
                # Merge group into one line (average)
                if len(group) > 1:
                    all_x1 = [g[0] for g in group]
                    all_y1 = [g[1] for g in group]
                    all_x2 = [g[2] for g in group]
                    all_y2 = [g[3] for g in group]
                    merged = [int(np.mean(all_x1)), int(np.mean(all_y1)),
                              int(np.mean(all_x2)), int(np.mean(all_y2))]
                else:
                    merged = coords1
                
                merged_lines.append(merged)
                used.add(i)
        
        # ============================================
        # 5. Convert to JSON
        # ============================================
        walls_data = []
        walls_image = image_np.copy()
        external_count = 0
        internal_count = 0
        
        for i, coords in enumerate(merged_lines):
            x1, y1, x2, y2 = coords
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            # Classify (improved)
            if length > 150:
                wall_type = "external"
                color = (255, 0, 0)
                thickness = 3
                external_count += 1
            else:
                wall_type = "internal"
                color = (0, 255, 0)
                thickness = 2
                internal_count += 1
            
            cv2.line(walls_image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
            
            walls_data.append({
                "id": i,
                "type": wall_type,
                "start": {"x": int(x1), "y": int(y1)},
                "end": {"x": int(x2), "y": int(y2)},
                "length": round(float(length), 2)
            })
        
        # ============================================
        # 6. Build JSON
        # ============================================
        building_data = {
            "building_name": uploaded_file.name,
            "image_size": {
                "width": int(image_np.shape[1]),
                "height": int(image_np.shape[0])
            },
            "total_walls": len(walls_data),
            "external_walls": external_count,
            "internal_walls": internal_count,
            "walls": walls_data
        }
    
    # ============================================
    # Display Results
    # ============================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖼️ Cleaned Walls")
        st.image(walls_clean, caption="After noise removal", use_container_width=True, clamp=True)
    
    with col2:
        st.markdown("### 📏 Detected Walls (Merged)")
        st.image(walls_image, caption=f"Detected {len(walls_data)} walls", use_container_width=True)
    
    # Statistics
    st.markdown("---")
    st.markdown("## 📊 Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Walls", len(walls_data))
    
    with col2:
        st.metric("External Walls", external_count)
    
    with col3:
        st.metric("Internal Walls", internal_count)
    
    # JSON Export
    st.markdown("---")
    st.markdown("## 📄 JSON Data")
    
    with st.expander("View JSON Data"):
        st.json(building_data)
    
    json_string = json.dumps(building_data, indent=2, ensure_ascii=False)
    st.download_button(
        label="📥 Download JSON",
        file_name=f"{uploaded_file.name.split('.')[0]}_walls.json",
        mime="application/json",
        data=json_string
    )
    
    st.success("✅ v0.6 complete. Walls merged. Next: 3D model.")

else:
    st.info("👆 Please upload a floorplan image to begin.")
