import streamlit as st
from io import BytesIO
import os
from dotenv import load_dotenv
import Langchain_helper

# Load API key
load_dotenv()
hf_token = os.getenv("HF_API_KEY")

# Page setup
st.set_page_config(page_title="Restaurant Name Generator", page_icon="🍽️")

# Sidebar content
st.sidebar.title("🍴 Restaurant Idea Generator")
st.sidebar.markdown("Welcome! Generate unique restaurant names, taglines, logos, and custom menus using our Personalizd Culinary Generator.")
st.sidebar.markdown("---")

# Input fields in sidebar
cuisine = st.sidebar.text_input("🍽️ Cuisine Type", placeholder="e.g. Pakistani, Italian, Chinese")
theme = st.sidebar.text_input("🎨 Theme or Mood", placeholder="e.g. Cozy, Futuristic, Rustic")

# Generate button in sidebar
generate = st.sidebar.button("✨ Generate Idea")

# Main title
st.title("🥘 Personalized Culinary Generator")

# Check for Hugging Face Token
if not hf_token:
    st.error("❌ HuggingFace API token missing! Please set `HF_API_KEY` in your .env file.")
    st.stop()

# On generate button click
if generate:
    cuisine = cuisine.strip()
    theme = theme.strip()

    if not cuisine or not theme:
        st.warning("⚠️ Please enter both cuisine and theme.")
    else:
        with st.spinner("🧠 Thinking creatively..."):
            response = Langchain_helper.generate_restaurant_name_and_items_and_tagline(cuisine, theme)
            logo_prompt = Langchain_helper.generate_logo_prompt(cuisine, theme)
            image_data = Langchain_helper.generate_logo_image(logo_prompt)

        if "error" in response:
            st.error(f"❌ Error: {response['error']}")
            st.text_area("Raw LLM Response", response.get("raw_response", ""), height=200)
        else:
            st.header(f"🏷️ {response['restaurant_name']}")
            st.subheader(f"✨ Tagline: _{response['tagline']}_")

            st.markdown("### 🖼️ Logo Concept Prompt")
            st.code(logo_prompt)

            if image_data:
                st.image(BytesIO(image_data), caption="AI-Generated Logo", use_column_width=True)
            else:
                st.warning("⚠️ Logo generation failed. Please try again after a few seconds or check your Hugging Face usage.")

            # Stylish menu section
            st.markdown("### 🍴 Menu")
            for item in response['menu_items']:
                if ":" in item:
                    name, desc = item.split(":", 1)
                    st.markdown(f"""
                        <div style="margin-bottom:10px;">
                            <span style="font-size:18px; font-weight:bold;">{name.strip()}</span><br>
                            <span style="font-size:13px;">{desc.strip()}</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"- {item.strip()}")
