from .base_command import BaseCommannd
from ..models.it_specialist_document import ItSpecialistDocument, ItSpecialistDocumentSchema
from ..session import Session
from ..errors.errors import InvalidParams, ItSpecialistDocumentNotFoundError

class GetItSpecialistDocument(BaseCommannd):
  def __init__(self, it_specialist_document_id):
    if self.is_integer(it_specialist_document_id):
      self.it_specialist_document_id = int(it_specialist_document_id)
    elif self.is_float(it_specialist_document_id):
      self.it_specialist_document_id = int(float(it_specialist_document_id))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    if len(session.query(ItSpecialistDocument).filter_by(id=self.it_specialist_document_id).all()) <= 0:
      session.close()
      raise ItSpecialistDocumentNotFoundError()

    it_specialist_document = session.query(ItSpecialistDocument).filter_by(id=self.it_specialist_document_id).one()
    schema = ItSpecialistDocumentSchema()
    it_specialist_document = schema.dump(it_specialist_document)

    session.close()

    return it_specialist_document

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