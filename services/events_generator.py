import urllib.parse
from icalendar import Calendar as iCalendar, Event as iEvent, vText
from calendars.models import Event

class EventsGenerator:
    @staticmethod
    def get_ics_file(event: Event) -> bytes:
        try:
            e = iEvent()
            e.add('summary', event.summary)
            e.add('description', event.description)
            e['dtstart'] = event.start_at
            e['dtend'] = event.end_at
            e['location'] = vText(event.location)
            #
            c = iCalendar()
            c.add('attendee', '')
            c.add_component(e)        
            #
            return c.to_ical()
        except Exception as e:
            raise EventsGeneratorException(str(e))
    
    @staticmethod
    def get_google_link(event: Event) -> str:
        try:
            url = "https://www.google.com/calendar/render?action=TEMPLATE&"
            url += "text=" + urllib.parse.quote(event.summary) + "&"
            if (event.description != None): url += "details=" + urllib.parse.quote(event.description) + "&"
            if (event.location != None): url += "location=" + urllib.parse.quote(event.location) + "&"
            url += "dates=" + event.start_at.strftime('%Y%m%dT%H%M%S') + "%2F" + event.end_at.strftime('%Y%m%dT%H%M%S')
            #      
            return url
        except Exception as e:
            raise EventsGeneratorException(str(e))
                
class EventsGeneratorException(Exception):
    pass
