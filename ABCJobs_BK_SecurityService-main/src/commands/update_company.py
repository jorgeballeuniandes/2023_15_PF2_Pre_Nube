from .base_command import BaseCommannd
from ..models.user import User, UserJsonSchema
from ..session import Session
from ..errors.errors import Unauthorized, IncompleteParams
from datetime import datetime


class UpdateCompanyId(BaseCommannd):
  def __init__(self, newid,companyId, token = None):
    self.newid=newid
    self.companyId = companyId
    if token == None or token == "":
      raise IncompleteParams()
    else:
      self.token = self.parse_token(token)
  
  def execute(self):
    session = Session()
    
    if len(session.query(User).filter_by(token=self.token).all()) <= 0:
      session.close()
      raise Unauthorized()

    user = session.query(User).filter_by(token=self.token).one()
    
    if user.expireAt < datetime.now():
      session.close()
      raise Unauthorized()
    if len (session.query(User).filter_by(companyId = self.companyId).all()) == 1: 
      user = session.query(User).filter_by(companyId=self.companyId).one() 
      user.companyId = self.newid
      session.commit()
    else:
      raise Unauthorized()
    
    schema = UserJsonSchema()
    user = schema.dump(user)
    session.close()

    return user
  
  def parse_token(self, token):
    return token.split(' ')[1]