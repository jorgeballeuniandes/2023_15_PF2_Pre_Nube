from .base_command import BaseCommannd
from ..models.it_specialist import ItSpecialist, ItSpecialistSchema
from ..session import Session
from ..errors.errors import InvalidParams, ItSpecialistNotFoundError

class GetItSpecialistByUserId(BaseCommannd):
  def __init__(self, user_id_):
    if self.is_integer(user_id_):
      self.user_id_ = int(user_id_)
    elif self.is_float(user_id_):
      self.user_id_ = int(float(user_id_))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    it_specialist = session.query(ItSpecialist).filter_by(userId=self.user_id_).first()
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