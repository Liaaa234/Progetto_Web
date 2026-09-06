#STRUTTURA DATI PER L'OGGETTO EVENTO

from typing import Annotated
from sqlmodel import Field, SQLModel
from datetime import datetime

class Event(SQLModel):      #classe radice e avrà gli attributi comuni per tutte le altre classi Event
    title: str
    description: str
    date: datetime
    location: str

class EventCreate(Event):   #creiamo la classe da usare nelle POST
    pass    #i campi sono ereditati da Event quindi lascio vuoti i campi

class EventDB(Event, table=True):   #creiamo il collegamento tra il nostro codice e il database
    __tablename__ = "event"     #nome classe nel database
    id: int = Field(default=None, primary_key=True)

class EventPublic(Event):   #usata nelle GET
    id: int