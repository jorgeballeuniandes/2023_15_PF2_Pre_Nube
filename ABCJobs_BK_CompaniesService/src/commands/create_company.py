from .base_command import BaseCommannd
from ..models.companies import Company, CompanySchema
from ..session import Session
from ..errors.errors import IncompleteParams

from .update_user_companyId import UpdateUserCompanyId


class CreateCompany(BaseCommannd):
  def __init__(self, data, token, userId):
    self.data = data
    self.token = token
    self.userId = userId
   
  def execute(self):
    try:
      posted_company = CompanySchema(
        only=('name','email','address','country','dept','city', 'phone', 'contact_name', 'contact_phone')
      ).load(self.data)
      company = Company(**posted_company)
      session = Session()
      session.add(company)
      session.commit()

      new_post = CompanySchema().dump(company)

      UpdateUserCompanyId(token = self.token, companyId = new_post['companyId'], userId = self.userId).execute()

      session.close()

      return new_post
    except TypeError:
      raise IncompleteParams
    
