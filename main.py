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

class UpdateUser(BaseModel):
    id_user: int
    login: str
    pswd: str 

class UpdateAisle(BaseModel):
    id_aisle: int
    name: str

class UpdateRecipe(BaseModel):
    id_user: int
    id_recipe: int
    name: str
    description: str
    ingredients: List[Ingredient]


"""
                                                ROUTES
"""

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/aisle")
async def getAllAisles():
    return getAisles()


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
    return getMultiplesIngredientsByRecipeIds(list.id_recipes)

@app.post("/deleteUser")
async def deleteUsers(user: DelUsers):
    deleteUser(user.id_user)
    return {"Status": "Success"}


@app.post("/deleteRecipe")
async def deleteRecipes(recipe: DelRecipes):
    deleteRecipe(recipe.id_recipe)
    return {"Status": "Success"}


@app.post("/deleteAisle")
async def deleteAisles(aisle: DelAisle):
    deleteAisle(aisle.id_aisle)
    return {"Status": "Success"}

@app.post("/updateUser")
async def updateUsers(user: UpdateUser):
    updateUser(user.id_user, user.login, user.pswd)
    return {"Status": "Success"}

@app.post("/updateAisle")
async def updateAisles(aisle: UpdateAisle):
    updateAisle(aisle.id_aisle, aisle.name)
    return {"Status": "Success"}

@app.post("/updateRecipe")
async def updateRecipes(rec: UpdateRecipe):
    if (checkRecipeNameAvaible(rec.id_user,rec.name)):
        updateRecipe(rec.id_recipe, rec.name, rec.description)
        updateIngredients(rec.ingredients, rec.id_recipe)
        return {
            "status": "Success",
        }
    else:
        return {"error: la recette existe deja"}