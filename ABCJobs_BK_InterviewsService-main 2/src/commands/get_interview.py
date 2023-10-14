from .base_command import BaseCommannd
from ..models.interview import Interview, InterviewSchema
from ..session import Session
from ..errors.errors import InvalidParams, InterviewNotFoundError

class GetInterview(BaseCommannd):
  def __init__(self, post_id):
    if self.is_integer(post_id):
      self.post_id = int(post_id)
    elif self.is_float(post_id):
      self.post_id = int(float(post_id))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    if len(session.query(Interview).filter_by(id=self.post_id).all()) <= 0:
      session.close()
      raise InterviewNotFoundError()

    interview = session.query(Interview).filter_by(id=self.post_id).one()
    schema = InterviewSchema()
    interview = schema.dump(interview)

    session.close()

    return interview

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