from .base_command import BaseCommannd
from .g_drive_service import GoogleDriveService

class GetAllDocsInFolder(BaseCommannd):
      
  def execute(self):
    selected_fields="files(id,name,webViewLink)"
    g_drive_service=GoogleDriveService().build()
    list_file=g_drive_service.files().list(fields=selected_fields).execute()
    return {"files":list_file.get("files")}