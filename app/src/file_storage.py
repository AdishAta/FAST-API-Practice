import json
from .models import Event,EventEncoder
from typing import List


class EventFileManager:
    FILE_PATH = 'event.json'
    

    @classmethod
    def read_events_from_file(cls):
        try:
            with open(cls.FILE_PATH) as f:
                events = json.load(f)
        except FileNotFoundError:
            events = []
        except json.JSONDecoderError:
            events = []
        return events

    @classmethod
    def write_events_to_file(cls, events):
        with open(cls.FILE_PATH, 'w') as file:
            json.dump(events, file, indent=4,cls=EventEncoder)       
    