from .base_command import BaseCommannd
from ..models.project import Project, ProjectSchema
from ..session import Session
from ..errors.errors import InvalidParams, ProjectNotFoundError

class GetProjectsByCompnayId(BaseCommannd):
  def __init__(self, company_id):
    if self.is_integer(company_id):
      self.company_id = int(company_id)
    elif self.is_float(company_id):
      self.company_id = int(float(company_id))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    project = session.query(Project).filter_by(companyId=self.company_id).all()
    schema = ProjectSchema(many=True)
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