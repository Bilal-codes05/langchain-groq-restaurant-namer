from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from uuid import uuid4
from Langchain_helper import generate_restaurant_name_and_items_and_tagline

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
restaurants: Dict[str, dict] = {}

class CuisineRequest(BaseModel):
    cuisine: str

class Restaurant(BaseModel):
    restaurant_name: str
    menu_items: List[str]
    tagline: str

class RestaurantWithID(Restaurant):
    id: str

# POST - Create/generate
@app.post("/generate", response_model=RestaurantWithID)
def generate_restaurant(cuisine_data: CuisineRequest):
    result = generate_restaurant_name_and_items_and_tagline(cuisine_data.cuisine)
    restaurant_id = str(uuid4())
    restaurant = {
        "restaurant_name": result["restaurant_name"],
        "menu_items": result["menu_items"].split(", "),
        "tagline": result["tagline"]
    }
    restaurants[restaurant_id] = restaurant
    return {**restaurant, "id": restaurant_id}

# GET - All restaurants
@app.get("/restaurants", response_model=List[RestaurantWithID])
def get_all_restaurants():
    return [{**restaurant, "id": rid} for rid, restaurant in restaurants.items()]

# GET - By name
@app.get("/restaurants/by-name/{restaurant_name}", response_model=List[RestaurantWithID])
def get_restaurants_by_name(restaurant_name: str):
    search_name = restaurant_name.strip().lower().replace('"', '')
    matches = [
        {**restaurant, "id": rid}
        for rid, restaurant in restaurants.items()
        if restaurant["restaurant_name"].strip().lower().replace('"', '') == search_name
    ]
    if not matches:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return matches

# PUT - Update
@app.put("/restaurants/{restaurant_id}", response_model=RestaurantWithID)
def update_restaurant(restaurant_id: str, updated_data: Restaurant):
    if restaurant_id not in restaurants:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurants[restaurant_id] = updated_data.dict()
    return {**updated_data.dict(), "id": restaurant_id}

# DELETE - Delete
@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(restaurant_id: str):
    if restaurant_id not in restaurants:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    del restaurants[restaurant_id]
    return {"detail": "Restaurant deleted"}
