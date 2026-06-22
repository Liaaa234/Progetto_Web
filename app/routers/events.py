from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.data.db import SessionDep
from app.models.event import Event, EventCreate, EventDB, EventPublic

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")    #prendiamo la lista di tutti gli eventi
def get_all_events(session: SessionDep) -> list[EventPublic]: #comunichiamo con il database
    """Return the list of all events."""
    events = session.exec(select(EventDB)).all()  #prende la lista di tutti i libri
    return events

@router.get("/{id}")    #prendiamo UNO specifico evento
def get_event_by_id(session: SessionDep) -> EventPublic:
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