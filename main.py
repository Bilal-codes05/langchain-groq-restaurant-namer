import streamlit as st
import Langchain_helper  # This should contain your LLM logic

# App Title
st.title("Restaurant Name Generator")

# Sidebar cuisine selector
cuisine = st.sidebar.selectbox(
    "Select a cuisine type:",
    ("Pakistani", "Italian", "Chinese", "Indian", "Mexican","American","Qatari","Turkish","Russian","French")
)

# Generate Button
if st.button("Generate Suggestions"):
    response = Langchain_helper.generate_restaurant_name_and_items_and_tagline(cuisine)

    # Display the restaurant name
    st.header(f"🏷️ {response['restaurant_name'].strip()}")
    
    st.subheader(f"Tagline: {response['tagline'].strip()}")

    # Process and show menu items
    menu_items = [item.strip() for item in response['menu_items'].split(",") if item.strip()]

    st.subheader("🍴 Menu Items")
    for item in menu_items:
        st.markdown(f"- {item}")

