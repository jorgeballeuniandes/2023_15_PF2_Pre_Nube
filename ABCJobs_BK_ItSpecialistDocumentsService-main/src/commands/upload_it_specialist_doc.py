from .base_command import BaseCommannd
from .g_drive_service import GoogleDriveService
import io
from datetime import datetime
from flask import request
from googleapiclient.http import MediaIoBaseUpload

class UploadItSpecialistDoc(BaseCommannd):
      
  def execute(self):
    file = request.files['file']
    buffer_memory=io.BytesIO()
    file.save(buffer_memory)

    media_body=MediaIoBaseUpload(file, file.mimetype, resumable=True)

    created_at= datetime.now().strftime("%Y%m%d%H%M%S")
    file_metadata={
        "name":f"{file.filename} ({created_at})"
    }

    returned_fields="id, name, mimeType, webViewLink, exportLinks"
    
    g_drive_service=GoogleDriveService().build()
    upload_response=g_drive_service.files().create(
        body = file_metadata, 
        media_body=media_body,  
        fields=returned_fields
    ).execute()

    return upload_response
    
    
    # uploaded_file=request.files.get("file")
    # buffer_memory=BytesIO()
    # uploaded_file.save(buffer_memory)
    # media_body=MediaIoBaseUpload(uploaded_file, uploaded_file.mimetype, resumable=True)
    # g_drive_service=GoogleDriveService().build()
    # created_at= datetime.now().strftime("%Y%m%d%H%M%S")
    # file_metadata={
    #     "name":f"{uploaded_file.filename} ({created_at})"
    # }

    # returned_fields="id, name, mimeType, webViewLink, exportLinks"
    
    # upload_response=g_drive_service.files().create(
    #     body = file_metadata, 
    #     media_body=media_body,  
    #     fields=returned_fields
    # ).execute()
    # return upload_response