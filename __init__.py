from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from calendars.config import SQLALCHEMY_DATABASE_URI, SWAGGER_URL, SWAGGER_FILE_URL
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
#
app = Flask(__name__)
#
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    SWAGGER_FILE_URL,
    config={ "app_name": "Calendars" }
)
app.register_blueprint(swaggerui_blueprint)
#
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
#
from calendars import routes, models
