from fastapi import APIRouter, HTTPException
from sqlmodel import select  #Importa la funzione select dalla libreria SQLModel

from app.models.registration import Registration  #Importa il modello Registration dal modulo app.models.registration
from app.data.db import SessionDep  #importa SessionDep dal file della configurazione del database
from app.models.user import UserDB
from app.models.event import EventDB

#Inizializzo un'istanza APIRouter e la salvo nella variabile router
router = APIRouter(prefix="/registrations", tags=["registrations"])

@router.get("/")
def get_registrations(
        session: SessionDep
) -> list[Registration]:
    """Returns a list of all registrations"""

    registrations = session.exec(
        select(Registration)
    ).all()

    return registrations

@router.delete("/")
def delete_registration(
        username: str,
        event_id: int,
        session: SessionDep
) ->dict:
    """Deletes a registration"""

    event = session.get(EventDB, event_id)

    if  event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    user = session.get(UserDB, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    registration = session.exec(
        select(Registration)
        .where(
            Registration.username == username,
            Registration.event_id == event_id
        )
    ).first()

    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(registration)
    session.commit()

    return {
        "message": "Registration successfully deleted"
    }