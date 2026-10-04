import streamlit as st
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT


# Gemini client
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


st.set_page_config(
    page_title="Snap & Grow",
    page_icon="🌱",
    layout="centered"
)


st.title("🌱 Snap & Grow")
st.write("AI Plant Health Assistant")

st.info(
    "Upload a clear photo of your plant or leaf. "
    "Snap & Grow will analyze visible signs and give basic care suggestions."
)


uploaded_file = st.file_uploader(
    "📸 Upload a plant/leaf photo",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded plant image",
        use_container_width=True
    )

    if st.button("🔍 Analyze Plant"):

        with st.spinner("Analyzing your plant..."):

            image_bytes = uploaded_file.getvalue()

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    SYSTEM_PROMPT,
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=uploaded_file.type
                    )
                ]
            )

        st.subheader("🌿 Plant Analysis")

        st.write(response.text)