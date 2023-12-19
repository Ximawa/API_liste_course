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
    Insert une nouvelle ligne dans la table Users avec le login et mdp en claire recu

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
    Retourne tout les utilisateurs present en BDD

"""
def getAllUsers():
    with Session(engine) as session:  
        statement = select(Users)  
        results = session.exec(statement)  
        return results.fetchall()

"""

    checkLoginAvaible 
    Vérifie si le nom de l'utilisateur existe déja

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
    Supprime l'utilisateur

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
    Insert une nouvelle ligne dans la table Recipes

"""
def createRecipe(name, description, id_user):
    recipe = Recipes(name=name, description=description, fk_user=id_user)

    with Session(engine) as session:
        session.add(recipe)
        session.commit()

        session.refresh(recipe)
        return recipe


"""
    getRecettesByUserId
    Retourne toutes les recettes lies a un utilisateur via l'id en input

"""
def getRecipesByUserId(user_id):
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.fk_user == user_id)
        results = session.exec(statement)

        return results.fetchall()
    

"""
    getRecettesById
    Retourne une recette via son id
"""
def getRecipeById(recipe_id):
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.id == recipe_id)
        results = session.exec(statement)

        return results.fetchall()
    

"""

checkRecipeAvaible 
Vérifie si le nom de la recette d'un utilisateur existe déja 

"""
def checkRecipeNameAvaible(user_id,name):
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.name == name).where(Recipes.fk_user == user_id)
        results = session.exec(statement)
        if results.fetchall() == []:
            return True
        else:
            return False
        
"""

    deleteRecipes
    Supprime une recette

"""

def deleteRecipes(id_recipe):
    deleteIngredientFromRecipe(id_recipe)
    with Session(engine) as session:
        statement = select(Recipes).where(Recipes.id == id_recipe)
        results = session.exec(statement)
        recipe = results.fetchall()
    
        session.delete(recipe)
        session.commit()


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

        session.refresh(aisle)
        return aisle
    

"""
    getAllAisles
    Retourne tout les rayons present en BDD

"""
def getAllAisles():
    with Session(engine) as session:  
        statement = select(Aisles)  
        results = session.exec(statement)  
        return results.fetchall()

"""

checkAisleNameAvaible 
Vérifie si le nom de la recette d'un utilisateur existe déja 

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
    Supprime un rayon

"""

def deleteAisles(id_aisle):
    with Session(engine) as session:
        statement = select(Aisles).where(Aisles.id == id_aisle)
        results = session.exec(statement)
        aisle = results.fetchall()
        session.delete(aisle)
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

        session.refresh(ingredient)
        return ingredient

"""
    createMultipleIngredients
    Insert plusieurs ligne dans la table ingredients toutes ayant la meme fk_recipe

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
    getIngredientsByRecipeIds
    Prend en input une liste d'id de recette et retourne les ingredients neccesaire en addionant la quantite des ingredients ayant le meme nom et unite

"""
def getIngredientsByRecipeIds(recipe_ids):
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
    getIngredientsByRecipeIds
    Retournes tous les ingredients lies a la recipe.id en input

"""
def getIngredientsByRecipeId(recipe_id):
    with Session(engine) as session:
        statement = select(Ingredients).where(Ingredients.fk_recipe == recipe_id)
        results = session.exec(statement)

        return results.fetchall()
    

"""

    deleteIngredientFromRecipe
    Supprime les ingredients d'une recette

"""

def deleteIngredientFromRecipe(id_recipe):
    with Session(engine) as session:
        ingredients_to_delete = session.exec(
            delete(Ingredients).where(Ingredients.fk_recipe == id_recipe)
        ).all()

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