from sqlalchemy import text
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TIMESTAMP, VARCHAR, CHAR, BIGINT, INTEGER
from calendars import db

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(BIGINT(20, unsigned=True), primary_key=True, autoincrement=True, nullable=False, comment='Company ID')
    name = db.Column(VARCHAR(500), nullable=False, comment='Company name')
    cid = db.Column(VARCHAR(32),  nullable=False, comment='Company CID')
    created_at = db.Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='Company create on date')
    updated_at = db.Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='Company last update date')
    blocked_at = db.Column(TIMESTAMP, nullable=True, default=None, comment='Company block date (set to real timestamp if you need to block company)')
    block_reason = db.Column(VARCHAR(500), default=None, comment='Block reason')
    
    def register_company(self, name, cid):
        self.name = name
        self.cid = cid

    def __repr__(self) -> str:
        return f"Company's ID - {self.id}, name - {self.name}, created at {self.created_at}."

class Event(db.Model):    
    __tablename__ = 'events'

    id = db.Column(BIGINT(20, unsigned=True), primary_key=True, autoincrement=True, comment='Event ID')
    external_id = db.Column(VARCHAR(36), nullable=True, comment='Event external ID')
    hash = db.Column(CHAR(7), nullable=True, comment='Event hash')
    company_id = db.Column(BIGINT(20, unsigned=True), nullable=False, comment='Company ID')
    delivery_id = db.Column(VARCHAR(36),  nullable=True, comment='Delivery ID')
    delivery_type = db.Column(VARCHAR(200), nullable=True, comment='Delivery type')
    delivery_name = db.Column(VARCHAR(500), nullable=True, comment='Delivery name')
    summary = db.Column(VARCHAR(500), nullable=False, comment='Event summary')
    location = db.Column(VARCHAR(500), nullable=True, comment='Event location')
    description = db.Column(VARCHAR(1000), nullable=True, comment='Event description')    
    start_at = db.Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='Beginning of the event')
    end_at = db.Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='End of the event')    
    ttl = db.Column(INTEGER(10, unsigned=True), nullable=False, server_default='0', comment='Event time to live')
    ics_clicks = db.Column(INTEGER(10, unsigned=True), nullable=False, server_default='0', comment='Quantity of clicks on ics link')
    google_clicks = db.Column(INTEGER(10, unsigned=True), nullable=False, server_default='0', comment='Quantity of clicks on google link')
    created_at = db.Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='Event creation date')
    updated_at = db.Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='Event update date')

    def register_event(self, summary, start_at, end_at, hash=None, ttl=10,  company_id=1, external_id=None, delivery_id=None, delivery_type=None, delivery_name=None, location=None, description=None):
        self.external_id = external_id
        self.company_id = company_id
        self.hash = hash
        self.delivery_id = delivery_id 
        self.delivery_type = delivery_type
        self.delivery_name = delivery_name
        self.summary = summary 
        self.location = location 
        self.description = description
        self.start_at = start_at
        self.end_at = end_at
        self.ttl = ttl

    def __repr__(self) -> str:
        return f"Event's ID - {self.id}, event's company ID - {self.company_id}, created at {self.created_at}."