from .base_command import BaseCommannd
from ..models.it_specialist_document import ItSpecialistDocument, ItSpecialistDocumentSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from datetime import datetime
import boto3
import os
import logging
from flask import request

class CreateItSpecialistDocument(BaseCommannd):
  def __init__(self, data, userId = None):
    self.data = data
    if userId != None:
      self.data['userId'] = userId
   
  def execute(self):
    try:
      posted_it_specialist_document = ItSpecialistDocumentSchema(
        only=('itSpecialistId', 'userId', 'documentName', 'fileName', 'weightInBytes', 'bucketUrl','folder')
      ).load(self.data)
      it_specialist_document = ItSpecialistDocument(**posted_it_specialist_document)



      session = Session()

      session.add(it_specialist_document)
      session.commit()

      new_it_specialist_document = ItSpecialistDocumentSchema().dump(it_specialist_document)
      session.close()
      


      return new_it_specialist_document
    except TypeError:
      raise IncompleteParams
    


