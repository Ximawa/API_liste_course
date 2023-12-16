from model import engine, Users, Recipes, Aisles, Ingredients
from sqlmodel import Session, select 

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
    Insert une nouvelle ligne dans la table Users avec le login et mdp en claire recu

"""
def createUser(login, pswd):
    user = Users(login=login, pswd=hashSha256(pswd))

    with Session(engine) as session:
        session.add(user)
        session.commit()


"""
    getAllUsers
    Retourne tout les utilisateurs present en BDD

"""
def getAllUsers():
    with Session(engine) as session:  
        statement = select(Users)  
        results = session.exec(statement)  
        return results.fetchall()

"""
                                                RECIPES
"""


"""
    createRecipe
    Insert une nouvelle ligne dans la table Recipes

"""
def createRecipe(name, description, id_user):
    recipe = Recipes(name=name, description=description, fk_user=id_user)

    with Session(engine) as session:
        session.add(recipe)
        session.commit()


"""
    getRecettesByUserId
    Retourne toutes les recettes lies a un utilisateur via l'id en input

"""
def getRecettesByUserId(user_id):
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.fk_user == user_id)
        results = session.exec(statement)

        return results.fetchall()
    

"""
    getRecettesById
    Retourne une recette via son id
"""
def getRecettesById(recipe_id):
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.id == recipe_id)
        results = session.exec(statement)

        return results.fetchall()
    

"""
                                                AISLES
"""


"""
    createAisle
    Insert une nouvelle ligne dans la table Aisles

"""
def createAisle(name):
    aisle = Aisles(name=name)

    with Session(engine) as session:
        session.add(aisle)
        session.commit()


"""
                                                INGREDIENTS
"""


"""
    createIngredient
    Insert une nouvelle ligne dans la table Aisles

"""
def createIngredient(name, quantity, unit, id_aisle, id_recipe):
    ingredient = Ingredients(name=name, quantity=quantity, unit=unit, fk_recipe=id_recipe, fk_aisle=id_aisle)

    with Session(engine) as session:
        session.add(ingredient)
        session.commit()

"""
    createMultipleIngredients
    Insert plusieurs ligne dans la table ingredients toutes ayant la meme fk_recipe

"""
def createMultipleIngredients(ingredientsList, id_recipe):
    with Session(engine) as session:
        ingredients_to_add = []
        for ingredient_data in ingredientsList:
            name = ingredient_data['name']
            quantity = ingredient_data['quantity']
            unit = ingredient_data['unit']
            id_aisle = ingredient_data['id_aisle']
            
            ingredient = Ingredients(name=name, quantity=quantity, unit=unit, fk_recipe=id_recipe, fk_aisle=id_aisle)
            ingredients_to_add.append(ingredient)
        
        session.add_all(ingredients_to_add)
        session.commit()


"""
    getIngredientsByRecipeIds
    Retournes tous les ingredients lies a la liste de recipe.id en input

"""
def getIngredientsByRecipeIds(recipe_ids):
    with Session(engine) as session:
        statement = select(Ingredients).where(Ingredients.fk_recipe.in_(recipe_ids))
        results = session.exec(statement)

        return results.fetchall()
    





def main():
    recipe_ids_to_search = [1, 2]
    ingredients_related_to_recipes = getIngredientsByRecipeIds(recipe_ids_to_search)

    if ingredients_related_to_recipes:
        print("Ingrédients associés aux recettes sélectionnées :")
        for ingredient in ingredients_related_to_recipes:
            print(f"{ingredient.name}, Quantite: {ingredient.quantity}{ingredient.unit}")

if __name__ == "__main__":
    main()