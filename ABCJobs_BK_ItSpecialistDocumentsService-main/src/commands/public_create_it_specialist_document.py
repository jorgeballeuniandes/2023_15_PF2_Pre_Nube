from .base_command import BaseCommannd
from ..models.it_specialist_document import ItSpecialistDocument, ItSpecialistDocumentSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidDates, ItSpecialistDocumentUserIdAlreadyExistis
from .create_it_specialist_document import CreateItSpecialistDocument
from datetime import datetime
import logging

class PublicCreateItSpecialistDocument(BaseCommannd):
  def __init__(self, data, user_id = None):
    self.data = data
    if user_id != None:
      self.data['userId'] = user_id
   
  def execute(self):
    try:    
      new_it_specialist_document = CreateItSpecialistDocument(self.data, self.data['userId']).execute()
      return new_it_specialist_document
    except TypeError:
      raise IncompleteParams

