from src.commands.create_post import CreateProject
from src.session import Session, engine
from src.models.model import Base
from src.models.project import Project
from src.errors.errors import IncompleteParams, InvalidDates
from datetime import datetime, timedelta

class TestCreateProject():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_post(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    project = CreateProject(data, userId).execute()

    assert project['routeId'] == data['routeId']
    assert project['userId'] == userId
    assert 'plannedStartDate' in project
    assert 'plannedEndDate' in project

  def test_create_post_missing_fields(self):
    try:
      CreateProject({}).execute()
      assert False
    except IncompleteParams:
      assert True

  def test_create_post_invalid_dates(self):
    try:
      data = {
        'routeId': 1,
        'plannedStartDate': (datetime.now() + timedelta(days=2)).date().isoformat(),
        'plannedEndDate': datetime.now().date().isoformat()
      }
      userId = 1
      CreateProject(data, userId).execute()
      assert False
    except InvalidDates:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)