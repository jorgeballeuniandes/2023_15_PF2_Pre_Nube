from .base_command import BaseCommannd
from .g_drive_service import GoogleDriveService
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io
import logging
import os

class DownloadFileById(BaseCommannd):
  def __init__(self, doc_name):
    self.doc_name = doc_name
      
  def execute(self):
    
    try:
        # create drive api client
        service = GoogleDriveService().build()

        file_id = self.doc_name

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None
    
    file.seek(0, os.SEEK_END)
    print(file.tell())
    
    
    # g_drive_service=GoogleDriveService().build()
    # self.doc_id = self.doc_name    
    # request = g_drive_service.files().get_media(fileId=self.doc_id)
    # fh = io.BytesIO()
    # downloader = MediaIoBaseDownload(fh, request)
    # done = False
    # while done is False:
    #   status, done = downloader.next_chunk()
    #   logging.warning(F'Download {int(status.progress() * 100)}.')
    # return fh.getvalue()