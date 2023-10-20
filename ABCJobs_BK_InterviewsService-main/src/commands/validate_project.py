from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ParentNotFoundError
import requests
import os

class ValidateProject(BaseCommannd):
  def __init__(self, token, projectId):
    self.token = token
    self.projectId = projectId

  def execute(self):
    host = os.environ['PROJECT_PATH'] if 'PROJECT_PATH' in os.environ else 'localhost'
    port = os.environ['PROJECT_PORT'] if 'PROJECT_PORT' in os.environ else 3004
    base_path = f'http://{host}:{port}'
    response = requests.get(
      f'{base_path}/projects/' + str(self.projectId),
      headers={
        'Authorization': f'{self.token}'
      }
    )

    if response.status_code == 200:
      return response.json()
    else:
      error = ParentNotFoundError()
      error.description = 'Project Error: ' + response.reason
      raise error