# calendars
This project is the backend part of service that permits to create ICS-files and events in Google Calendars.

-The idea is that the user fills in some fields to create an "event". The server handles the information and stores it in a database (MySQL in our case). 
-After this the user can ask to create an ICS-file (calendar format) and/or a Google-event. The server gets the information from the database and:
1. Dynamically create the file without storing it in the server, then sends it to the user.    
2. Creates a Google-event.

-The server validates the incoming requests.

-Authorization through API-key is included :)

-You can also find swagger-documentation in the static folder.
