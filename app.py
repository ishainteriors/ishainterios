import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Isha Interiors AI", page_icon="🏠", layout="centered"
)

st.title("🏠 Isha Interiors — Marketing Generator")
st.write(
    "Generate Instagram/Facebook posts and AI photo prompts for Hyderabad projects."
)

# Fetch API Key from Streamlit Secrets or Environment
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

# Input Form
project_type = st.selectbox(
    "Project Type",
    [
        "3BHK Modern Apartment Interior",
        "2BHK Apartment Interior",
        "Luxury Villa Interior",
        "Modular Kitchen Renovation",
        "Commercial Office",
    ],
)
locality = st.text_input("Locality in Hyderabad", value="Gachibowli")
target_budget = st.selectbox(
    "Target Budget", ["Mid to Premium", "High-End Luxury", "Budget-Friendly"]
)
key_features = st.text_area(
    "Key Design Features",
    value="Modular kitchen, false ceiling with cove lighting, space-saving wardrobes, warm wood finishes",
)

if st.button("🚀 Generate Marketing Post"):
    if not api_key:
        st.error(
            "API Key is missing. Please configure GEMINI_API_KEY in Streamlit Secrets."
        )
    else:
        with st.spinner("Generating post for Isha Interiors..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                You are an expert digital marketing specialist for Isha Interiors, an interior design company in Hyderabad, India.
                PROJECT DETAILS:
                - Type: {project_type}
                - Location: {locality}, Hyderabad
                - Design Features: {key_features}
                - Target Budget: {target_budget}
                
                Return ONLY 3 sections:
                SECTION 1 — SOCIAL MEDIA CAPTION (Highlight features, CTA to contact Isha Interiors for free site visit)
                SECTION 2 — HASHTAGS (12-15 tags including Hyderabad and {locality})
                SECTION 3 — AI IMAGE GENERATION PROMPT (Photorealistic, architectural photography, no people)
                """
                interaction = client.interactions.create(
                    model="gemini-3.6-flash", input=prompt
                )
                st.success("Generated Successfully!")
                st.markdown(interaction.output_text)
            except Exception as e:
                st.error(f"Error: {e}")
