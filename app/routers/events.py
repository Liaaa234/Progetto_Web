from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.data.db import SessionDep
from app.models.event import Event,EventCreate, EventDB, EventPublic
from app.models.user import UserDB
from app.models.registration import Registration

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")    #prendiamo la lista di tutti gli eventi
def get_all_events(session: SessionDep) -> list[EventPublic]: #comunichiamo con il database
    """Return the list of all events."""
    events = session.exec(select(EventDB)).all()  #query
    return events

@router.get("/{id}")    #prendiamo UNO specifico evento
def get_event_by_id(
        id: int,
        session: SessionDep
) -> EventPublic:
    """Return the event with the given id."""
    event = session.get(EventDB, id)  #cerchiamo nella tabella l'evento con quell'id

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")  #gestiamo l'errore in caso l'id non esista

    return event

@router.post("/")   #API per creare nuovi eventi
def create_event(
        session: SessionDep,
        event: EventCreate
):
    """Create a new event."""
    event_entry = EventDB.model_validate(event)
    session.add(event_entry)
    session.commit()    #aggiorniamo l'oggetto e rendiamo effettive le modifiche
    return event_entry

@router.put("/{id}")
def replace_event(
        id: int,
        session: SessionDep,
        new_event: EventCreate
):
    """Replace the event with the given id."""
    event = session.get(EventDB, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location
    session.add(event)
    session.commit()
    return event



#API post
@router.post("/events/{id}/register")
def register_to_event(
    id: int,
    username: str,
    session: SessionDep
):

    event = session.get(EventDB, id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Evento non trovato"
        )

    user = session.get(UserDB, username)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Utente non trovato"
        )

    registration = session.get(
        Registration,
        (username, id)
    )

    if registration is not None:
        raise HTTPException(
            status_code=400,
            detail="Utente già registrato all'evento"
        )

    registration = Registration(
        username=username,
        event_id=id
    )

    session.add(registration)
    session.commit()

    return {"message": "Registrazione effettuata"}



#API delete event
@router.delete("/events/{id}")
def delete_event(
    id: int,
    session: SessionDep
):

    event = session.get(EventDB, id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Evento non trovato"
        )

    session.delete(event)
    session.commit()

    return {"message": "Evento eliminato"}



#API delete all events
@router.delete("/events")
def delete_all_events(
    session: SessionDep
):

    events = session.exec(
        select(EventDB)
    ).all()

    for event in events:
        session.delete(event)

    session.commit()

    return {"message": "Tutti gli eventi eliminati"}