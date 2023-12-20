from model import engine, Users, Recipes, Aisles, Ingredients
from sqlmodel import Session, select, delete
from collections import defaultdict


import hashlib


"""
                                                UTILITAIRE
"""

"""
    hashSha256
    Prend une chaine de caracteres et retoune le SHA-256 de cette chaine
"""
def hashSha256(string):
    string_bytes = string.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(string_bytes)
    sha256_hash = sha256.hexdigest()
    
    return sha256_hash

"""
                                                USERS
"""

"""
createUser
Inserts a new row in the Users table with the received login and clear password.

Parameters:
login (str): The login of the user.
pswd (str): The password of the user.

Returns:
user: The created user.
"""
def createUser(login, pswd):
    user = Users(login=login, pswd=hashSha256(pswd))

    with Session(engine) as session:
        session.add(user)
        session.commit()

        session.refresh(user)
        return user
    
"""
getAllUsers
Returns all users present in the database.

Returns:
list: A list of all users.
"""
def getAllUsers():
    with Session(engine) as session:  
        statement = select(Users)  
        results = session.exec(statement)  
        return results.fetchall()
    
"""
checkLoginAvaible
Checks if the username already exists.

Parameters:
login (str): The login of the user.

Returns:
bool: True if the username is available, False otherwise.
"""
def checkLoginAvaible(login):
    with Session(engine) as session:
        statement = select(Users).where(Users.login == login)
        results = session.exec(statement)
        if results.fetchall() == []:
            return True
        else:
            return False

"""
deleteUsers
Deletes a user from the database based on the user id.

Parameters:
id_user (int): The id of the user to be deleted.
"""
def deleteUsers(id_user):
    with Session(engine) as session:
        statement = select(Users).where(Users.id == id_user)
        results = session.exec(statement)
        user = results.one()
        session.delete(user)
        session.commit()

"""
                                                RECIPES
"""


"""
createRecipe
Inserts a new row in the Recipes table with the given name, description, and user id.

Parameters:
name (str): The name of the recipe.
description (str): The description of the recipe.
id_user (int): The id of the user who created the recipe.

Returns:
recipe: The created recipe.
"""
def createRecipe(name, description, id_user):
    recipe = Recipes(name=name, description=description, fk_user=id_user)

    with Session(engine) as session:
        session.add(recipe)
        session.commit()

        session.refresh(recipe)
        return recipe


"""
getRecipesByUserId
Fetches all recipes linked to a user via the user id.

Parameters:
user_id (int): The id of the user.

Returns:
list: A list of recipes linked to the user.
"""
def getRecipesByUserId(user_id):
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.fk_user == user_id)
        results = session.exec(statement)

        return results.fetchall()
    

"""
getRecipeById
Fetches a recipe via its id.

Parameters:
recipe_id (int): The id of the recipe.

Returns:
recipe: The fetched recipe.
"""
def getRecipeById(recipe_id):
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.id == recipe_id)
        results = session.exec(statement)

        return results.fetchall()
    

"""
checkRecipeNameAvaible
Checks if the recipe name already exists for a specific user.

Parameters:
user_id (int): The id of the user.
name (str): The name of the recipe.

Returns:
bool: True if the recipe name is available for the user, False otherwise.
"""
def checkRecipeNameAvaible(user_id, name):
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.name == name).where(Recipes.fk_user == user_id)
        results = session.exec(statement)
        if results.fetchall() == []:
            return True
        else:
            return False
        
"""
deleteRecipes
Deletes a recipe from the database based on the recipe id.

Parameters:
id_recipe (int): The id of the recipe to be deleted.

Note:
This function will first delete all ingredients linked to the recipe by calling the deleteIngredientFromRecipe function.
Then it will delete the recipe itself.
"""
def deleteRecipes(id_recipe):
    deleteIngredientFromRecipe(id_recipe)
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.id == id_recipe)
        results = session.exec(statement)
        recipe = results.one()
    
        session.delete(recipe)
        session.commit()


"""
                                                AISLES
"""


"""
createAisle
Inserts a new row in the Aisles table with the given name.

Parameters:
name (str): The name of the aisle.

Returns:
aisle: The created aisle.
"""
def createAisle(name):
    aisle = Aisles(name=name)

    with Session(engine) as session:
        session.add(aisle)
        session.commit()

        session.refresh(aisle)
        return aisle
    

"""
getAllAisles
Returns all aisles present in the database.

Returns:
list: A list of all aisles.
"""
def getAllAisles():
    with Session(engine) as session:  
        statement = select(Aisles)  
        results = session.exec(statement)  
        return results.fetchall()

