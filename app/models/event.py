#STRUTTURA DATI PER L'OGGETTO EVENTO

from sqlmodel import Field, SQLModel
from datetime import datetime

class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  #generato automaticamente dal database
    title: str
    description: str
    date: datetime
    location: str