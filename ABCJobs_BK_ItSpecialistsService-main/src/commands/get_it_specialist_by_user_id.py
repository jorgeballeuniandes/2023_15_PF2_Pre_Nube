from .base_command import BaseCommannd
from ..models.it_specialist import ItSpecialist, ItSpecialistSchema
from ..session import Session
from ..errors.errors import InvalidParams, ItSpecialistNotFoundError

class GetItSpecialistByUserId(BaseCommannd):
  def __init__(self, user_id):
    if self.is_integer(user_id):
      self.user_id = int(user_id)
    elif self.is_float(user_id):
      self.user_id = int(float(user_id))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    it_specialist = session.query(ItSpecialist).filter_by(userId=self.user_id).first()
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