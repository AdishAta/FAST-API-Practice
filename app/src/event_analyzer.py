from .models import Event,EventEncoder
from typing import List

class EventAnalyzer:
    @classmethod
    def get_joiners_multiple_meetings_method(cls,events:List[Event]):
        attendees = {}
        for event in events:
            
            for joiner in event.get('joiners'):
                email = joiner.get('email')
                if(email in attendees):
                    attendees[email] = {'joiner':attendees[email].get('joiner'),'count':attendees[email].get('count')+1}
                else: 
                    attendees[email] = {'joiner' : joiner, 'count':1}

        output = [attendees[email].get('joiner') for email in attendees if attendees[email].get('count') >= 2]
        return output if output!= [] else "No joiners attending at least 2 meetings"