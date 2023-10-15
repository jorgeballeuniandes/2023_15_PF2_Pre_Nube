from .base_command import BaseCommannd
from ..models.project import Project, ProjectSchema
from ..session import Session
from ..errors.errors import InvalidParams, ProjectNotFoundError

class GetProject(BaseCommannd):
  def __init__(self, project_id):
    if self.is_integer(project_id):
      self.project_id = int(project_id)
    elif self.is_float(project_id):
      self.project_id = int(float(project_id))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    if len(session.query(Project).filter_by(id=self.project_id).all()) <= 0:
      session.close()
      raise ProjectNotFoundError()

    project = session.query(Project).filter_by(id=self.project_id).one()
    schema = ProjectSchema()
    project = schema.dump(project)

    session.close()

    return project

  def is_integer(self, string):
    try:
      int(string)
      return True
    except:
      return False

  def is_float(self, string):
    try:
      float(string)
      return True
    except:
      return False