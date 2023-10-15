from src.commands.get_post import GetProject
from src.commands.create_post import CreateProject
from src.session import Session, engine
from src.models.model import Base
from src.models.project import Project
from src.errors.errors import InvalidParams, ProjectNotFoundError
from datetime import datetime, timedelta

class TestGetProject():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    self.project = CreateProject(data, userId).execute()

  def test_get_post(self):
    project = GetProject(self.project['id']).execute()

    assert project['id'] == self.project['id']
    assert project['userId'] == self.project['userId']
    assert project['plannedStartDate'] == self.project['plannedStartDate']
    assert project['plannedEndDate'] == self.project['plannedEndDate']

  def test_get_post_invalid_id(self):
    try:
      GetProject('Invalid').execute()
      assert False
    except InvalidParams:
      assert True

  def test_get_post_doesnt_exist(self):
    try:
      GetProject(self.project['id'] + 1).execute()
      assert False
    except ProjectNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)