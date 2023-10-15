from .base_command import BaseCommannd
from ..models.companies import Company, CompanySchema
from ..session import Session
from ..errors.errors import InvalidParams, CompanyNotFoundError

class GetCompanybyUserId(BaseCommannd):
  def __init__(self, userId):
    if self.is_integer(userId):
      self.userId = int(userId)
    elif self.is_float(userId):
      self.userId = int(float(userId))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    if len(session.query(Company).filter_by(userId=self.userId).all()) <= 0:
      session.close()
      raise CompanyNotFoundError()

    company = session.query(Company).filter_by(userId=self.userId).one()
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
