from __future__ import print_function
from googleapiclient.discovery import build
from flask import jsonify
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
from db_manager import DatabaseManageer
import os


class DriveManager(object):
    """This class contains the functions for transaction required with google drive API"""


    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/drive'
    client_id_file = os.path.abspath("client_id.json")
    client_token = os.path.abspath('token.json')


    def drive_connection(self):
        """Set the connection with the google drive API.

        Returns
        service
        type
            Conecction with google drive API.

        """
        store = file.Storage(self.client_token)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.client_id_file, self.SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('drive', 'v3', http=creds.authorize(Http()))
        return service

    def search_in_folder(self,id,name):
        """Searches a given file name in a folder identified by id.

        Parameters
        id : string
            folder identificator.
        name : string
            Name of file we want to search.

        Returns
        id
        type
            id of file found or initial given id if file not found.

        status
        type
            Numeric value, 1 if file found 0 if not found

        """
        service = self.drive_connection()
        results = service.files().list(q=f"'{id}' in parents ",fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        status = 0
        if items:
            for item in items:
                if item["name"] == name:
                    status = 1
                    id = item["id"]
                    return id, status
        return id, status

    def check_drive_path(self,path):
        """check if all folders of a given path exist in google Drive.

        Parameters
        ----------
        path : type
            Path we want to check.

        Returns
        -------
        id
        type
            Identificator for last folder found.
        index
            Index for last folder found in the given path

        """
        index = 0
        id = "root"
        if path == "":
            return id, index
        path = path.split("/")
        for folder in path:
            if folder == "":
                return None, None
            id, status = self.search_in_folder(id, folder)
            if status == 1:
                index += 1
            else:
                break
        return id , index

    def load_to_drive_path(self,media_path,drive_path,file_name):
        """Load a file in goolge drive.

        Parameters
        ----------
        media_path : string
            media path of file we want to upload to Drive.
        drive_path : string
            Path where we want to put the file.
        file_name : type
            name for file in Drive.

        Returns
        -------
        json
            json with url uploaded file .

        """

        folder_id, index= self.check_drive_path(drive_path)
        if folder_id == None and index == None:
            error = "Invalitd Drive Path"
            print(error)
            return error
        drive_path = drive_path.split("/")
        for folder in drive_path[index:]:
            folder_id = self.create_drive_folder(folder_id,folder)
        file_id = self.load_by_id(media_path,folder_id,file_name)
        file_url = f"https://drive.google.com/file/d/{file_id}"
        DatabaseManageer().file_db_register(file_name,file_url)
        return   jsonify({"file_url":file_url})

    def create_drive_folder(self,parent_id, folder_name):
        """create a folder in Drive.

        Parameters
        ----------
        parent_id : string
            location id for folder where we want to save the folder that we will create.
        folder_name : string
            name we will give to the new folder.

        Returns
        -------
        string
            created folder id.

        """
        service = self.drive_connection()
        file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
        }
        file = service.files().create(body=file_metadata,
        fields='id').execute()
        id = file.get('id')
        return id

    def load_by_id(self,media_path,parent_id,file_name):
        """loads a file in the given id folder.

        Parameters
        ----------
        media_path : string
            media path of file we want to upload to Drive.
        parent_id : string
            folder id where we want to upload the file.
        file_name : type
            name for file in Drive.


        Returns
        -------
        string
            id of uploaded file.

        """
        service = self.drive_connection()
        folder_id = parent_id
        file_metadata = {
        'name': file_name,
        'parents': [folder_id],
        'visibility': 'DEFAULT'
        }
        media = MediaFileUpload(media_path,resumable=True)
        file = service.files().create(body=file_metadata, media_body=media,fields='id').execute()
        file_id = file.get('id')
        perm = {
        "type":"anyone",
        "role":"reader"
        }
        service.permissions().create(fileId=file_id, body = perm).execute()
        return file_id
