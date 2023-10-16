from src.commands.get_it_specialist_document import GetItSpecialistDocument
from src.commands.create_it_specialist_document import CreateItSpecialistDocument
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist_document import ItSpecialistDocument
from src.errors.errors import InvalidParams, ItSpecialistDocumentNotFoundError
from datetime import datetime, timedelta

class TestGetItSpecialistDocument():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    self.it_specialist_document = CreateItSpecialistDocument(data, userId).execute()

  def test_get_it_specialist_document(self):
    it_specialist_document = GetItSpecialistDocument(self.it_specialist_document['id']).execute()

    assert it_specialist_document['id'] == self.it_specialist_document['id']
    assert it_specialist_document['userId'] == self.it_specialist_document['userId']
    assert it_specialist_document['plannedStartDate'] == self.it_specialist_document['plannedStartDate']
    assert it_specialist_document['plannedEndDate'] == self.it_specialist_document['plannedEndDate']

  def test_get_it_specialist_document_invalid_id(self):
    try:
      GetItSpecialistDocument('Invalid').execute()
      assert False
    except InvalidParams:
      assert True

  def test_get_it_specialist_document_doesnt_exist(self):
    try:
      GetItSpecialistDocument(self.it_specialist_document['id'] + 1).execute()
      assert False
    except ItSpecialistDocumentNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)