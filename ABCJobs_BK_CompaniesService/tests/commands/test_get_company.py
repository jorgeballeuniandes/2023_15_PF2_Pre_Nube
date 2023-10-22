from src.commands.get_company import GetCompany
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import InvalidParams, IncompleteParams
from httmock import HTTMock

class TestGetCompany():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_get_company(self):
    with HTTMock():

      company = GetCompany(1).execute()

      assert 'companyId' in company
      assert 'name' in company
      assert 'email' in company
  
  def test_get_company_with_incomplete_params(self):
    with HTTMock():
      try:
        company = GetCompany('').execute()
      except InvalidParams as err:
        assert err.description == 'Bad request'
