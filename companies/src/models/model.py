from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Model():
  id = Column(Integer, primary_key=True)
  

  def __init__(self):
    pass