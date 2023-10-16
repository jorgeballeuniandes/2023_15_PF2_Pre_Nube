from .base_command import BaseCommannd
from ..models.it_specialist_document import ItSpecialistDocument, ItSpecialistDocumentSchema
from ..session import Session
from ..errors.errors import InvalidParams, ItSpecialistDocumentNotFoundError

class GetItSpecialistDocumentsByItSpecialistId(BaseCommannd):
  def __init__(self, it_specialist_id):
    if self.is_integer(it_specialist_id):
      self.it_specialist_id = int(it_specialist_id)
    elif self.is_float(it_specialist_id):
      self.it_specialist_id = int(float(it_specialist_id))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    it_specialist_documents = session.query(ItSpecialistDocument).filter_by(itSpecialistId=self.it_specialist_id).all()
    schema = ItSpecialistDocumentSchema(many=True)
    it_specialist_documents = schema.dump(it_specialist_documents)

    session.close()

    return it_specialist_documents

  def is_integer(self, string):
    try:
      int(string)
      return True
    except:
      return False

  def is_float(self, string):
    try:
      float(string)
      return True
    except:
      return False