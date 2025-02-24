
from flask import Flask, request, jsonify # type: ignore
import os

app = Flask(__name__)

# Ensure the directory for shopping lists exists
if not os.path.exists('shopping_lists'):
    os.makedirs('shopping_lists')

# Endpoint to create a shopping list
@app.route('/create-list', methods=['POST'])
def create_shopping_list():
    data = request.get_json()
    recipe_id = data.get('recipe_id')
    additional_ingredients = data.get('additional_ingredients', [])
    clear_list = data.get('clear_list', False)
    
    recipe_ingredients = get_ingredients_from_recipe(recipe_id)
    
    if clear_list:
        shopping_list = []
    else:
        shopping_list = recipe_ingredients
    
    shopping_list.extend(additional_ingredients)
    
    filename = 'shopping_lists/shoppingList.txt'
    with open(filename, 'w') as f:
        for ingredient in shopping_list:
            f.write(f"{ingredient}\n")
    
    return jsonify({"message": "Shopping list created", "filename": filename})

def get_ingredients_from_recipe(recipe_id):
    return ["2 cups flour", "1 tsp salt", "1/2 cup butter", "1 egg", "1 tbsp sugar"]

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