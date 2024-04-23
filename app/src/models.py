from typing import List, Optional
from pydantic import BaseModel
from json import JSONEncoder


class Organizer(BaseModel):
    name:str
    email: str


class Joiner(BaseModel):
    name: str
    email:str
    country: str


class Event(BaseModel):
    id: Optional[int]
    name:str
    date: str
    organizer: Organizer
    status: str
    type:str
    joiners: Optional[List[Joiner]]
    location:str
    max_attendees: int

    


class EventEncoder(JSONEncoder):
    def default(self,o):
        return o.__dict__