from .base_command import BaseCommannd
from ..models.it_specialist import ItSpecialist, ItSpecialistSchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime

class GetItSpecialists(BaseCommannd):

  def execute(self):
    session = Session()
    it_specialists = session.query(ItSpecialist).all()

    it_specialists = ItSpecialistSchema(many=True).dump(it_specialists)
    session.close()

    return it_specialists