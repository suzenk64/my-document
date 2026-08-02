import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="AI Label & Prescription Scanner", layout="centered")

st.title("📷 Live AI Prescription & Food Label Scanner")
st.write("Apne device ke camera se seedha label ya prescription capture karein aur live verified analysis dekhein.")

api_key = st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("⚠️ Gemini API Key missing! Streamlit Cloud Settings -> Secrets me GEMINI_API_KEY add karein.")
else:
    # Naya GenAI Client (AQ... key support ke saath)
    client = genai.Client(api_key=api_key)

    st.sidebar.header("⚙️ Input Settings")
    input_mode = st.sidebar.radio("Scan Mode Chunein:", ["Live Camera Capture", "File Upload (Gallery)"])

    img = None

    if input_mode == "Live Camera Capture":
        img_file = st.camera_input("Apne Camera ke saamne Label ya Prescription rakhein aur Photo capture karein")
        if img_file:
            img = Image.open(img_file)
    else:
        uploaded_file = st.file_uploader("Label ya Prescription ki photo upload karein", type=["jpg", "jpeg", "png", "webp"])
        if uploaded_file:
            img = Image.open(uploaded_file)

    if img is not None:
        st.image(img, caption="Captured Image", use_column_width=True)
        
        prompt = """
        You are a strict, highly accurate medical and food packaging OCR analyzer. 
        Examine the provided image with extreme accuracy and follow these explicit instructions:

        1. FIRST CHECK (CRITICAL):
           Determine if this image contains a clear, readable FOOD INGREDIENT LABEL, NUTRITIONAL FACT TABLE, or MEDICAL PRESCRIPTION/MEDICINE PACKAGING.
           - IF THE IMAGE IS A SELFIE, A PERSON, A ROOM, A BLANK/BLURRY PHOTO, AN IRRELEVANT OBJECT, OR HAS NO READABLE TEXT/LABEL:
             Respond ONLY with:
             "❌ INVALID SCAN: Photo me koi readable food label ya medical prescription nahi mila. Kripya dabba, packaging ya prescription ki saaf photo lein."
             Do NOT invent, guess, or manufacture any ingredients, chemical names, or medical safety notes.

        2. SECOND CHECK (IF VALID):
           Provide a direct, factual analysis based strictly on what is physically printed or visible on the image:
           - Category: (Food Label / Medical Prescription / Medicine Pack)
           - Extracted Ingredients / Dosage Details: (Exact text read from image)
           - Age Safety & Warnings: (Children 0-12, Adults, Seniors - factual medical/dietary cautions based strictly on identified components)
           - Critical Cautions: (Allergens, High Sugar/Sodium, Steroids, Prescription-only warnings)

        No promotional text, no guessing. Give only ground-checked, factual observations.
        """

        with st.spinner("Analyzing image... Please wait..."):
            try:
                # Naya models.generate_content call
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt, img]
                )
                st.markdown("### 🔍 Analysis Result")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error analyzing image: {e}")
