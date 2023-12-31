from marshmallow import  Schema, fields
from sqlalchemy import Column, String, DateTime, Double
from .model import Model, Base
import bcrypt
from datetime import datetime, timedelta
from uuid import uuid4

class User(Model, Base):
  __tablename__ = 'users'

  username = Column(String)
  email = Column(String)
  password = Column(String)
  salt = Column(String)
  token = Column(String)
  expireAt = Column(DateTime)
  role = Column(String)
  companyId = Column(Double)

  def __init__(self, username, email, password,role):
    Model.__init__(self)
    self.username = username
    self.email = email
    self.role=role
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    self.companyId= None
    self.password = bcrypt.hashpw(password, salt).decode()
    self.salt = salt.decode()
    self.set_token()

  def set_token(self):
    self.token = uuid4()
    self.expireAt = datetime.now() + timedelta(hours=1)

class UserSchema(Schema):
  id = fields.Number()
  username = fields.Str()
  email = fields.Str()
  password = fields.Str()
  salt = fields.Str()
  token = fields.Str()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()
  role =fields.Str()
  companyId = fields.Float()

class UserJsonSchema(Schema):
  id = fields.Number()
  username = fields.Str()
  email = fields.Str()
  token = fields.Str()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()
  role = fields.Str()
  companyId = fields.Float()
  
  
