from fastapi import APIRouter, HTTPException
from sqlmodel import select  #Importa la funzione select dalla libreria SQLModel

from app.models.registration import Registration  #Importa il modello Registration dal modulo app.models.registration
from app.data.db import SessionDep  #importa SessionDep dal file della configurazione del database
from app.models.user import UserDB
from app.models.event import EventDB

#Inizializzo un'istanza APIRouter e la salvo nella variabile router
router = APIRouter(prefix="/registrations", tags=["registrations"])

@router.get("/")  #prendiamo la lista di tutte le registrazioni
def get_registrations(
        session: SessionDep
) -> list[Registration]:
    """Returns a list of all registrations"""

    registrations = session.exec(
        select(Registration)
    ).all()

    return registrations

@router.delete("/")  #eliminazione di una singola registrazione
def delete_registration(
        username: str,
        event_id: int,
        session: SessionDep
) ->dict:
    """Deletes a registration"""

    # Cerco l'evento nel database tramite la sua chiave primaria
    event = session.get(EventDB, event_id)
    # Se l'evento non esiste, blocco la richiesta e restituisco un errore HTTP 404
    if  event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    # Se l'utente non esiste, restituisco un errore 404

    user = session.get(UserDB, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Cerco specifica registrazione
    registration = session.exec(
        select(Registration)
        .where(
            Registration.username == username,
            Registration.event_id == event_id
        )
    ).first()  # .first() prende il primo risultato trovato

    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")
    # Se la registrazione non esiste, restituisco un errore 404

    # Se tutti i controlli sono superati, procedo con l'eliminazione
    session.delete(registration)  # Eliminazione
    session.commit()  # Salvataggio delle modifiche nel database

    return {
        "message": "Registration successfully deleted"
    }