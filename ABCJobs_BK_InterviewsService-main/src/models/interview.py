from marshmallow import  Schema, fields
from sqlalchemy import Column, DateTime, Integer, String
from .model import Model, Base

class Interview(Model, Base):
  __tablename__ = 'interviews'

  itSpecialistId = Column(Integer)
  companyId = Column(Integer)
  projectId = Column(Integer)
  date = Column(DateTime)
  

  def __init__(self, itSpecialistId, companyId, projectId, date):
    Model.__init__(self)
    self.itSpecialistId = itSpecialistId
    self.companyId = companyId
    self.projectId = projectId
    self.date = date

class InterviewSchema(Schema):
  id = fields.Number()
  itSpecialistId = fields.Number()
  companyId = fields.Number()
  projectId = fields.Number()
  date = fields.DateTime()
  
