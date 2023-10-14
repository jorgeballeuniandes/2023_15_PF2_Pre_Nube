from .base_command import BaseCommannd
from ..models.it_specialist import ItSpecialist, ItSpecialistSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidDates
from datetime import datetime

class CreateItSpecialist(BaseCommannd):
  def __init__(self, data, userId = None):
    self.data = data
    if userId != None:
      self.data['userId'] = userId
   
  def execute(self):
    try:
      posted_it_specialist = ItSpecialistSchema(
        only=('userId','name','email','nationality','profession','speciality','profile')
      ).load(self.data)
      it_specialist = ItSpecialist(**posted_it_specialist)



      session = Session()

      session.add(it_specialist)
      session.commit()

      new_post = ItSpecialistSchema().dump(it_specialist)
      session.close()

      return new_post
    except TypeError:
      raise IncompleteParams

