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

class UploadItSpecialistDocument(BaseCommannd):

   
  def execute(self):
    try:
      document_id = request.form['document_id']
      logging.warning("Este es el document_id: {}".format(document_id))
      file = request.files['file']
      # if user does not select file, browser also
      # submit an empty part without filename
      if file.filename == '':
        raise NoSelectedFile
      if not file or not allowed_file(file.filename):
        raise NotAllowedFileType     
      
      try:       
        s3_client = boto3.resource(
          's3',
          aws_access_key_id=os.environ['S3_ACCESS_KEY'],
          aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY'],
          region_name=os.environ['S3_REGION']          
        )
        s3_client.Bucket(os.environ['S3_BUCKET_NAME']).put_object(Key=os.environ['S3_INNER_FILE_NAME']+str(document_id)+".pdf",Body=file)
      except Exception as e:
        logging.warning("Error al cargar documento: {}".format(e))
      return "Document uploaded successfully"
    except TypeError:
      raise IncompleteParams
    


