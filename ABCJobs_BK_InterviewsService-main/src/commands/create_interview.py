from .base_command import BaseCommannd
from ..models.interview import Interview, InterviewSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidDates
from .validate_it_specialist import ValidateItSpecialist
from .validate_company import ValidateCompany
from .validate_project import ValidateProject
from datetime import datetime

class CreateInterview(BaseCommannd):
  def __init__(self, data, auth_token):
    self.data = data
    self.auth_token = auth_token

  def execute(self):
    try:
      posted_interview = InterviewSchema(
        only=('itSpecialistId','companyId','projectId','date')
      ).load(self.data)
      interview = Interview(**posted_interview)
      ValidateItSpecialist(self.auth_token,self.data['itSpecialistId']).execute()
      ValidateCompany(self.auth_token,self.data['companyId']).execute()
      ValidateProject(self.auth_token,self.data['projectId']).execute()

      session = Session()

      session.add(interview)
      session.commit()

      new_post = InterviewSchema().dump(interview)
      session.close()

      return new_post
    except TypeError:
      raise IncompleteParams

