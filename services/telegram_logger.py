import requests, re, io, zipfile
from datetime import datetime
from flask import request
import calendars.config as Config

class TelegramLogger():
    @staticmethod    
    def log_request(message: str, request: request, response: str):
        try:
            # Prepare message data
            id = Config.TELEGRAM_BOT_APP_SHORT_NAME + "-" +  datetime.now().strftime("%Y-%m-%d-T-%H-%M-%S")
            app = Config.TELEGRAM_BOT_APP_NAME
            
            # Prepare message
            msg  = "\U0001F534" + "\t" + "*Error*"
            msg += "\n\n"
            msg += "*ID:* " + re.sub(r"([-_\[\]\(\\)~>#+=|{}.!*])", r"\\\1", id) + "\n"
            msg += "*App:* " + re.sub(r"([-_\[\]\(\\)~>#+=|{}.!*])", r"\\\1", app) + "\n"
            msg += "*Date:* " + re.sub(r"([-_\[\]\(\\)~>#+=|{}.!*])", r"\\\1", datetime.now().strftime("%Y-%m-%dT%H:%M:%S")) + "\n"
            msg += "\n"
            msg += "*Summary:* " + re.sub(r"([-_\[\]\(\\)~>#+=|{}.!*])", r"\\\1", message) + "\n";
            
            # Prepare log file
            content =  "Message: " + message + ";\n"
            content += "IP: " + request.remote_addr + ";\n"
            content += "URL: " + request.url + ";\n"
            content += "HEADERS: " + ' '.join(str(e) for e in request.headers) + ";\n"
            content += "REQUEST: " + str(request.get_json(silent=True)) + ";\n"
            content += "RESPONSE: " + response + ";"      
            #
            text = io.StringIO()
            text.write(content)
            text.seek(0)
            #        
            file = io.BytesIO()
            file.write(text.getvalue().encode())
            file.seek(0)
            file.name = Config.TELEGRAM_BOT_APP_SHORT_NAME + "-" + datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".log"

            # Compress file
            zip = io.BytesIO()
            with zipfile.ZipFile(zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
                with zf.open(file.name, 'w') as file1:
                    file1.write(file.read())
            #
            zip.seek(0)
            zip.name = Config.TELEGRAM_BOT_APP_SHORT_NAME + "-" + datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".zip"

            # Send message
            requests.post("https://api.telegram.org/bot" + Config.TELEGRAM_BOT_TOKEN + "/sendDocument", 
                            data={
                                    "chat_id": Config.TELEGRAM_BOT_CHAT_ID,
                                    "parse_mode" : "MarkdownV2",
                                    "caption": msg                                
                                    }, 
                            files={'document': zip}
                            )
        except Exception as e:
            pass
