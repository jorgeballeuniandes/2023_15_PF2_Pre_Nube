from src.commands.create_it_specialist_document import CreateItSpecialistDocument
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist_document import ItSpecialistDocument
from src.errors.errors import IncompleteParams, InvalidDates
from datetime import datetime, timedelta

class TestCreateItSpecialistDocument():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_it_specialist_document(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    it_specialist_document = CreateItSpecialistDocument(data, userId).execute()

    assert it_specialist_document['routeId'] == data['routeId']
    assert it_specialist_document['userId'] == userId
    assert 'plannedStartDate' in it_specialist_document
    assert 'plannedEndDate' in it_specialist_document

  def test_create_it_specialist_document_missing_fields(self):
    try:
      CreateItSpecialistDocument({}).execute()
      assert False
    except IncompleteParams:
      assert True

  def test_create_it_specialist_document_invalid_dates(self):
    try:
      data = {
        'routeId': 1,
        'plannedStartDate': (datetime.now() + timedelta(days=2)).date().isoformat(),
        'plannedEndDate': datetime.now().date().isoformat()
      }
      userId = 1
      CreateItSpecialistDocument(data, userId).execute()
      assert False
    except InvalidDates:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)