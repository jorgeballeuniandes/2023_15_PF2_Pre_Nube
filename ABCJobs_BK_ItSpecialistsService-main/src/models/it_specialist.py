from marshmallow import  Schema, fields
from sqlalchemy import Column, DateTime, Integer, String
from .model import Model, Base

class ItSpecialist(Model, Base):
  __tablename__ = 'it_specialists'

  userId = Column(Integer)
  name = Column(String)
  email = Column(String)
  nationality = Column(String)
  profession = Column(String)
  speciality = Column(String)
  profile = Column(String)

  def __init__(self, userId, name, email, nationality, profession, speciality, profile):
    Model.__init__(self)
    self.userId = userId
    self.name = name
    self.email = email
    self.nationality = nationality
    self.profession = profession
    self.speciality = speciality
    self.profile = profile

class ItSpecialistSchema(Schema):
  id = fields.Number()
  userId = fields.Number()
  name = fields.String()
  email = fields.String()
  nationality = fields.String()
  profession = fields.String()
  speciality = fields.String()
  profile = fields.String()
  createdAt = fields.DateTime()
