import streamlit as st
import Langchain_helper

st.set_page_config(page_title="Restaurant Name Generator", page_icon="🍽️")

st.title("🍽️ Restaurant Name Generator")

# Input from user for cuisine & theme
cuisine = st.text_input("Enter the cuisine type:", placeholder="e.g. Pakistani, Italian, Chinese")
theme = st.text_input("Enter the theme or mood:", placeholder="e.g. Cozy, Futuristic, Rustic")

if st.button("Generate Suggestions"):
    if not cuisine.strip() or not theme.strip():
        st.warning("⚠️ Please enter both cuisine and theme to generate suggestions.")
    else:
        with st.spinner("Generating..."):
            response = Langchain_helper.generate_restaurant_name_and_items_and_tagline(cuisine.strip(), theme.strip())

        if "error" in response:
            st.error(f"Error: {response['error']}")
            st.text_area("Raw Response:", response.get("raw_response", ""), height=200)
        else:
            st.header(f"🏷️ {response['restaurant_name']}")
            st.subheader(f"Tagline: {response['tagline']}")
            st.subheader("🍴 Menu Items")
            for item in response['menu_items']:
                st.markdown(f"- {item}")
