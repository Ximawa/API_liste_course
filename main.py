from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

from functions import *

"""
                                                BASEMODEL to declare request body
"""

class Aisle(BaseModel):
    name: str

class User(BaseModel):
    login: str
    pswd: str 

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str
    rayon: int

class Recipe(BaseModel):
    name: str
    description: str
    ingredients: List[Ingredient]
    id_user: int

class GroceriesList(BaseModel):
    id_recipes: List[int]

class DelUsers(BaseModel):
    id_user: int

class DelRecipes(BaseModel):
    id_recipe: int

class DelAisle(BaseModel):
    id_aisle: int

"""
                                                ROUTES
"""


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/rayon")
async def getAllRayon():
    return getAllAisles()


@app.get("/users")
async def getUsers():
    return getAllUsers()


@app.get("/recette/{recetteID}")
async def getRecipeByID(recetteID):
    return getIngredientsByRecipeId(recetteID)


@app.post("/addUser")
async def addUser(user: User):
    if (checkLoginAvaible(user.login)):
        u = createUser(user.login, user.pswd)
        return {"status": "Success", "userID" : u.id}
    else:
        return {"error": "Le login n'est pas disponible"}


@app.post("/addAisle")
async def addAisle(aisle: Aisle):
    if (checkAisleNameAvaible(aisle.name)):
        createAisle(aisle.name)
        return {"status": "Success"}
    else:
        return {"error": "Le Rayon existe deja"}

@app.post("/addRecipe")
async def addRecipe(rec: Recipe):
    if (checkRecipeNameAvaible(rec.id_user,rec.name)):
        recipe = createRecipe(rec.name, rec.description, rec.id_user)
        createMultipleIngredients(rec.ingredients, recipe.id)
        return {
            "status": "Success",
            'idRecette': recipe.id
        }
    else:
        return {"error: la recette existe deja"}


@app.post("/listeCourse")
async def groceriesList(list: GroceriesList):
    return getIngredientsByRecipeIds(list.id_recipes)

@app.post("/deleteUser")
async def deleteUser(user: DelUsers):
    deleteUsers(user.id_user)
    return {"Status": "Success"}

# Ne fonctionne pas
@app.post("/deleteRecipe")
async def deleteRecipe(recipe: DelRecipes):
    deleteRecipes(recipe.id_recipe)
    return {"Status": "Success"}

# Ne fonctionne pas
@app.post("/deleteAisle")
async def deleteAisles(aisle: DelAisle):
    deleteAisles(aisle.id_aisle)
    return {"Status": "Success"}