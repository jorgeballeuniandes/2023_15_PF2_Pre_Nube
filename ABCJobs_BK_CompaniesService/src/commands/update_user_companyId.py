from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ExternalError
import requests
from flask import jsonify
import os

class UpdateUserCompanyId(BaseCommannd):
  def __init__(self, token, companyId, userId):
    self.token = token
    self.companyId = companyId
    self.userId = userId

  def execute(self):
    host = os.environ['USERS_PATH'] if 'USERS_PATH' in os.environ else 'localhost'
    port = os.environ['USERS_PORT'] if 'USERS_PORT' in os.environ else 3000
    base_path = f'http://{host}:{port}'

    data = {
        "userId": self.userId,
        "companyId": self.companyId
    }

    response = requests.post(
      f'{base_path}/update/companyID/',
      headers={
        'Authorization': f'{self.token}'
      },
      json = data
    )

    if response.status_code == 200:
      return response.json()
    else:
      raise ExternalError(response.status_code)