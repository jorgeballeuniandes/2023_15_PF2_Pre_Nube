from .base_command import BaseCommannd
from ..models.companies import Company, CompanySchema
from ..session import Session
from ..errors.errors import InvalidParams, CompanyNotFoundError

class GetCompanyByUserId(BaseCommannd):
  def __init__(self, user_id):
    if self.is_integer(user_id):
      self.user_id = int(user_id)
    elif self.is_float(user_id):
      self.user_id = int(float(user_id))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    company = session.query(Company).filter_by(userId=self.user_id).first()
    schema = CompanySchema()
    company = schema.dump(company)

    session.close()

    return company

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
