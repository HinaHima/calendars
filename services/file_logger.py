import logging
import logging.config
import logging.handlers
from flask import request
import calendars.config as Config

logging.basicConfig(filename=Config.LOG_FILENAME, filemode='a', format="[%(asctime)s][%(levelname)s]: %(message)s")

class FileLogger:
    @staticmethod
    def log_request(message: str, request: request, response: str):
        try:
            logging.warning(message + "; " +
                            "IP: " + request.remote_addr + "; " +
                            "URL: " + request.url + "; " + 
                            "HEADERS: " + ' '.join(str(e) for e in request.headers) + "; " +
                            "REQUEST: " + str(request.get_json(silent=True)) + "; " +
                            "RESPONSE: " + response + ";"
                            )
        except Exception as e:
            pass
