import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Swagger module config
SWAGGER_URL = '/docs/api/client/v1.0'
SWAGGER_FILE_URL = '/static/docs/api/client/1_0.yaml'

# Service config
BASE_URL = 'url.for.example'
SHORT_URL = 'x.y.z'

# ORM config
SQLALCHEMY_DATABASE_URI = "mysql://user:sdfoIODJFjnscjksdf_safklwer@localhost/db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

#LOGGER
LOG_FILENAME = "./logs/logs.log"

#Telegram
TELEGRAM_BOT_TOKEN = "asdfkljhn4238924kmwsf2390_wiejfm-234"
TELEGRAM_BOT_CHAT_ID = "-1234567890"
TELEGRAM_BOT_APP_NAME = "Calendars"
TELEGRAM_BOT_APP_SHORT_NAME = "CAL"