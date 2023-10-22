from src.commands.get_companies import GetCompanies
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import IncompleteParams
from httmock import HTTMock

class TestGetCompanies():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_get_companies(self):
    with HTTMock():

      company =GetCompanies([]).execute()

      assert 'companyId' in company[0]
      assert 'name' in company[0]
      assert 'email' in company[0]
  
  def test_get_companies_with_filter(self):
    with HTTMock():

      company =GetCompanies({'filter': 'me'}, 1).execute()

      assert 'companyId' in company[0]
      assert 'name' in company[0]
      assert 'email' in company[0]

  def test_get_companies_with_incomplete_params(self):
    with HTTMock():
      try:
        company = GetCompanies({}, 1).execute()
      except IncompleteParams as err:
        assert err.message == 'Missing params: companyId'
  
  
