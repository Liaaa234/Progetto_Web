from fastapi import APIRouter, HTTPException
from sqlmodel import select


from app.models.user import User
from app.data.db import SessionDep

router = APIRouter(prefix="/users", tags=["users"])
@router.get("/")
def get_users(session: SessionDep)->list[User]:#fastapi crea una sessione del database per passarla alla funzione che restituisce una lista
    """Return the list of all existing users."""
    users = session.exec(select(User)).all()#query sql seleziona tutti gli utenti della tabella user
    return users

@router.post("/", status_code=201)
def create_user(user: User, session: SessionDep)->User:
    """Create a new user."""
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/users/{username}")
def get_user(username: str, session: SessionDep)->User:
    """Return the user."""
    user = session.exec(select(User).where(User.username == username)).first()
    if user in None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
