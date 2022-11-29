from marshmallow import ValidationError, validates, validates_schema, Schema, fields as f
from marshmallow.validate import Length, Range

# --- VALIDATION SCHEMES ----------------------------------------------------------------------------------------------------
class DeliverySchema(Schema):
    id = f.String(required=False, allow_none=True, validate=Length(max=36, error="Must be not more than 36 characters."))
    type = f.String(required=False, allow_none=True, validate=Length(max=200, error="Must be not more than 200 characters."))
    name = f.String(required=False, allow_none=True, validate=Length(max=500, error="Must be not more than 500 characters."))

class EventsSchema(Schema):
    id = f.String(required=False, allow_none=True, validate=Length(max=36, error="Must be not more than 36 characters."))
    summary = f.String(required=True, allow_none=False, validate=Length(max=500, error="Must be not more than 500 characters."))
    location = f.String(required=False, allow_none=True, validate=Length(max=500, error="Must be not more than 500 characters."))
    description = f.String(required=False, allow_none=True, validate=Length(max=1000, error="Must be not more than 1000 characters."))
    start = f.DateTime(required=True, allow_none=False)
    end = f.DateTime(required=True, allow_none=False)
    ttl = f.Integer(required=False, allow_none=True, validate=Range(min=0, error="Can not be negative."))

class GetEventsSchema(Schema):
    delivery_id = f.String(required=False, allow_none=True, validate=Length(max=36, error="Should be not more than 36 characters."))
    delivery_type = f.String(required=False, allow_none=True, validate=Length(max=200, error="Should be not more than 200 characters."))
    delivery_name = f.String(required=False, allow_none=True, validate=Length(max=500, error="Should be not more than 500 characters."))
    id = f.String(required=False, allow_none=True, validate=Length(max=36, error="Should be not more than 36 characters."))    
    internal_id = f.Integer(required=False, allow_none=True, validate=Range(min=0, error="Can not be negative."))    
    created_at_begin = f.DateTime(required=False, allow_none=True)
    created_at_end = f.DateTime(required=False, allow_none=True)
    fields = f.String(required=False, allow_none=True)
    offset = f.Integer(required=False, allow_none=True, validate=Range(min=0, error="Can not be negative."))
    limit = f.Integer(required=False, allow_none=True, validate=Range(min=1, error="Can not be negative or zero."))
    page_num = f.Integer(required=False, allow_none=True, validate=Range(min=1, error="Can not be negative or zero."))
    page_size = f.Integer(required=False, allow_none=True, validate=Range(min=1, error="Can not be negative or zero."))
    is_clicked = f.Boolean(required=False, allow_none=True)
    
    @validates_schema    
    def validate_params(self, data, **kwargs):
        # Offset anf Limit
        if ( ( ('offset' in data) and ('limit' not in data) ) or ( ('limit' in data) and ('offset' not in data) ) ):
            raise ValidationError("Offset and limit must be both presented.")

        # Page Num and Page Size
        if ( ( ('page_num' in data) and ('page_size' not in data) ) or ( ('page_size' in data) and ('page_num' not in data) ) ):
            raise ValidationError("page_num and page_size must be both presented.")

        # Offset anf Limit AND Page Num and Page Size
        if  (('offset' in data or 'limit' in data) and ('page_num' in data or 'page_size' in data)):
            raise ValidationError("You must use page_num and page_size OR limit and offset.")
        if  (('page_num' in data or 'page_size' in data) and ('offset' in data or 'limit' in data)):
            raise ValidationError("You must use page_num and page_size OR limit and offset.")

        # Fields
        if ('fields' in data):
            available_fields = ["id", "internal_id", "delivery_id", "delivery_type", "delivery_name", "summary", "location",
                                "description", "start", "end", "ttl", "ics_clicks", "google_clicks", "created_at",
                                "updated_at", "ics", "ics_short", "google", "google_short"]
            fields = data['fields'].split(',')
            for field in fields:
                if field not in available_fields: raise ValidationError("Wrong fields argument value.")

class SaveEventsSchema(Schema):
    delivery = f.Nested(DeliverySchema, required=False, allow_none=True)
    events = f.Nested(EventsSchema, many=True, required=True)


# ---------------------------------------------------------------------------------------------------------------------------
class EventsValidator():
    @staticmethod
    def save_events(data):
        try:
            res = SaveEventsSchema().validate(data)
            if (res): raise EventsValidatorException(str(res))
        except ValidationError as e:
            raise EventsValidatorException(f"{e.messages}")
        except Exception as e:
            raise EventsValidatorException(str(e))
    
    @staticmethod
    def get_events(data):
        try:
            res = GetEventsSchema(partial=True).validate(data)
            if (res): raise EventsValidatorException(str(res))
        except ValidationError as e:
            raise EventsValidatorException(f"{e.messages}")
        except Exception as e:
            raise EventsValidatorException(str(e))            

class EventsValidatorException(Exception):
    pass
