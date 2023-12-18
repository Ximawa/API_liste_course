from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

from functions import *


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

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/rayon")
async def getAllRayon():
    return getAllAisles()


@app.post("/addUser")
async def addUser(user: User):
    # TODO  Verif si login est libre
    u = createUser(user.login, user.pswd)

    return {"status": "Success", "userID" : u.id}

@app.get("/users")
async def getAUsers():
    return getAllUsers()


@app.post("/addAisle")
async def addAisle(aisle: Aisle):
    # TODO  Verif si name est libre
    createAisle(aisle.name)

    return {"status": "Success"}



@app.post("/addRecipe")
async def addRecipe(rec: Recipe):
    recipe = createRecipe(rec.name, rec.description, rec.id_user)

    createMultipleIngredients(rec.ingredients, recipe.id)

    return {
        "status": "Success",
        'idRecette': recipe.id
    }


@app.get("/recette/{recetteID}")
async def getRecetteByID(recetteID):
    return getIngredientsByRecipeId(recetteID)

@app.post("/listeCourse")
async def getGroceriesList(list: GroceriesList):
    print(f"Recette demander : {list.id_recipes}")
    return getIngredientsByRecipeIds(list.id_recipes)
