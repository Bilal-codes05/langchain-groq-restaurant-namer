import requests
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import groq_cloud_api
from huggingface_hub import InferenceClient
import os

# Set up Groq LLM (LLaMA 3)
llm = ChatGroq(
    model_name="llama3-8b-8192",
    api_key=groq_cloud_api
)



# Restaurant branding generation
def generate_restaurant_name_and_items_and_tagline(cuisine: str, theme: str) -> dict:
    prompt = PromptTemplate(
        input_variables=["cuisine", "theme"],
        template="""
You are a branding and creative food expert AI.

Based on the following details:
Cuisine: {cuisine}
Theme: {theme}

Generate the following:
1. A unique and catchy restaurant name.
2. A creative and short tagline matching the cuisine and theme.
3. A list of exactly 6 menu items WITH short, flavorful descriptions.

Return the response in **this exact format**:

Restaurant Name: <name>
Tagline: <tagline>
Menu:
- <Item Name with Bold Syntax>: <Short Description>
- <Item Name with Bold Syntax>: <Short Description>
- <Item Name with Bold Syntax>: <Short Description>
- <Item Name with Bold Syntax>: <Short Description>
- <Item Name with Bold Syntax>: <Short Description>
- <Item Name with Bold Syntax>: <Short Description>
"""
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"cuisine": cuisine, "theme": theme}).strip()

    # Parse the response safely
    try:
        name = response.split("Restaurant Name:")[1].split("Tagline:")[0].strip()
        tagline = response.split("Tagline:")[1].split("Menu:")[0].strip()
        menu_raw = response.split("Menu:")[1].strip()

        menu_items = []
        for line in menu_raw.split("\n"):
            if ":" in line:
                item_name, desc = line.split(":", 1)
                menu_items.append(f"{item_name.strip()}: {desc.strip()}")

        return {
            "restaurant_name": name,
            "tagline": tagline,
            "menu_items": menu_items
        }

    except Exception as e:
        print("Parsing error:", e)
        print("Raw response:", response)
        return {
            "restaurant_name": "",
            "tagline": "",
            "menu_items": [],
            "error": f"Parsing failed: {str(e)}",
            "raw_response": response
        }

# Logo prompt generator
def generate_logo_prompt(cuisine: str, theme: str) -> str:
    return (
        f"A symbolic logo design for a {theme.lower()} themed {cuisine.lower()} cuisine restaurant. "
        "Artistic, modern, minimal, and high quality. No text, just the visual symbol. Rich colors."
    )


hf_token = os.getenv("HF_API_KEY")  # or HF_TOKEN

client = InferenceClient(
    provider="nebius",
    api_key=hf_token,
)

def generate_logo_image(prompt: str):
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev",
    )
    # Return raw bytes for Streamlit display
    from io import BytesIO
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
# # HuggingFace image generation (Stable Diffusion)
# def generate_logo_image(prompt: str, hf_token: str):
#     api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
#     headers = {"Authorization": f"Bearer {hf_token}"}
#     payload = {"inputs": prompt}

#     response = requests.post(api_url, headers=headers, json=payload)

#     print("🧪 Prompt sent to HF:", prompt)
#     print("📡 Status Code:", response.status_code)
#     print("📄 Response Text:", response.text)

#     if response.status_code == 200:
#         return response.content
#     elif response.status_code == 503:
#         print("⏳ Model loading, retry later.")
#         return None
#     else:
#         print(f"❌ Error: {response.status_code} - {response.text}")
#         return None

