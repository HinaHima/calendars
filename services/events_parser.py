from sqlalchemy import text, create_engine
from datetime import datetime,timedelta
from calendars import db
from calendars.models import Event
import calendars.config as Config

class EventsParser:
    @staticmethod
    def get_events(args):
        try:
            # Prepare query (sorry, i dont belive in alchemy)
            # SELECT FROM
            query_str = "SELECT * FROM events WHERE 1 = 1 "
            #
            # WHERE
            if 'delivery_id' in args: query_str += f" AND delivery_id = '{args['delivery_id']}' "
            if 'delivery_type' in args: query_str += f" AND delivery_type = '{args['delivery_type']}' "
            if 'delivery_name' in args: query_str += f" AND delivery_name = '{args['delivery_name']}' "
            if 'id' in args: query_str += f" AND external_id = '{args['id']}' "
            if 'internal_id' in args: query_str += f" AND id = {args['internal_id']} "
            #
            if 'is_clicked' in args: 
                if 'is_clicked' == True: query_str += f" AND (ics_clicks != 0 OR google_clicks != 0) "
                else: query_str += f" AND (ics_clicks = 0 AND google_clicks = 0) "
            #
            if 'created_at_begin' in args: query_str += f" AND created_at >= '{args['created_at_begin']}' "
            if 'created_at_end' in args: query_str += f" AND created_at <= '{args['created_at_begin']}' "
            #
            # LIMITS AND PAGINATION
            if 'limit' in args: query_str += f" LIMIT {args['limit']} OFFSET {args['offset']} "
            if 'page_num' in args:                 
                query_str += f" LIMIT {args['page_size']} OFFSET {(int(args['page_num']) - 1) * int(args['page_size'])} "


            # Execute query and get data
            events_list = {"events": []}           
            engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
            with engine.connect() as connection:
                rows = connection.execute(text(query_str)).all()
                for row in rows:
                    e = {}
                    #
                    e["id"] = row['external_id']
                    e["internal_id"] = row['id']
                    e["delivery_id"] = row['delivery_id']
                    e["delivery_type"] = row['delivery_type']
                    e["delivery_name"] = row['delivery_name']
                    e["summary"] = row['summary']
                    e["location"] = row['location']
                    e["description"] = row['description']
                    e["start"] = row['start_at'].strftime('%Y-%m-%dT%H:%M:%S')
                    e["end"] = row['end_at'].strftime('%Y-%m-%dT%H:%M:%S')
                    e["ttl"] = row['ttl']
                    e["ics_clicks"] = row['ics_clicks']
                    e["google_clicks"] = row['google_clicks']
                    e["ics"] = 'https://' + Config.BASE_URL + '/i/' + row['hash']
                    e["ics_short"] = 'https://' + Config.SHORT_URL + '/i/' + row['hash']
                    e["google"] = 'https://' + Config.BASE_URL + '/g/' + row['hash']
                    e["google_short"] = 'https://' + Config.SHORT_URL + '/g/' + row['hash']
                    e["created_at"] = row['created_at'].strftime('%Y-%m-%dT%H:%M:%S')
                    e["updated_at"] = row['updated_at'].strftime('%Y-%m-%dT%H:%M:%S')
                    #
                    events_list["events"].append(e)


            # Parse data
            if ('fields' in args):
                fields = args['fields'].split(',')
                for event in events_list['events']:
                    for key in event.keys():
                        if key not in fields: event[key] = None
            #        
            for event in events_list['events']:
                for key, value in event.copy().items():
                    if value is None:
                        del event[key]    
            
            
            # Return data
            return events_list
        except Exception as e:
            raise EventsParserException(str(e))

    @staticmethod        
    def save_events(company_id, data):
        try:
            res = {"events":[]}
            #
            for event in data["events"]:
                # Save event
                new_event = Event()
                #               
                new_event.company_id=company_id,                                        
                if ('id' in event): new_event.external_id=event["id"]
                if ('delivery' in data and 'id' in data["delivery"]): new_event.delivery_id=data["delivery"]["id"]
                if ('delivery' in data and 'type' in data["delivery"]): new_event.delivery_type=data["delivery"]["type"]
                if ('delivery' in data and 'name' in data["delivery"]): new_event.delivery_name=data["delivery"]["name"]
                new_event.summary=event["summary"]
                if ('description' in event): new_event.description=event["description"]
                if ('location' in event): new_event.location=event["location"]                
                new_event.start_at=event["start"]
                new_event.end_at=event["end"]                                      
                if ('ttl' in event): new_event.ttl=event["ttl"]
                #
                db.session.add(new_event)
                db.session.commit()

                # Get and save hash
                new_event.hash = EventsParser.get_hash_by_id(new_event.id)
                db.session.commit()

                # Add to result
                res["events"].append({
                    "id": new_event.external_id, 
                    "internal_id": new_event.id, 
                    "ics": 'https://' + Config.BASE_URL + '/i/' + new_event.hash, 
                    "ics_short": 'https://' + Config.SHORT_URL + '/i/' + new_event.hash, 
                    "google": 'https://' + Config.BASE_URL + '/g/' + new_event.hash,
                    "google_short": 'https://' + Config.SHORT_URL + '/g/' + new_event.hash
                    })
            #
            return res
        except Exception as e:
            raise EventsParserException(str(e))

    @staticmethod
    def get_hash_by_id(id: int) -> str:
        string = ''
        r_count = 7
        shift_count = 5
        i = 0
        charset = "Z123456789ABCDEFGHJKLMNPQRTUVWXY";
        #
        r = []
        #
        if ((id & 0x07FFFFFFFF) != id): 
            return None
        #
        while i < r_count:
            r.append(id & 0x0000001F)
            id = id >> shift_count
            i += 1
        #
        string += charset[r[1]]
        string += charset[r[3]]
        string += charset[r[4]]
        string += charset[r[0]]
        string += charset[r[6]]
        string += charset[r[2]]
        string += charset[r[5]]
        #
        return string

    @staticmethod
    def get_event_by_hash(event_hash: str, event_type: str) -> Event:
        try:
            event = Event.query.filter_by(hash=event_hash).first()
            if (event == None): raise Exception("Cant find event dy hash.")
            #
            if (event.ttl != 0 and event.ttl != None):
                ttl = event.created_at + timedelta(minutes=event.ttl)
                if (ttl < datetime.now()): raise Exception("Event TTL.")
            #
            if (event_type == 'ics'): event.ics_clicks += 1
            else: event.google_clicks += 1
            #
            db.session.commit()
            # 
            return event
        except Exception as e:
            raise EventsParserException(str(e))

class EventsParserException(Exception):
    pass