import pymysql
from db_credentials import credentials
import json



class DatabaseManageer(object):
    """this class contains all the functions required for the service for get
       an put data in 'drive_file_register' table ."""

    def conection_to_db(self):
        """set de connection with the data base and get the credentials
           from credentials.py.

        Returns
        db
        type
            data base connection.

        """
        host = credentials["host"]
        user = credentials["user"]
        passw = credentials["password"]
        db = credentials["data_base"]
        db = pymysql.connect(host,user,passw,db )
        return db

    def file_db_register(self,file_name,file_path):
        """Save file name and file drive path in 'drive_file_register' table.

        Parameters
        file_name : string
            file name we want to save`.
        file_path : string
            file url we want to save.

        Returns
        None
        type
            None.

        """
        db = self.conection_to_db()
        cursor = db.cursor()
        query = f"INSERT INTO drive_file_register(file_name, file_url) VALUES ('{file_name}','{file_path}');"
        cursor.execute(query)
        db.commit()
        db.close()

    def file_by_id(self, id):
        """Gets file name and url for a given id.

        Parameters
        id : string
            file identificator in data base.

        Returns
        ------
        type
            json with file data.

        """
        db = self.conection_to_db()
        cursor = db.cursor()
        cursor.execute(f"SELECT id, file_name, file_url FROM drive_file_register WHERE id = '{id}'")
        data = cursor.fetchall()
        dic = {"id" : data[0][0], "file_name" : data[0][1], "file_url" : data[0][2]}
        db.close()
        return json.dumps(dic)



    def full_db_register(self):
        """get a json with all data files in 'drive_file_register' table.

        Returns
        -------
        type
            json with all files data.

        """
        db = self.conection_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, file_name, file_url FROM drive_file_register")
        data = cursor.fetchall()
        db.close()
        dic={}
        for counter,item in enumerate(data):
            dic.update({counter : {"id" : item[0], "file_name" : item[1], "file_url" : item[2]}})
        return json.dumps(dic)
