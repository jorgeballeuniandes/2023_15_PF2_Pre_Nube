from .base_command import BaseCommannd
from ..models.companies import Company, CompanySchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime

class GetCompanies(BaseCommannd):
  def __init__(self, data, companyId = None):
    try:
      self.filter = data['filter'] if 'filter' in data else None
      self.companyId = companyId
    except ValueError:
      raise InvalidParams()

  def execute(self):
    session = Session()
    companies = session.query(Company).all()

    if self.filter == 'me':
      companies = [company for company in companies if company.companyId == int(self.companyId)]

    companies = CompanySchema(many=True).dump(companies)
    session.close()

    return companies