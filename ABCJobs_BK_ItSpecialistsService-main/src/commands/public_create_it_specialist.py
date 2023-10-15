from .base_command import BaseCommannd
from ..models.it_specialist import ItSpecialist, ItSpecialistSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidDates, ItSpecialistUserIdAlreadyExistis
from .create_it_specialist import CreateItSpecialist
from .get_it_specialist_by_user_id import GetItSpecialistByUserId
from datetime import datetime
import logging

class PublicCreateItSpecialist(BaseCommannd):
  def __init__(self, data, user_id = None):
    self.data = data
    if user_id != None:
      self.data['userId'] = user_id
   
  def execute(self):
    try:    
      found_it_specialist = GetItSpecialistByUserId(self.data['userId']).execute() 
      if len(found_it_specialist) != 0:
        raise ItSpecialistUserIdAlreadyExistis
      
      
      new_it_specialist = CreateItSpecialist(self.data, self.data['userId']).execute()
      return new_it_specialist
    except TypeError:
      raise IncompleteParams

