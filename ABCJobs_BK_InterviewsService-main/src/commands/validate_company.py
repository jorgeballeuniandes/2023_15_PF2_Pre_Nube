from .base_command import BaseCommannd
from ..session import Session
from ..errors.errors import ParentNotFoundError
import requests
import os

class ValidateCompany(BaseCommannd):
  def __init__(self, token, companyId):
    self.token = token
    self.companyId = companyId

  def execute(self):
    host = os.environ['COMPANY_PATH'] if 'COMPANY_PATH' in os.environ else 'localhost'
    port = os.environ['COMPANY_PORT'] if 'COMPANY_PORT' in os.environ else 3003
    base_path = f'http://{host}:{port}'
    response = requests.get(
      f'{base_path}/companies/' + str(self.companyId),
      headers={
        'Authorization': f'{self.token}'
      }
    )

    if response.status_code == 200:
      return response.json()
    else:
      error = ParentNotFoundError()
      error.description = 'Company Error: ' + response.reason
      raise error