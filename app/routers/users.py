from fastapi import APIRouter, HTTPException
from sqlmodel import select


from app.models.user import User, UserDB, UserPublic, CreateUser
from app.data.db import SessionDep

router = APIRouter(prefix="/users", tags=["users"])
@router.get("/")
def get_users(session: SessionDep)->list[UserPublic]:#fastapi crea una sessione del database per passarla alla funzione che restituisce una lista
    """Return the list of all existing users."""
    users = session.exec(select(UserDB)).all()#query sql seleziona tutti gli utenti della tabella user
    return users

@router.post("/", status_code=201)
def create_user(user: CreateUser, session: SessionDep)->UserPublic:
    """Create a new user."""
    existing_user = session.exec(
        select(UserDB).
        where(UserDB.username == user.username)
    ).first()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    user_db=UserDB.model_validate(user)#prendi i campi di user, controllali/convertli secondo il modello UserDB, e costruisci un nuovo oggetto UserDB
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@router.get("/{username}")
def get_user(username: str, session: SessionDep)->UserPublic:
    """Return the user."""
    user = session.exec(
        select(UserDB).
        where(UserDB.username == username)
    ).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/")
def delete_users(session: SessionDep)-> dict:
    """Delete all users."""
    users = session.exec(select(UserDB)).all()
    for user in users:
        session.delete(user)
    session.commit()
    return {"message": "All Users successfully deleted"}

@router.delete("/{username}")
def delete_user(username: str, session: SessionDep)-> dict:
    """Delete one user."""

    user = session.exec(
        select(UserDB)
        .where(UserDB.username == username)
    ).first()

    if user is None :
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {
        "message":"User successfully deleted"
    }