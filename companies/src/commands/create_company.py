from .base_command import BaseCommannd
from ..models.companies import Company, CompanySchema
from ..session import Session
from ..errors.errors import IncompleteParams


class CreateCompany(BaseCommannd):
  def __init__(self, data, companyId = None):
    self.data = data
    if companyId != None:
      self.data['companyId'] = companyId
   
  def execute(self):
    try:
      posted_company = CompanySchema(
        only=('companyId','name','email','address','country','dept','city', 'phone', 'contact_name', 'contact_phone')
      ).load(self.data)
      company = Company(**posted_company)
      session = Session()
      session.add(company)
      session.commit()

      new_post = CompanySchema().dump(company)
      session.close()

      return new_post
    except TypeError:
      raise IncompleteParams
    
