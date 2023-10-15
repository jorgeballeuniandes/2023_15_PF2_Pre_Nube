from marshmallow import  Schema, fields
from sqlalchemy import Column, DateTime, Integer, String
from .model import Model, Base

class Company(Model, Base):
  __tablename__ = 'companies'

  companyId = Column(Integer)
  name = Column(String)
  email = Column(String)
  address = Column(String)
  country = Column(String)
  dept = Column(String)
  city = Column(String)
  phone = Column(String)
  contact_name = Column(String)
  contact_phone = Column(String)
  userId = Column(Integer)
  
  def __init__(self, companyId, name, email, address, country, dept, city, phone, contact_name, contact_phone, userId):
    Model.__init__(self)
    self.companyId = companyId
    self.name = name
    self.email = email
    self.address = address
    self.country = country
    self.dept = dept
    self.city = city
    self.phone = phone
    self.contact_name = contact_name
    self.contact_phone = contact_phone
    self.userId = userId

class CompanySchema(Schema):
  id = fields.Number()
  companyId = fields.Number()
  name = fields.Str()
  email = fields.Str()
  address = fields.Str()
  country = fields.Str()
  dept = fields.Str()
  city = fields.Str()
  phone = fields.Number()
  contact_name = fields.Str()
  contact_phone = fields.Number()
  userId = fields.Number()
