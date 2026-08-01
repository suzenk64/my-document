import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Live AI Health & Ingredient Scanner", layout="wide")

# Custom Styling for Age Cards and Risk Indicators
st.markdown("""
    <style>
    .safe-card { background-color: #d4edda; border-left: 5px solid #28a745; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #155724; }
    .warning-card { background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #856404; }
    .danger-card { background-color: #f8d7da; border-left: 5px solid #dc3545; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #721c24; }
    .age-title { font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

st.title("📸 Live AI Prescription & Food Label Scanner")
st.write("Apne device ke camera se seedha label ya prescription capture karein aur live analysis dekhein.")

# Sidebar Controls for Input Mode
st.sidebar.header("⚙️ Input Settings")
input_mode = st.sidebar.radio("Scan Mode Chunein:", ["Live Camera Capture", "File Upload (Gallery)"])
scan_type = st.sidebar.selectbox("Item Type:", ["Khane/Peene ki Cheez (Food Label)", "Medical Prescription / Report"])

image = None

# Input Handling based on Mode
if input_mode == "Live Camera Capture":
    st.subheader("🔴 Live Camera Scanner")
    # Streamlit ka built-in live camera input widget
    camera_image = st.camera_input("Apne Camera ke saamne Label ya Prescription rakhein aur Photo capture karein")
    if camera_image is not None:
        image = Image.open(camera_image)
else:
    uploaded_file = st.sidebar.file_uploader("Image Upload Karein", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

def generate_mock_analysis(scan_type):
    """
    AI Processing Engine: Yahan real-time me Gemini Vision API / OCR kaam karega.
    """
    if scan_type == "Khane/Peene ki Cheez (Food Label)":
        return {
            "product_name": "Scanned Packaged Food / Beverage",
            "ingredients_found": ["Refined Flour (Maida)", "Trans Fats", "Sodium Chloride", "Artificial Flavours"],
            "accuracy_score": "96%",
            "health_score": "40 / 100 (Caution)",
            "age_cards": {
                "kids": {
                    "status": "Danger",
                    "reason": "Trans fats aur artificial additives bachhon ke growth aur digestion par bura asar daal sakte hain."
                },
                "adults": {
                    "status": "Warning",
                    "reason": "Regular consumption se weight gain aur cholesterol badhne ka risk ho sakta hai."
                },
                "seniors": {
                    "status": "Danger",
                    "reason": "High sodium aur refined ingredients blood pressure aur heart ke liye harmful ho sakte hain."
                }
            }
        }
    else:
        return {
            "product_name": "Scanned Medical Prescription",
            "ingredients_found": ["Pantoprazole 40mg (Khali pet)", "Glimepiride 2mg", "Metformin 500mg"],
            "accuracy_score": "99%",
            "health_score": "Verified Prescription Format",
            "age_cards": {
                "kids": {
                    "status": "Danger",
                    "reason": "Ye heavy adult medication hai. Bachhon ke liye bilkul upyukt nahi hai."
                },
                "adults": {
                    "status": "Safe",
                    "reason": "Doctor ke nirdesh anusar sahi samay par lein. Regular sugar monitoring rakhein."
                },
                "seniors": {
                    "status": "Warning",
                    "reason": "Elderly patients me dosage modification ki zaroorat pad sakti hai. Doctor se salah lein."
                }
            }
        }

# Main Results Dashboard Logic
if image is not None:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("🖼️ Captured Image")
        st.image(image, use_column_width=True)
    
    with col2:
        st.subheader("🔍 Instant Scan Results")
        data = generate_mock_analysis(scan_type)
        
        st.markdown(f"**Item Detected:** `{data['product_name']}`")
        st.markdown(f"**OCR Accuracy:** `{data['accuracy_score']}`")
        st.markdown(f"**Health Score:** `{data['health_score']}`")
        
        st.write("---")
        st.subheader("🧪 Extracted Elements / Ingredients:")
        for item in data['ingredients_found']:
            st.write(f"- {item}")

    st.write("---")
    st.header("👥 Har Umar Ke Liye Age-Specific Health Cards")

    col_k, col_a, col_s = st.columns(3)

    # 1. Kids Card (0-12 Years)
    with col_k:
        k_data = data['age_cards']['kids']
        css_class = "danger-card" if k_data['status'] == "Danger" else ("warning-card" if k_data['status'] == "Warning" else "safe-card")
        st.markdown(f"""
            <div class="{css_class}">
                <div class="age-title">👶 Bachhon ke liye (0-12 yrs)</div>
                <p><b>Status: {k_data['status']}</b></p>
                <p>{k_data['reason']}</p>
            </div>
        """, unsafe_allow_html=True)

    # 2. Adults Card (13-59 Years)
    with col_a:
        a_data = data['age_cards']['adults']
        css_class = "danger-card" if a_data['status'] == "Danger" else ("warning-card" if a_data['status'] == "Warning" else "safe-card")
        st.markdown(f"""
            <div class="{css_class}">
                <div class="age-title">🧑 Adults ke liye (13-59 yrs)</div>
                <p><b>Status: {a_data['status']}</b></p>
                <p>{a_data['reason']}}}</p>
            </div>
        """, unsafe_allow_html=True)

    # 3. Seniors Card (60+ Years)
    with col_s:
        s_data = data['age_cards']['seniors']
        css_class = "danger-card" if s_data['status'] == "Danger" else ("warning-card" if s_data['status'] == "Warning" else "safe-card")
        st.markdown(f"""
            <div class="{css_class}">
                <div class="age-title">👵 Seniors ke liye (60+ yrs)</div>
                <p><b>Status: {s_data['status']}</b></p>
                <p>{s_data['reason']}</p>
            </div>
        """, unsafe_allow_html=True)

else:
    st.info("👆 Live Camera mode active hai. Upar diye gaye camera box mein 'Take Photo' button dabakar scan karein.")