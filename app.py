import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Isha Interiors AI Hub",
    page_icon="🏠",
    layout="centered"
)
st.title("🏠 Isha Interiors")
st.write("Generate social media posts, local hashtags, and high-resolution design images instantly.")

# Fetch API Key from Streamlit Secrets or Environment
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

# Input Controls
language = st.radio("Select Output Language", ["English", "Telugu", "Hindi"], horizontal=True)

# Expanded Categorized Project Options
project_type = st.selectbox(
    "Project Type",
    [
        "--- 🏠 RESIDENTIAL ---",
        "1BHK Apartment Interior",
        "2BHK Apartment Interior",
        "3BHK Apartment Interior",
        "4BHK Apartment Interior",
        "Luxury Apartment Interior",
        "Villa Interior",
        "Duplex House Interior",
        "Independent House Interior",
        "--- 🍳 KITCHEN & ROOMS ---",
        "Modular Kitchen",
        "Living Room Interior",
        "Master Bedroom Interior",
        "Kids Bedroom Interior",
        "Wardrobe & Storage",
        "--- 🏢 COMMERCIAL ---",
        "Corporate Office Interior",
        "Retail Store Interior",
        "Showroom Interior",
        "Restaurant Interior",
        "Clinic Interior",
        "Salon & Spa Interior",
        "--- 💡 OTHER SERVICES ---",
        "Home Renovation",
        "Commercial Renovation",
        "Turnkey Interior Project",
        "Interior Design Consultation",
        "Not Sure — Help Me Choose"
    ],
)

# Complete Hyderabad & Nearby Locations
localities_list = [
    "Gachibowli", "HITEC City", "Madhapur", "Financial District", "Kondapur",
    "Nanakramguda", "Raidurg", "Kokapet", "Banjara Hills", "Jubilee Hills",
    "Narsingi", "Manikonda", "Begumpet", "Somajiguda", "Punjagutta",
    "Ameerpet", "Kukatpally", "Miyapur", "Uppal", "Secunderabad",
    "Khairatabad", "Mehdipatnam", "Masab Tank", "Abids", "Himayatnagar",
    "Koti", "Dilsukhnagar", "LB Nagar", "Nagole", "Kompally", "Suchitra",
    "Alwal", "Tarnaka", "Nacharam", "Habsiguda", "ECIL", "Bowenpally",
    "Shamshabad", "Khammam", "Warangal", "Other (Type Custom Location)"
]

selected_locality = st.selectbox("Locality / Area", localities_list)

if selected_locality == "Other (Type Custom Location)":
    locality = st.text_input("Enter Custom Location Name", value="Hyderabad")
else:
    locality = selected_locality

target_budget = st.selectbox(
    "Target Budget", ["Mid to Premium", "High-End Luxury", "Budget-Friendly"]
)

key_features = st.text_area(
    "Key Design Features",
    value="Modular kitchen, false ceiling with cove lighting, space-saving wardrobes, warm wood finishes",
)

if st.button("🚀 Generate Post & AI Image"):
    if project_type.startswith("---"):
        st.warning("Please select a valid project type instead of a header category.")
    elif not api_key:
        st.error("API Key is missing. Please configure GEMINI_API_KEY in Streamlit Secrets.")
    else:
        client = genai.Client(api_key=api_key)
        
        # Step 1: Text Generation
        with st.spinner("Generating marketing caption and prompt..."):
            try:
                text_prompt = f"""
                You are an expert digital marketing specialist for Isha Interiors, an interior design company in Hyderabad, India.
                Language requested: {language}.
                
                PROJECT DETAILS:
                - Type: {project_type}
                - Location: {locality}, Hyderabad
                - Design Features: {key_features}
                - Target Budget: {target_budget}
                
                Generate content in {language}.
                Return ONLY 3 labeled sections:
                SECTION 1 — SOCIAL MEDIA CAPTION (Engaging tone, highlight features, call to action to contact Isha Interiors for a free site visit).
                SECTION 2 — HASHTAGS (12-15 relevant tags including #IshaInteriors, Hyderabad, and #{locality.replace(' ', '')}).
                SECTION 3 — AI IMAGE GENERATION PROMPT (In English: Photorealistic architectural interior photo, no people).
                """
                
                text_response = client.interactions.create(
                    model="gemini-3.6-flash",
                    input=text_prompt
                )
                generated_text = text_response.output_text
                
                st.success("Marketing Content Ready!")
                st.markdown(generated_text)
                
            except Exception as e:
                st.error(f"Text Generation Error: {e}")
                generated_text = None

        # Step 2: Direct Image Generation
        if generated_text:
            with st.spinner("Generating photorealistic design image..."):
                try:
                    img_prompt = f"Photorealistic interior design photography of {project_type} in Hyderabad with {key_features}, luxury warm ambient lighting, 8k resolution, magazine quality, no people."
                    
                    image_result = client.models.generate_images(
                        model='imagen-3.0-generate-002',
                        prompt=img_prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,
                            aspect_ratio="1:1"
                        )
                    )
                    
                    for generated_image in image_result.generated_images:
                        st.subheader("🖼️ Generated Project Visual")
                        st.image(generated_image.image.image_bytes, caption=f"{project_type} — {locality}")
                        
                except Exception as img_err:
                    st.info("Image generation fallback: Copy Section 3 prompt into Midjourney or Canva if Imagen access is limited.")
