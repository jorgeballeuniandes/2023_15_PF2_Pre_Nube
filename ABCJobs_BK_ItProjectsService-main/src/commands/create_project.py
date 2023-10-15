from .base_command import BaseCommannd
from ..models.project import Project, ProjectSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidDates
from datetime import datetime

class CreateProject(BaseCommannd):
  def __init__(self, data, userId = None):
    self.data = data
    if userId != None:
      self.data['userId'] = userId
   
  def execute(self):
    try:
      posted_project = ProjectSchema(
        only=('userId', 'companyId', 'projectName', 'projectLeader', 'projectLeaderPhone', 'Country', 'City', 'Department')
      ).load(self.data)
      project = Project(**posted_project)



      session = Session()

      session.add(project)
      session.commit()

      new_project = ProjectSchema().dump(project)
      session.close()

      return new_project
    except TypeError:
      raise IncompleteParams

