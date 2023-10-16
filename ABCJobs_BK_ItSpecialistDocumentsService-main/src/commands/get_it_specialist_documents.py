from .base_command import BaseCommannd
from ..models.it_specialist_document import ItSpecialistDocument, ItSpecialistDocumentSchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime

class GetItSpecialistDocuments(BaseCommannd):
  def __init__(self, data, userId = None):
    try:
      self.when = datetime.strptime(data['when'], "%Y-%m-%d") if 'when' in data else None
      self.routeId = data['route'] if 'route' in data else None
      self.filter = data['filter'] if 'filter' in data else None
      self.userId = userId
    except ValueError:
      raise InvalidParams()

  def execute(self):
    session = Session()
    it_specialist_documents = session.query(ItSpecialistDocument).all()

    if self.filter == 'me':
      it_specialist_documents = [it_specialist_document for it_specialist_document in it_specialist_documents if it_specialist_document.userId == int(self.userId)]

    if self.routeId != None:
      it_specialist_documents = [it_specialist_document for it_specialist_document in it_specialist_documents if it_specialist_document.routeId == int(self.routeId)]

    if self.when != None:
      it_specialist_documents = [it_specialist_document for it_specialist_document in it_specialist_documents if it_specialist_document.plannedStartDate.date().isoformat() == self.when.date().isoformat()]

    it_specialist_documents = ItSpecialistDocumentSchema(many=True).dump(it_specialist_documents)
    session.close()

    return it_specialist_documents