from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event,EventEncoder
from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer
import json

router = APIRouter()

events_data = EventFileManager.read_events_from_file()
    
@router.get("/events", response_model=List[Event])
async def get_all_events():
    
    return events_data


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    filtered_events = events_data
    
    # Apply filters
    if date:
        filtered_events = [event for event in filtered_events if event.get('date') == date]
    if organizer:
        filtered_events = [event for event in filtered_events if event.get('organizer') == organizer]
    if status:
        filtered_events = [event for event in filtered_events if event.get('status') == status]
    if event_type:
        filtered_events = [event for event in filtered_events if event.get('event_type') == event_type]
    
    return filtered_events


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    
    for event in events_data:
        if(type(event) == dict): existing_event_id = event.get('id') 
        else: existing_event_id=event.id
        if existing_event_id == event_id:
            return event
    raise HTTPException(status_code=404,detail="Item not found")


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    for existing_event in events_data:
        if(type(existing_event) == dict): existing_event_id = existing_event.get('id') 
        else: existing_event_id=existing_event.id
        print(type(existing_event))
        if existing_event_id == event.id:
            raise HTTPException(status_code=409, detail="Item already exists")

    events_data.append(event)
    EventFileManager.write_events_to_file(events_data)
    return event


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    existing_event:dict
    for existing_event in events_data:
        if existing_event.get('id') == event_id:

            existing_event.update(event)
            EventFileManager.write_events_to_file(events_data)
            return existing_event
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    global events_data

    event_index = None
    for index, event in enumerate(events_data):
        if event.get('id') == event_id:
            event_index = index
            break
    if event_index is not None:
        del events_data[event_index]
        EventFileManager.write_events_to_file(events_data)
        return {"message": "Event deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    return EventAnalyzer.get_joiners_multiple_meetings_method(events_data)
