from fastapi import APIRouter
from sqlmodel import select

from app.models.user import User
from app.data.db import SessionDep

router = APIRouter(prefix="/users", tags=["users"])
@router.get("")
def get_users(session: SessionDep)->list[User]:#fastapi crea una sessione del database per passarla alla funzione che restituisce una lista
    users = session.exec(select(User)).all()#query sql seleziona tutti gli utenti della tabella user
    return users
