from sqlalchemy import table
from sqlmodel import Field, SQLModel

class User(SQLModel):#classe base dei modelli del database
    username:str
    name: str
    email:str
class CreateUser(User):
    pass
class UserDB(User, table=True):#classe che rappresenta la tabella del database
    username:str=Field(default=None, primary_key=True)
class UserPublic(User):
    pass


