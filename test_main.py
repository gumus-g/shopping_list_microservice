
import requests # type: ignore

# Base URL for the microservice
BASE_URL = 'http://localhost:5001'

# Function to prompt user for confirmation
def prompt_user(message):
    while True:
        response = input(f"{message} (yes/no): ").strip().lower()
        if response in ['yes', 'no']:
            return response == 'yes'
        print("Please respond with 'yes' or 'no'.")

# Function to create a shopping list
def create_shopping_list(recipe_id, additional_ingredients, clear_list):
    if not prompt_user("WARNING: Creating a new shopping list will overwrite the existing shopping list. Do you want to continue?"):
        print("Operation cancelled.")
        return
    url = f'{BASE_URL}/create-list'
    payload = {
        "recipe_id": recipe_id,
        "additional_ingredients": additional_ingredients,
        "clear_list": clear_list
    }
    
    # Sending the request to create a shopping list
    response = requests.post(url, json=payload)
    # Handling the response from the microservice

    if response.status_code == 200:
        print("Shopping list created:", response.json()["filename"])
    else:
        print("Failed to create shopping list:", response.status_code, response.text)

# Function to add ingredients to the shopping list
def add_ingredients(additional_ingredients):
    if not prompt_user("WARNING: Adding ingredients to the existing shopping list. Do you want to continue?"):
        print("Operation cancelled.")
        return
    url = f'{BASE_URL}/add-ingredients'
    payload = {
        "additional_ingredients": additional_ingredients
    }

    # Sending the request to add ingredients to the shopping list
    response = requests.post(url, json=payload)
    # Handling the response from the microservice

    if response.status_code == 200:
        print("Ingredients added:", response.json()["filename"])
    else:
        print("Failed to add ingredients:", response.status_code, response.text)

# Function to erase the shopping list
def erase_shopping_list():
    if not prompt_user("WARNING: Erasing the shopping list will clear all ingredients from the list. Do you want to continue?"):
        print("Operation cancelled.")
        return
    url = f'{BASE_URL}/erase-list'

    # Sending the request to erase the shopping list
    response = requests.delete(url)
    # Handling the response from the microservice

    if response.status_code == 200:
        print("Shopping list erased:", response.json()["filename"])
    else:
        print("Failed to erase shopping list:", response.status_code, response.text)

def main():
    # Step 1: Create a shopping list
    print("Creating shopping list...")
    create_shopping_list(1, ["1 cup sugar", "2 eggs"], False)
    
    # Step 2: Add ingredients to the shopping list
    print("Adding ingredients to shopping list...")
    add_ingredients(["3 bananas", "1 liter milk"])
    
    # Step 3: Fetch and display the shopping list content
    print("Shopping list content:")
    with open('shopping_lists/shoppingList.txt', 'r') as f:
        content = f.read()
        print(content)
    
    # Step 4: Erase the shopping list
    print("Erasing shopping list...")
    erase_shopping_list()

if __name__ == '__main__':
    main()