import streamlit as st
from PIL import Image

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="Evacuation Simulator",
    page_icon="🏢",
    layout="wide"
)

# ============================================
# Header
# ============================================
st.title("🏢 Evacuation Simulator")
st.markdown("### Upload a floorplan to start")

# ============================================
# File Uploader
# ============================================
uploaded_file = st.file_uploader(
    "Choose a floorplan image (PNG, JPG)",
    type=["png", "jpg", "jpeg"]
)

# ============================================
# Display Uploaded Image
# ============================================
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.markdown("---")
    st.markdown("## 📐 Uploaded Floorplan")
    st.image(image, caption="Uploaded Floorplan", use_container_width=True)
    
    # Image Info
    st.markdown("### 📊 Image Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Width", f"{image.size[0]} px")
    
    with col2:
        st.metric("Height", f"{image.size[1]} px")
    
    with col3:
        st.metric("Format", image.format)
    
    st.success("✅ Floorplan uploaded successfully. Next step: wall extraction.")
else:
    st.info("👆 Please upload a floorplan image to begin.")