"""
checkAisleNameAvaible
Checks if the aisle name already exists in the database.

Parameters:
name (str): The name of the aisle.

Returns:
bool: True if the aisle name is available, False otherwise.
"""
def checkAisleNameAvaible(name):
    with Session(engine) as session:
        statement = select(Aisles).where(Aisles.name == name)
        results = session.exec(statement)
        if results.fetchall() == []:
            return True
        else:
            return False

"""
deleteAisles
Deletes an aisle from the database based on the aisle id.

Parameters:
id_aisle (int): The id of the aisle to be deleted.
"""
def deleteAisles(id_aisle):
    with Session(engine) as session:
        statement = select(Aisles).where(Aisles.id == id_aisle)
        results = session.exec(statement)
        aisle = results.one()
        session.delete(aisle)
        session.commit()



"""
                                                INGREDIENTS
"""


"""
createIngredient
Inserts a new row in the Ingredients table with the given name, quantity, unit, aisle id, and recipe id.

Parameters:
name (str): The name of the ingredient.
quantity (float): The quantity of the ingredient.
unit (str): The unit of measurement for the ingredient.
id_aisle (int): The id of the aisle where the ingredient is located.
id_recipe (int): The id of the recipe that the ingredient is part of.

Returns:
ingredient: The created ingredient.
"""
def createIngredient(name, quantity, unit, id_aisle, id_recipe):
    ingredient = Ingredients(name=name, quantity=quantity, unit=unit, fk_recipe=id_recipe, fk_aisle=id_aisle)

    with Session(engine) as session:
        session.add(ingredient)
        session.commit()

        session.refresh(ingredient)
        return ingredient

"""
createMultipleIngredients
Inserts multiple rows in the Ingredients table, all having the same recipe id.

Parameters:
ingredientsList (list): A list of ingredient data. Each item in the list is an object with properties: name, quantity, unit, and aisle id.
id_recipe (int): The id of the recipe that the ingredients are part of.
"""
def createMultipleIngredients(ingredientsList, id_recipe):
    with Session(engine) as session:
        ingredients_to_add = []
        for ingredient_data in ingredientsList:
            name = ingredient_data.name
            quantity = ingredient_data.quantity
            unit = ingredient_data.unit
            id_aisle = ingredient_data.rayon
            
            ingredient = Ingredients(name=name, quantity=quantity, unit=unit, fk_recipe=id_recipe, fk_aisle=id_aisle)
            ingredients_to_add.append(ingredient)
        
        session.add_all(ingredients_to_add)
        session.commit()


"""
getMultiplesIngredientsByRecipeIds
Fetches all ingredients linked to a list of recipe ids.

Parameters:
recipe_ids (list): A list of recipe ids.

Returns:
list: A list of ingredients linked to the recipes.
"""
def getMultiplesIngredientsByRecipeIds(recipe_ids):
    with Session(engine) as session:
        statement = select(Ingredients, Aisles).where(Ingredients.fk_recipe.in_(recipe_ids)).where(Ingredients.fk_aisle == Aisles.id)
        results = session.exec(statement)

        ingredients_dict = defaultdict(float)

        for row in results.fetchall():
            ingredient_key = (row.Ingredients.name, row.Ingredients.unit, row.Aisles.name)
            ingredients_dict[ingredient_key] += row.Ingredients.quantity
        
        unique_ingredients = [
            {'name': key[0], 'unit': key[1], 'aisle': key[2], 'quantity': quantity}
            for key, quantity in ingredients_dict.items()
        ]
        return unique_ingredients


"""
getIngredientsByRecipeId
Fetches all ingredients linked to a specific recipe id.

Parameters:
recipe_id (int): The id of the recipe.

Returns:
list: A list of ingredients linked to the recipe.
"""
def getIngredientsByRecipeId(recipe_id):
    with Session(engine) as session:
        statement = select(Ingredients).where(Ingredients.fk_recipe == recipe_id)
        results = session.exec(statement)

        return results.fetchall()
    

"""
deleteIngredientFromRecipe
Deletes all ingredients linked to a specific recipe id from the database.

Parameters:
recipe_id (int): The id of the recipe.
"""
def deleteIngredientFromRecipe(id_recipe):
    with Session(engine) as session:
        ingredients_to_delete = delete(Ingredients).where(Ingredients.fk_recipe == id_recipe)
        session.exec(ingredients_to_delete)
        session.commit()


def main():
    recipe_ids_to_search = [1, 2]
    ingredients_related_to_recipes = getIngredientsByRecipeIds(recipe_ids_to_search)

    if ingredients_related_to_recipes:
        print("Ingrédients associés aux recettes sélectionnées :")
        for ingredient in ingredients_related_to_recipes:
            print(f"{ingredient.name}, Quantite: {ingredient.quantity}{ingredient.unit}")

if __name__ == "__main__":
    main()