from src.commands.get_it_specialist_documents import Getit_specialist_documents
from src.commands.create_it_specialist_document import CreateItSpecialistDocument
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist_document import ItSpecialistDocument
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta

class TestGetit_specialist_documents():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.it_specialist_document_data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    self.userId = 1
    self.it_specialist_document = CreateItSpecialistDocument(self.it_specialist_document_data, self.userId).execute()

  def test_get_it_specialist_documents(self):
    data = {
      'when': datetime.now().date().isoformat(),
      'route': self.it_specialist_document_data['routeId'],
      'filter': 'me'
    }
    it_specialist_documents = Getit_specialist_documents(data, self.userId).execute()
    assert len(it_specialist_documents) == 1

    data['when'] = (datetime.now() + timedelta(days=3)).date().isoformat()
    it_specialist_documents = Getit_specialist_documents(data, self.userId).execute()
    assert len(it_specialist_documents) == 0

  def test_get_it_specialist_documents_invalid_dates(self):
    try:
      data = {
        'when': 'invalid',
        'route': self.it_specialist_document_data['routeId'],
        'filter': 'me'
      }
      Getit_specialist_documents(data, self.userId).execute()
      assert False
    except InvalidParams:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)