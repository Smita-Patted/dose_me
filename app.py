import streamlit as st
import pandas as pd
import os

# Set page config
st.set_page_config(
    page_title="DoseMe Product Catalog",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for background and smaller back buttons
st.markdown("""
    <style>
    body, .stApp {
        background-color: #f6f8fa !important;
    }
    .stButton>button {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 4px 24px 0 rgba(34, 41, 47, 0.08);
        padding: 2rem 1.5rem;
        margin-bottom: 2rem;
        transition: box-shadow 0.3s, transform 0.3s;
        cursor: pointer;
        border: 1.5px solid #f0f0f0;
        min-height: 20px;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 500;
        color: #22292f;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        overflow: hidden;
    }
    .stButton>button::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 4%;
        background: #2196F3;
        border-radius: 18px 0 0 18px;
    }
    .stButton>button:hover {
        box-shadow: 0 8px 32px 0 rgba(34, 41, 47, 0.16);
        border: 1.5px solid #4CAF50;
        transform: translateY(-4px) scale(1.03);
    }
    .product-card {
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 2px 12px 0 rgba(34, 41, 47, 0.08);
        padding: 1.5rem 1rem;
        margin-bottom: 2rem;
        min-height: 370px;
        text-align: center;
        border: 1px solid #f0f0f0;
        transition: box-shadow 0.3s, transform 0.3s;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .product-card:hover {
        box-shadow: 0 6px 24px 0 rgba(34, 41, 47, 0.13);
        border: 1.5px solid #4CAF50;
        transform: translateY(-2px) scale(1.01);
    }
    .product-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #22292f;
        margin: 0.7rem 0 0.5rem 0;
    }
    .product-detail {
        color: #444;
        font-size: 0.98rem;
        margin-bottom: 0.2rem;
    }
    .product-img-row {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 0.5rem;
    }
    .product-img {
        border-radius: 10px;
        background: #f8f8f8;
        object-fit: cover;
        width: 160px;
        height: 160px;
        box-shadow: 0 1px 6px 0 rgba(34, 41, 47, 0.07);
        border: 1px solid #eee;
    }
    .product-block {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 1px 6px 0 rgba(34, 41, 47, 0.07);
        border: 1px solid #eee;
        margin-bottom: 2.5rem;
        padding: 1.5rem 1rem;
        text-align: center;
    }
    .back-btn-small > button {
        font-size: 0.85rem !important;
        padding: 0.15rem 0.7rem !important;
        border-radius: 6px !important;
        background: #f5f7fa !important;
        color: #222 !important;
        border: 1px solid #d1d5db !important;
        box-shadow: none !important;
        margin-bottom: 1.2rem !important;
        min-height: 32px !important;
        min-width: 120px !important;
        width: fit-content !important;
        height: 32px !important;
        font-weight: 500 !important;
        display: inline-block !important;
    }
    .back-btn-small > button:hover {
        background: #e2e6ea !important;
        color: #111 !important;
        border: 1.5px solid #4CAF50 !important;
    }
    .back-btn-small > button::before {
        display: none !important;
    }

    /* Force small styling for image toggle button container */
    .stButton[data-testid^="stButton-toggle_"] {
        margin: 0.5rem auto !important; /* Center and add vertical margin */
        padding: 0 !important;
        width: fit-content !important; /* Shrink container to fit content */
    }

    /* Force small styling for image toggle button itself */
    .stButton>button[data-testid^="stButton-toggle_"] {
        font-size: 0.75rem !important;
        padding: 0.1rem 0.5rem !important;
        min-height: 20px !important;
        height: auto !important; /* Allow height to adjust based on content */
        width: fit-content !important; /* Prevent full width */
        border-radius: 4px !important; /* Smaller border radius */
        background: #e9ecef !important; /* Light gray background */
        color: #495057 !important; /* Dark gray text */
        border: 1px solid #ced4da !important; /* Light border */
        box-shadow: none !important;
        text-align: center; /* Center text */
        display: inline-block !important; /* Ensure it's treated as a block for centering */
    }
    .stButton>button[data-testid^="stButton-toggle_"]:hover {
        background: #dee2e6 !important; /* Slightly darker hover */
        border-color: #adb5bd !important; /* Darker border hover */
        color: #212529 !important; /* Darker text hover */
    }

    </style>
""", unsafe_allow_html=True)

# Function to read Excel file
@st.cache_data
def load_excel_sheets():
    excel_file = "DoseMe_Product_Catalog_with_SKUs_and_Prices_DM.xlsx"
    xl = pd.ExcelFile(excel_file)
    return {sheet_name: pd.read_excel(excel_file, sheet_name=sheet_name) 
            for sheet_name in xl.sheet_names}

def get_product_image(product_name, suffix, folder="medicine_photos"):
    # Try to find the image with the given suffix (front/rear)
    for ext in [".jpg", ".jpeg", ".png"]:
        filename = f"{product_name} {suffix}{ext}"
        path = os.path.join(folder, filename)
        if os.path.exists(path):
            return path
    return None

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'selected_sheet' not in st.session_state:
    st.session_state.selected_sheet = None
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

# Load all sheets
sheets_data = load_excel_sheets()

# Home: Location cards
if st.session_state.current_page == 'home':
    # Header section
    st.markdown('<h1 style="text-align:center; margin-bottom:0.5rem;">&nbsp;&nbsp;Find Us Here 📌</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#666; margin-bottom:2.5rem;">Select a preferred location to view the data</p>', unsafe_allow_html=True)
    
    # Get unique locations from Sheet1
    df = sheets_data['Sheet1']
    locations = df['Location'].dropna().unique()
    
    # Create columns for the grid layout with proper spacing
    cols = st.columns(2)
    
    # Display location cards
    for idx, location in enumerate(locations):
        with cols[idx % 2]:
            row_count = len(df[df['Location'] == location])
            card_label = f"{location}"
            if st.button(card_label, key=location, use_container_width=True):
                st.session_state.selected_sheet = 'Sheet1'
                st.session_state.selected_location = location
                st.session_state.current_page = 'sheet'
                st.rerun()

# Sheet: Category cards
elif st.session_state.current_page == 'sheet':
    sheet_name = st.session_state.selected_sheet
    location = st.session_state.selected_location
    df = sheets_data[sheet_name]
    # Filter by selected location
    filtered_df = df[df['Location'] == location]
    st.markdown(f'<h2 style="text-align:center;">{location}</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#666; margin-bottom:2.5rem;">Select a category</p>', unsafe_allow_html=True)
    st.markdown('<div class="back-btn-small">', unsafe_allow_html=True)
    if st.button("← Back To Home", key="back_home"):
        st.session_state.current_page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    categories = filtered_df['Category'].dropna().unique()
    cols = st.columns(3)
    for idx, category in enumerate(categories):
        with cols[idx % 3]:
            count = (filtered_df['Category'] == category).sum()
            card_label = f"{category}"
            if st.button(card_label, key=f"cat_{category}", use_container_width=True):
                st.session_state.selected_category = category
                st.session_state.current_page = 'category'
                st.rerun()

# Category: Show all products as simple info blocks (carousel for images if >1)
elif st.session_state.current_page == 'category':
    sheet_name = st.session_state.selected_sheet
    location = st.session_state.selected_location
    category = st.session_state.selected_category
    df = sheets_data[sheet_name]
    # Filter by both selected location and category
    cat_df = df[(df['Location'] == location) & (df['Category'] == category)]
    st.markdown(f'<h2 style="text-align:center;">{category}</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#666; margin-bottom:2.5rem;">Products in this category</p>', unsafe_allow_html=True)
    if st.button("← Back to Categories", key="back_cats"):
        st.session_state.current_page = 'sheet'
        st.rerun()

    # Display products in rows of 3
    product_rows = list(cat_df.iterrows())
    for i in range(0, len(product_rows), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(product_rows):
                idx, row = product_rows[i + j]
                with cols[j]:
                    product = row['Product']
                    quantity = row['Quantity']
                    price = row['Price (EUR)']

                    # Image paths
                    def get_image_path(product, suffix):
                        import os
                        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
                            path = os.path.join('medicine_photos', f"{product} {suffix}{ext}")
                            if os.path.exists(path):
                                return path
                        return None

                    toggle_key = f"img_toggle_{product}_{idx}"
                    if toggle_key not in st.session_state:
                        st.session_state[toggle_key] = 'front'

                    if st.button(f"Show {'rear' if st.session_state[toggle_key]=='front' else 'front'} image", key=f"toggle_{product}_{idx}"):
                        st.session_state[toggle_key] = 'rear' if st.session_state[toggle_key] == 'front' else 'front'

                    img_path = get_image_path(product, st.session_state[toggle_key])
                    if img_path:
                        st.image(img_path, width=180, caption=f"{product} ({st.session_state[toggle_key]})")
                    else:
                        st.write("No image found.")

                    st.write(f"**Product:** {product}")
                    st.write(f"**Quantity:** {quantity}")
                    st.write(f"**Price (EUR):** {price}")

# Product: Show details and images
elif st.session_state.current_page == 'product':
    sheet_name = st.session_state.selected_sheet
    category = st.session_state.selected_category
    product = st.session_state.selected_product
    df = sheets_data[sheet_name]
    prod_row = df[(df['Category'] == category) & (df['Product'] == product)].iloc[0]
    st.markdown(f'<h2 style="text-align:center;">{product}</h2>', unsafe_allow_html=True)
    if st.button("← Back to Products", type="primary"):
        st.session_state.current_page = 'category'
        st.rerun()
    # Show images
    img_front = get_product_image(product, 'front')
    img_rear = get_product_image(product, 'rear')
    img_cols = st.columns(2)
    if img_front:
        with img_cols[0]:
            st.image(img_front, caption="Front", use_column_width=True)
    if img_rear:
        with img_cols[1]:
            st.image(img_rear, caption="Rear", use_column_width=True)
    # Show details
    st.markdown("### Product Details")
    details = prod_row.to_dict()
    for k, v in details.items():
        st.markdown(f"**{k}:** {v}")   