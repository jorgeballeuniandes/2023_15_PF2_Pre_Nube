from marshmallow import  Schema, fields
from sqlalchemy import Column, DateTime, Integer, String
from .model import Model, Base

class ItSpecialistDocument(Model, Base):
  __tablename__ = 'it_specialist_documents'

  itSpecialistId = Column(Integer)
  userId = Column(Integer)
  documentName = Column(String)
  fileName = Column(String)
  weightInBytes = Column(Integer)
  bucketUrl = Column(String)
  folder = Column(String)

  def __init__(self, itSpecialistId, userId, documentName, fileName, weightInBytes, bucketUrl, folder):
    Model.__init__(self)
    self.itSpecialistId = itSpecialistId
    self.userId = userId
    self.documentName = documentName
    self.fileName = fileName
    self.weightInBytes = weightInBytes
    self.bucketUrl = bucketUrl
    self.folder = folder

class ItSpecialistDocumentSchema(Schema):
  id = fields.Number()
  itSpecialistId = fields.Number()
  userId = fields.Number()
  documentName = fields.String()
  fileName = fields.String()
  weightInBytes = fields.Number()
  bucketUrl = fields.String()
  folder = fields.String()
  profile = fields.String()
  createdAt = fields.DateTime()

