
from flask import Flask, request, jsonify # type: ignore
import os

import requests # needed for HTTP requests

app = Flask(__name__)

# Ensure the directory for shopping lists exists
if not os.path.exists('shopping_lists'):
    os.makedirs('shopping_lists')

# Endpoint to create a shopping list
@app.route('/create-list', methods=['POST'])
def create_shopping_list():
    print("Received POST request to /create-list")

    data = request.get_json()
    print(f"Request data: {data}")

    recipe_id = data.get('recipe_id')
    # additional_ingredients = data.get('additional_ingredients', [])
    # clear_list = data.get('clear_list', False)

    print(f"Parsed recipe_id: {recipe_id}")
    
    recipe_ingredients = get_ingredients_from_recipe(recipe_id)
    print(f"Fetched ingredients: {recipe_ingredients}")
    
    # if clear_list:
    #     shopping_list = []
    # else:
    #     shopping_list = recipe_ingredients
    shopping_list = recipe_ingredients
    
    # shopping_list.extend(additional_ingredients)
    print(f"Final shopping list: {shopping_list}")
    
    filename = 'shopping_lists/shoppingList.txt'
    print(f"Writing to file: {filename}")

    with open(filename, 'w') as f:
        for ingredient in shopping_list:
            f.write(f"{ingredient}\n")

    print(f"Shopping list saved to {filename}")
    
    return jsonify({"message": "Shopping list created", "filename": filename})

# def get_ingredients_from_recipe(recipe_id):
#     return ["2 cups flour", "1 tsp salt", "1/2 cup butter", "1 egg", "1 tbsp sugar"]

def get_ingredients_from_recipe(recipe_id):
    try:
        print(f"Fetching ingredients for recipe ID: {recipe_id}")
        # fetch the recipe data from the main server
        response = requests.get(f'http://localhost:5555/recipes')
        response.raise_for_status()
        recipes = response.json()
        
        # find the recipe by its it and return its ingredients
        if 0 <= recipe_id < len(recipes):
            ingredients = recipes[recipe_id].get('ingredients', '')
            # split ingredients into a list if they are in a csv format
            return [ingredient.strip() for ingredient in ingredients.split(',')]
        
        print(f"Recipe ID {recipe_id} is out of range.")
        return []
    
    except requests.RequestException as e:
        print(f"Error fetching ingredients: {e}")
        return []

# Endpoint to add ingredients to the shopping list
@app.route('/add-ingredients', methods=['POST'])
def add_ingredients():
    data = request.get_json()
    additional_ingredients = data.get('additional_ingredients', [])
    
    shopping_list = load_existing_shopping_list()
    shopping_list.extend(additional_ingredients)
    
    filename = 'shopping_lists/shoppingList.txt'
    with open(filename, 'w') as f:
        for ingredient in shopping_list:
            f.write(f"{ingredient}\n")
    
    return jsonify({"message": "Ingredients added", "filename": filename})

def load_existing_shopping_list():
    try:
        with open('shopping_lists/shoppingList.txt', 'r') as f:
            shopping_list = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        shopping_list = []
    return shopping_list

# Endpoint to erase the shopping list
@app.route('/erase-list', methods=['DELETE'])
def erase_shopping_list():
    shopping_list = []
    
    filename = 'shopping_lists/shoppingList.txt'
    with open(filename, 'w') as f:
        for ingredient in shopping_list:
            f.write(f"{ingredient}\n")
    
    return jsonify({"message": "Shopping list erased", "filename": filename})

if __name__ == '__main__':
    app.run(port=5001, debug=True)