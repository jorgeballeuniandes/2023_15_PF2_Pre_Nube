from .base_command import BaseCommannd
from ..models.project import Project, ProjectSchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime

class GetProjects(BaseCommannd):
  def __init__(self, data, userId = None):
    try:
      self.when = datetime.strptime(data['when'], "%Y-%m-%d") if 'when' in data else None
      self.routeId = data['route'] if 'route' in data else None
      self.filter = data['filter'] if 'filter' in data else None
      self.userId = userId
    except ValueError:
      raise InvalidParams()

  def execute(self):
    session = Session()
    projects = session.query(Project).all()

    if self.filter == 'me':
      projects = [project for project in projects if project.userId == int(self.userId)]

    if self.routeId != None:
      projects = [project for project in projects if project.routeId == int(self.routeId)]

    if self.when != None:
      projects = [project for project in projects if project.plannedStartDate.date().isoformat() == self.when.date().isoformat()]

    projects = ProjectSchema(many=True).dump(projects)
    session.close()

    return projects