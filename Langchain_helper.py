from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from secret_key import groq_cloud_api

import os
os.environ["GROQ_API_KEY"] = groq_cloud_api

llm = ChatGroq(
    temperature=0.8,  # Increased for more creativity
    model_name="llama3-8b-8192"
)

def generate_restaurant_name_and_items(cuisine):
    # More creative and contextual name generation
    prompt_template_name = PromptTemplate(
        input_variables=["cuisine"],
        template=(
            "You're a branding expert. Suggest a unique and creative restaurant name for a restaurant "
            "that specializes in {cuisine} cuisine. Return only the name without any explanation."
        )
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    # Menu items prompt grounded in both name and cuisine
    prompt_template_items = PromptTemplate(
        input_variables=["restaurant_name", "cuisine"],
        template=(
            "Suggest exactly 5 popular traditional food items served at a restaurant named {restaurant_name} "
            "that specializes in {cuisine} cuisine. Return only the list as comma-separated values without any explanations."
        )
    )
    items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")

    # SequentialChain
    chain = SequentialChain(
        chains=[name_chain, items_chain],
        input_variables=["cuisine"],
        output_variables=["restaurant_name", "menu_items"],
        verbose=False
    )

    response = chain({"cuisine": cuisine})
    return response

if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Pakistani"))
