from marshmallow import  Schema, fields
from sqlalchemy import Column, DateTime, Integer, String
from .model import Model, Base

class Project(Model, Base):
  __tablename__ = 'projects'

  userId = Column(Integer)
  companyId = Column(Integer)
  projectName = Column(String)
  projectLeader = Column(String)
  projectLeaderPhone = Column(String)
  Country = Column(String)
  City = Column(String)
  Department = Column(String)

  def __init__(self, userId, companyId, projectName, projectLeader, projectLeaderPhone, Country, City, Department):
    Model.__init__(self)
    self.userId = userId
    self.companyId = companyId
    self.projectName = projectName
    self.projectLeader = projectLeader
    self.projectLeaderPhone = projectLeaderPhone
    self.Country = Country
    self.City = City
    self.Department = Department

class ProjectSchema(Schema):
  id = fields.Number()
  userId = fields.Number()
  companyId = fields.Number()
  projectName = fields.String()
  projectLeader = fields.String()
  projectLeaderPhone = fields.String()
  Country = fields.String()
  City = fields.String()
  Department = fields.String()
  createdAt = fields.DateTime()
