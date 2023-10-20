from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ParentNotFoundError
import requests
import os

class ValidateItSpecialist(BaseCommannd):
  def __init__(self, token, itSpecialistId):
    self.token = token
    self.itSpecialistId = itSpecialistId

  def execute(self):
    host = os.environ['IT_SPECIALIST_PATH'] if 'IT_SPECIALIST_PATH' in os.environ else 'localhost'
    port = os.environ['IT_SPECIALIST_PORT'] if 'IT_SPECIALIST_PORT' in os.environ else 3002
    base_path = f'http://{host}:{port}'
    response = requests.get(
      f'{base_path}/it_specialists/' + str(self.itSpecialistId),
      headers={
        'Authorization': f'{self.token}'
      }
    )

    if response.status_code == 200:
      return response.json()
    else:
      error = ParentNotFoundError()
      error.description = 'It Specialist Error: ' + response.reason
      raise error