from .base_command import BaseCommannd
from ..models.interview import Interview, InterviewSchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime

class GetInterviews(BaseCommannd):
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
    interviews = session.query(Interview).all()

    if self.filter == 'me':
      interviews = [interview for interview in interviews if interview.userId == int(self.userId)]

    if self.routeId != None:
      interviews = [interview for interview in interviews if interview.routeId == int(self.routeId)]

    if self.when != None:
      interviews = [interview for interview in interviews if interview.plannedStartDate.date().isoformat() == self.when.date().isoformat()]

    interviews = InterviewSchema(many=True).dump(interviews)
    session.close()

    return interviews