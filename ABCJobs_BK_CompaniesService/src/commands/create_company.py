from .base_command import BaseCommannd
from ..models.companies import Company, CompanySchema
from ..session import Session
from ..errors.errors import IncompleteParams, CompanyAlreadyExists

from .update_user_companyId import UpdateUserCompanyId


class CreateCompany(BaseCommannd):
  def __init__(self, data, token, userid):
    self.data = data
    self.token = token
    self.userId = userid
   
  def execute(self):
    try:
          
      posted_company = CompanySchema(
        only=('name','email','address','country','dept','city', 'phone', 'contact_name', 'contact_phone')
      ).load(self.data)
      company = Company(**posted_company)
      session = Session()

      company_exists = session.query(Company).filter_by(name=self.data['name']).first()

      if company_exists:
        raise CompanyAlreadyExists
      
      session.add(company)
      session.commit()

      new_post = CompanySchema().dump(company)

      UpdateUserCompanyId(token = self.token, companyId = new_post['companyId'], userId = self.userId).execute()

      session.close()

      return new_post
    except TypeError:
      raise IncompleteParams
    except CompanyAlreadyExists:
      raise CompanyAlreadyExists
    
