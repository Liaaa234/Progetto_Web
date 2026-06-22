from fastapi import APIRouter
from sqlmodel import select  #Importa la funzione select dalla libreria SQLModel

from app.models.registration import Registration  #Importa il modello Registration dal modulo app.models.registration
from app.data.db import SessionDep  #importa SessionDep dal file della configurazione del database

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