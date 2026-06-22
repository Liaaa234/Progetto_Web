from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.data.db import SessionDep
from app.models.event import Event

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")    #prendiamo la lista di tutti gli eventi
def get_all_events(session: SessionDep) -> list[Event]: #comunichiamo con il database
    """Return the list of all events."""
    events = session.exec(select(Event)).all()  #query
    return events

@router.get("/{id}")    #prendiamo UNO specifico evento
def get_event_by_id(session: SessionDep) -> Event: