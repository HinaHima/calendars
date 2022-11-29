from io import BytesIO
from flask import request, redirect, send_file
from calendars import app
from calendars.services.auth import Auth, AuthException
from calendars.services.file_logger import FileLogger
from calendars.services.telegram_logger import TelegramLogger
from calendars.services.events_validator import EventsValidator, EventsValidatorException
from calendars.services.events_parser import EventsParser, EventsParserException
from alendars.services.events_generator import EventsGenerator, EventsGeneratorException

# --- API methods -----------------------------------------------------------------------------------------------------------
@app.route("/api/client/v1.0/events", methods=['POST'])
def save_events():
    try:
        company_id = Auth.client(request.headers.get('Auth'))
        EventsValidator.save_events(request.get_json())
        return EventsParser.save_events(company_id, request.get_json()), 200
    except AuthException as e:
        FileLogger.log_request("Auth exception. Message: " + str(e), request, "401")
        TelegramLogger.log_request("Auth exception. Message: " + str(e), request, "401")
        return '', 401
    except EventsValidatorException as e:
        response = { "state": "error", "error": { "code": 0, "message": "Validation error.", "info": str(e) } }
        FileLogger.log_request("Validation exception. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Validation exception. Message: " + str(e), request, str(response))
        return response, 400
    except EventsParserException as e:
        response = { "state": "error", "error": { "code": 0, "message": "Request error.", "info": str(e) } }
        FileLogger.log_request("Request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Request error. Message: " + str(e), request, str(response))
        return response, 400
    except Exception as e:        
        response = { "state": "error", "error": { "code": 0, "message": "Unhandled request error.", "info": str(e) } }
        FileLogger.log_request("Unhandled request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Unhandled request error. Message: " + str(e), request, str(response))
        return response, 400

@app.route("/api/client/v1.0/events", methods=['GET'])
def get_events():
    try:
        company_id = Auth.client(request.headers.get('Auth'))
        EventsValidator.get_events(request.args)
        return EventsParser.get_events(company_id, request.args), 200
    except AuthException as e:
        FileLogger.log_request("Auth exception. Message: " + str(e), request, "401")
        TelegramLogger.log_request("Auth exception. Message: " + str(e), request, "401")
        return "", 401
    except EventsValidatorException as e:
        response = { "state": "error", "error": { "code": 0, "message": "Validation error.", "info": str(e) } }
        FileLogger.log_request("Validation exception. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Validation exception. Message: " + str(e), request, str(response))
        return response, 400
    except EventsParserException as e:
        response = { "state": "error", "error": { "code": 0, "message": "Request error.", "info": str(e) } }
        FileLogger.log_request("Request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Request error. Message: " + str(e), request, str(response))
        return response, 400
    except Exception as e:        
        response = { "state": "error", "error": { "code": 0, "message": "Unhandled request error.", "info": str(e) } }
        FileLogger.log_request("Unhandled request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Unhandled request error. Message: " + str(e), request, str(response))
        return response, 400


# --- User methods ----------------------------------------------------------------------------------------------------------
@app.route("/i/<hash>", methods=['GET'])
def get_ics(hash):
    try:
        event = EventsParser.get_event_by_hash(hash,'ics')
        ics_file = EventsGenerator.get_ics_file(event)    
        return send_file(BytesIO(ics_file), download_name='event.ics', as_attachment=True, mimetype='text/calendar')
    except EventsParserException as e:
        response = { "state": "error", "error": { "code": 0, "message": "Request error.", "info": str(e) } }
        FileLogger.log_request("Request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Request error. Message: " + str(e), request, str(response))
        return '', 400
    except EventsGeneratorException as e:
        response = { "state": "error", "error": { "code": 0, "message": "Request error.", "info": str(e) } }
        FileLogger.log_request("Request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Request error. Message: " + str(e), request, str(response))
        return '', 400    
    except Exception as e:        
        response = { "state": "error", "error": { "code": 0, "message": "Unhandled request error.", "info": str(e) } }
        FileLogger.log_request("Unhandled request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Request error. Message: " + str(e), request, str(response))
        return '', 400

@app.route("/g/<hash>", methods=['GET'])
def get_google(hash):
    try:
        event = EventsParser.get_event_by_hash(hash,'google')
        google_link = EventsGenerator.get_google_link(event)                    
        return redirect(google_link)
    except EventsParserException as e:
        response = { "state": "error", "error": { "code": 0, "message": "Request error.", "info": str(e) } }
        FileLogger.log_request("Request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Request error. Message: " + str(e), request, str(response))
        return '', 400
    except EventsGeneratorException as e:
        response = { "state": "error", "error": { "code": 0, "message": "Request error.", "info": str(e) } }
        FileLogger.log_request("Request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Request error. Message: " + str(e), request, str(response))
        return response, 400    
    except Exception as e:        
        response = { "state": "error", "error": { "code": 0, "message": "Unhandled request error.", "info": str(e) } }        
        FileLogger.log_request("Unhandled request error. Message: " + str(e), request, str(response))
        TelegramLogger.log_request("Request error. Message: " + str(e), request, str(response))
        return '', 400
