from .base_command import BaseCommannd
from ..models.interview import Interview, InterviewSchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime

class GetInterviews(BaseCommannd):

  def execute(self):
    session = Session()
    interviews = session.query(Interview).all()

    interviews = InterviewSchema(many=True).dump(interviews)
    session.close()

    return interviews