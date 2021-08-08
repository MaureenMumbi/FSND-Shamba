import os
from sqlalchemy import Column, String, Integer, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate



# database_path = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
# if not database_path:
database_name = "shamba"
database_path = "postgresql://{}/{}".format('postgres@localhost:5432', database_name)


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path= database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


'''
Worker

'''
class Worker(db.Model):
    __tablename__ = 'worker'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    national_id= Column(Integer)
    phone_number= Column(String)
    type = Column(String)
    procedures = db.relationship('Procedure', backref='worker', lazy=True)

    def __init__(self, name, national_id, phone_number, type):
        self.name = name
        self.national_id = national_id
        self.phone_number = phone_number
        self.type = type
   
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id':self.id,
            'name': self.name,
            'national_id': self.national_id,
            'phone_number':self.phone_number,
            'type':self.type
        }



'''
Inputs
'''

class Inputs(db.Model):
    __tablename__ = 'inputs'
    id = Column(Integer, primary_key=True)
    name =Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    metrics = Column(String, nullable=False)
    type = Column(String)
    procedures = db.relationship('Procedure', backref='inputs', lazy=True)

    def __init__(self, name, quantity, type, metrics):
        self.name = name
        self.quantity = quantity
        self.type = type
        self.metrics = metrics
   
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id':self.id,
            'name': self.name,
            'quantity':self.quantity,
            'metrics': self.metrics, 
        }

'''
Fields
'''

class Fields(db.Model):
    __tablename__ = 'fields'
    id = Column(Integer, primary_key=True)
    name =Column(String, nullable=False)
    size = Column(Float, nullable=False)
    procedures = db.relationship('Procedure', backref='fields', lazy=True)

    def __init__(self, name, size):
        self.name = name
        self.size = size
       
   
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id':self.id,
            'name': self.name,
            'size': self.size,
        }
   

'''
Procedure
'''

class Procedure(db.Model):
    __tablename__ = 'procedures'
    id = Column(Integer, primary_key=True)
    name = Column (String)
    date =Column(db.DateTime, nullable=False)
    activity = Column(String)
    field_id = Column(Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)
    worker_id =Column(Integer, db.ForeignKey('worker.id', ondelete='CASCADE'), nullable=False)
    input_id =Column(Integer, db.ForeignKey('inputs.id', ondelete='CASCADE'), nullable=True)
    inputs_quantity =Column(Integer, nullable=True)
    image_link = Column(String,nullable=True)

    def __init__(self, name, date, activity, field_id, worker_id, input_id, inputs_quantity,image_link):
        self.name = name
        self.date = date
        self.activity = activity
        self.field_id = field_id
        self.worker_id = worker_id
        self.input_id = input_id
        self.inputs_quantity = inputs_quantity
        self.image_link = image_link      
   
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id':self.id,
            'name': self.name,
            'date':self.date,
            'activity':self.activity,
            'field': self.field_id,
            'worker':self.worker_id,
            'input': self.input_id,
            'inputs_qty': self.inputs_quantity,
            'image_link':self.image_link
        }


