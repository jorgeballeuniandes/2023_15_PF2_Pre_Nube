from .base_command import BaseCommannd
from ..models.interview import Interview, InterviewSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidDates
from datetime import datetime

class CreateInterview(BaseCommannd):
  def __init__(self, data):
    self.data = data

   
  def execute(self):
    try:
      posted_interview = InterviewSchema(
        only=('itSpecialistId','companyId','projectId','date')
      ).load(self.data)
      interview = Interview(**posted_interview)



      session = Session()

      session.add(interview)
      session.commit()

      new_post = InterviewSchema().dump(interview)
      session.close()

      return new_post
    except TypeError:
      raise IncompleteParams

