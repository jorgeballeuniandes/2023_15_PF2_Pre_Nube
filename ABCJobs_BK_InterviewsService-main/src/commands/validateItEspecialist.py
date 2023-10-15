from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ExternalError
import requests
from flask import jsonify
import os

class ValidateItSpecialist(BaseCommannd):
  def __init__(self, token):
    self.token = token

  def execute(self):
    host = os.environ['IT_SPECIALIST_PATH'] if 'IT_SPECIALIST_PATH' in os.environ else 'localhost'
    port = os.environ['IT_SPECIALIST_PORT'] if 'IT_SPECIALIST_PORT' in os.environ else 3000
    base_path = f'http://{host}:{port}'
    response = requests.get(
      f'{base_path}/public/me',
      headers={
        'Authorization': f'{self.token}'
      }
    )

    if response.status_code == 200:
      return response.json()
    else:
      raise ExternalError(response.status_code)