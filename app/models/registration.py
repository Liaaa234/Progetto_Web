from sqlmodel import SQLModel, Field

class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username")
    event_id: int = Field(primary_key=True, foreign_key="event.id")

# struttura dati per Registration

class Registration(SQLModel):     # attributi comuni
    username: str
    event_id: int
class RegistrationPublic(Registration):   # usata nelle GET
    pass