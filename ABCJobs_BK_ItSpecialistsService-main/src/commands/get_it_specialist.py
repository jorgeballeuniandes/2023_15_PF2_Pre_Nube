from .base_command import BaseCommannd
from ..models.it_specialist import ItSpecialist, ItSpecialistSchema
from ..session import Session
from ..errors.errors import InvalidParams, ItSpecialistNotFoundError

class GetItSpecialist(BaseCommannd):
  def __init__(self, it_specialist_id):
    if self.is_integer(it_specialist_id):
      self.it_specialist_id = int(it_specialist_id)
    elif self.is_float(it_specialist_id):
      self.it_specialist_id = int(float(it_specialist_id))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    if len(session.query(ItSpecialist).filter_by(id=self.it_specialist_id).all()) <= 0:
      session.close()
      raise ItSpecialistNotFoundError()

    it_specialist = session.query(ItSpecialist).filter_by(id=self.it_specialist_id).one()
    schema = ItSpecialistSchema()
    it_specialist = schema.dump(it_specialist)

    session.close()

    return it_specialist

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