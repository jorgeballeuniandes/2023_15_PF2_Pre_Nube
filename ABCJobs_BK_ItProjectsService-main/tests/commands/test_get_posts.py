from src.commands.get_projects import Getprojects
from src.commands.create_post import CreateProject
from src.session import Session, engine
from src.models.model import Base
from src.models.project import Project
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta

class TestGetprojects():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.post_data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    self.userId = 1
    self.project = CreateProject(self.post_data, self.userId).execute()

  def test_get_projects(self):
    data = {
      'when': datetime.now().date().isoformat(),
      'route': self.post_data['routeId'],
      'filter': 'me'
    }
    projects = Getprojects(data, self.userId).execute()
    assert len(projects) == 1

    data['when'] = (datetime.now() + timedelta(days=3)).date().isoformat()
    projects = Getprojects(data, self.userId).execute()
    assert len(projects) == 0

  def test_get_projects_invalid_dates(self):
    try:
      data = {
        'when': 'invalid',
        'route': self.post_data['routeId'],
        'filter': 'me'
      }
      Getprojects(data, self.userId).execute()
      assert False
    except InvalidParams:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)