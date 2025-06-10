from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import groq_cloud_api

llm = ChatGroq(
    model_name="llama3-8b-8192",
    api_key=groq_cloud_api
)

def generate_restaurant_name_and_items_and_tagline(cuisine: str, theme: str) -> dict:
    prompt = PromptTemplate(
        input_variables=["cuisine", "theme"],
        template="""
You are a creative AI assistant. Generate a restaurant name, a catchy tagline, and a simple list of 6 traditional menu items (one per line, no descriptions), based on the following:

Cuisine: {cuisine}
Theme: {theme}

Respond in this exact format:
Restaurant Name: <name>
Tagline: <tagline>
Menu:
- item1
- item2
- item3
- item4
- item5
- item6
"""
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"cuisine": cuisine, "theme": theme})

    try:
        name = response.split("Restaurant Name:")[1].split("Tagline:")[0].strip()
        tagline = response.split("Tagline:")[1].split("Menu:")[0].strip()
        menu_raw = response.split("Menu:")[1].strip()
        menu_items = [line.strip().lstrip("- ").strip() for line in menu_raw.split("\n") if line.strip()]
        return {
            "restaurant_name": name,
            "tagline": tagline,
            "menu_items": menu_items
        }
    except Exception as e:
        return {
            "restaurant_name": "",
            "tagline": "",
            "menu_items": [],
            "error": f"Parsing failed: {str(e)}",
            "raw_response": response,
           
        }
