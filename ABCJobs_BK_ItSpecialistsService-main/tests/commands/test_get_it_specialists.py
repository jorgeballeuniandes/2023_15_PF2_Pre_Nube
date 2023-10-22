from src.commands.get_it_specialists import GetItSpecialists
from src.commands.create_it_specialist import CreateItSpecialist
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist import ItSpecialist
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta

class TestGetItSpecialists():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.it_specialist_data = {
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
    }
    self.userId = 1
    self.it_specialist = CreateItSpecialist(self.it_specialist_data, self.userId).execute()

  def test_get_it_specialists(self):
    it_specialists = GetItSpecialists().execute()
    assert len(it_specialists) >= 1
     



  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)