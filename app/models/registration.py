from sqlmodel import SQLModel, Field

# Creo una tabella di associazione che collega gli utenti agli eventi
class Registration(SQLModel, table=True):
    # Chiave esterna collegata alla tabella 'user'
    username: str = Field(primary_key=True, foreign_key="user.username")
    # Chiave esterna collegata alla tabella 'event'
    event_id: int = Field(primary_key=True, foreign_key="event.id")

