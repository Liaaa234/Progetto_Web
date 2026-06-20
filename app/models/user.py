from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):#classe base dei modelli del database
    username:str=Field(primary_key=True)#chiave primaria della tabella
    name: str
    email:str

