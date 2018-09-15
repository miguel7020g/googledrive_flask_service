# googledrive_flask_service
flask service for upload and list files to google drive


HOW TO RUN!

place your credentials in the project directory:

  client_id.json
  credentials.json
  db_credentials.py
  token.json

make sure you got the requirements, place the terminal in your project and run:

  pip install -r requirements.txt


then run the next commands:

  1.export FLASK_APP=drive_servuice_miguel.py
  2.flask run

examples for try the service using curl:

1.Load a file in given google drive path


  curl -i -X POST -H 'Content-Type: application/json' -d '{"media_path": "/home/miguel/Pictures/Wallpapers/spacex.jpg", "drive_path": "my_first_upload/sub1/sub2_1", "file_name":"spacex.jpg"}' http://localhost:5000/drive_service

2.Get the url file by id
  curl http://localhost:5000/drive_service?id=2

3.list all the file in the drive with url_for
  curl http://localhost:5000/drive_service?id=2
