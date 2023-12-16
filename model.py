from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, ForeignKey


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    login: str
    pswd: str

class Aisles(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Recipes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    fk_user: Optional[int] = Field(default=None, foreign_key="users.id")

class Ingredients(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    quantity: int
    unit: str
    fk_recipe: Optional[int] = Field(default=None, foreign_key="recipes.id")
    fk_aisle: Optional[int] = Field(default=None, foreign_key="aisles.id")





def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():
    create_db_and_tables()

if __name__ == "__main__":
    main()