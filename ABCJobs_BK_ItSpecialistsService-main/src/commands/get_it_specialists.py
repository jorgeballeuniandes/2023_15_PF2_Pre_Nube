from .base_command import BaseCommannd
from ..models.it_specialist import ItSpecialist, ItSpecialistSchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime

class GetItSpecialists(BaseCommannd):
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
    it_specialists = session.query(ItSpecialist).all()

    if self.filter == 'me':
      it_specialists = [it_specialist for it_specialist in it_specialists if it_specialist.userId == int(self.userId)]

    if self.routeId != None:
      it_specialists = [it_specialist for it_specialist in it_specialists if it_specialist.routeId == int(self.routeId)]

    if self.when != None:
      it_specialists = [it_specialist for it_specialist in it_specialists if it_specialist.plannedStartDate.date().isoformat() == self.when.date().isoformat()]

    it_specialists = ItSpecialistSchema(many=True).dump(it_specialists)
    session.close()

    return it_specialists