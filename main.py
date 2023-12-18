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
    # TODO  Verif si name est libre
    createAisle(aisle.name)

    return {"status": "Success"}


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

