from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import settings.settings as settings
from datetime import datetime
from connections import db_conn

#todo implement 

class GdriveConn:
    def __init__(self, sid):
        self.drive = self.authenticate()
        self.sid = sid

    def authenticate(self):
        gauth = GoogleAuth()
        gauth.DEFAULT_SETTINGS['client_config_file'] = settings.GOOGLE_CLIENT_SECRETS
        gauth.LoadCredentialsFile(settings.GOOGLE_CLIENT_CREDENTIALS)
        return GoogleDrive(gauth)

    def upload_file(self, google_id, file, mimetype, filename='random'):
        myfile = self.drive.CreateFile({'title':filename, 'mimeType':mimetype,
        "parents": [{"kind": "drive#fileLink","id": google_id}]})
        document_id = myfile['parents'][0]['id']
        myfile.SetContentString(file)
        myfile.Upload()

        #myfile.FetchMetadata(fields='*')
        myfile.FetchMetadata(fields='permissions')
        permission = myfile.InsertPermission({
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'writer'})
        myfile.FetchMetadata(fields='permissions')
        return document_id

    def download_file(self, google_id, filename):
        try:
            myfile = self.drive.CreateFile({'id': google_id})
            myfile.GetContentFile(filename)
        except Exception as e:
            print(e)
            raise ValueError(str(e))

    def download_files(self, google_id_path, filename='random'):
        results = self.list_folder(google_id_path)
        for myfile in results():
            file1 = self.drive.CreateFile({'id': myfile['id']})
            file1.GetContentFile(filename) 

            # Initialize GoogleDriveFile instance with file id.
            #file1 = drive.CreateFile({'id': myfile['id']})
            #content = file1.GetContentString()

    def list_folder(self, google_id_path):
        request_template = "'{parent_id}' in parents and trashed=false"
        file_list = self.drive.ListFile({'q': request_template.format(parent_id=google_id_path)}).GetList()
        return file_list
    
    def upload_notebook(self, data, filename):
        #Store notebook in google drive
        result = self.list_folder(settings.GOOGLE_COLAB_FOLDER)
        gid = self.upload_file(settings.GOOGLE_COLAB_FOLDER, data, settings.GOOGLE_DOC_TYPE, filename)
        return gid

        
        