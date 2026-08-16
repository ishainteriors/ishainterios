from io import BytesIO
from google import genai
from google.genai import types
import streamlit as st
from PIL import Image

# Initialize the Gemini client using st.secrets or environment variable
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


def generate_interior_image(image_prompt: str):
  """Generates an interior design preview image using the updated Google GenAI SDK.

  """
  try:
    # Invoke Imagen via the updated client method
    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=image_prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",  # Options: "1:1", "16:9", "4:3", "3:4", "9:16"
            person_generation="ALLOW_ADULT",
        ),
    )

    # Process and render the generated image
    if response.generated_images:
      for generated_image in response.generated_images:
        image_bytes = generated_image.image.image_bytes
        image = Image.open(BytesIO(image_bytes))
        st.image(
            image,
            caption="AI Generated Interior Design Preview",
            use_container_width=True,
        )
    else:
      st.warning(
          "No image was generated. Please try again with a revised prompt."
      )

  except Exception as e:
    st.error(f"Failed to generate image: {e}")
