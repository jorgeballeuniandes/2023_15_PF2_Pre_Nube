from .base_command import BaseCommannd
from ..models.it_specialist_document import ItSpecialistDocument, ItSpecialistDocumentSchema
from ..session import Session
from ..errors.errors import IncompleteParams, NoFilePart, NoSelectedFile, NotAllowedFileType
from datetime import datetime
import boto3
import os
import logging
from flask import request


ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
  return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class CreateItSpecialistDocument(BaseCommannd):
  def __init__(self, data, userId = None):
    self.data = data
    if userId != None:
      self.data['userId'] = userId
   
  def execute(self):
    try:
      posted_it_specialist_document = ItSpecialistDocumentSchema(
        only=('itSpecialistId', 'userId', 'documentName', 'fileName', 'weightInBytes', 'bucketUrl','folder')
      ).load(self.data)
      it_specialist_document = ItSpecialistDocument(**posted_it_specialist_document)
      if 'file' not in request.files:
        raise NoFilePart
      file = request.files['file']
      # if user does not select file, browser also
      # submit an empty part without filename
      if file.filename == '':
        raise NoSelectedFile
      if not file or not allowed_file(file.filename):
        raise NotAllowedFileType


      session = Session()

      session.add(it_specialist_document)
      session.commit()

      new_it_specialist_document = ItSpecialistDocumentSchema().dump(it_specialist_document)
      session.close()
      
      try:       
        s3_client = boto3.resource(
          's3',
          aws_access_key_id=os.environ['S3_ACCESS_KEY'],
          aws_secret_key_access_key=os.environ['S3_SECRET_ACCESS_KEY'],
          region_name=os.environ['S3_REGION']          
        )
        s3_client.Bucket(os.environ['S3_BUCKET_NAME']).put_object(Key=os.environ['S3_INNER_FILE_NAME']+str(it_specialist_document['id']),Body=file)
      except Exception as e:
        logging.warning("Error al cargar documento{}".format(e))
        

      return new_it_specialist_document
    except TypeError:
      raise IncompleteParams
    

